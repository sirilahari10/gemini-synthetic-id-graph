-- dbt Model: High-Velocity Fiat/Crypto Wash Trading Detection
-- Captures bot behavior vs. legitimate Agentic Commerce

{{ config(materialized='table', tags=['fraud_detection']) }}

WITH raw_tx AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

velocity_metrics AS (
    SELECT 
        user_id,
        tx_time,
        -- Production Scar: Coalesce null amounts to 0 to prevent downstream math failures
        COALESCE(amount_usd, 0) AS safe_amount_usd,
        
        -- Time since last transaction to catch rapid-fire API bots
        TIMEDIFF(second, LAG(tx_time) OVER (PARTITION BY user_id ORDER BY tx_time), tx_time) as seconds_since_last_tx,
        
        -- 24h rolling velocity
        SUM(COALESCE(amount_usd, 0)) OVER (
            PARTITION BY user_id 
            ORDER BY tx_time 
            RANGE BETWEEN INTERVAL '24 HOURS' PRECEDING AND CURRENT ROW
        ) AS rolling_24h_volume
    FROM raw_tx
)

SELECT 
    user_id,
    rolling_24h_volume,
    -- Rule 1: High velocity API bot (>$50k in under 10 seconds)
    IFF(seconds_since_last_tx < 10 AND rolling_24h_volume > 50000, TRUE, FALSE) AS is_bot_velocity,
    
    -- Rule 2: Structuring / Smurfing (Repeated transactions just under the $10k AML reporting limit)
    IFF(safe_amount_usd BETWEEN 9000 AND 9999 AND seconds_since_last_tx < 60, TRUE, FALSE) AS is_structuring_risk
FROM velocity_metrics
WHERE is_bot_velocity = TRUE OR is_structuring_risk = TRUE;
