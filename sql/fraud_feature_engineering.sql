-- Identifies rapid fiat-to-crypto velocity and potential wash trading behaviors
WITH account_funding AS (
    SELECT 
        user_id,
        transaction_time,
        asset_type, -- e.g., USD, BTC, Gemini_Stocks
        amount_usd,
        -- Calculate time since last transaction to spot rapid-fire bot behavior
        TIMEDIFF(second, LAG(transaction_time) OVER (PARTITION BY user_id ORDER BY transaction_time), transaction_time) as seconds_since_last_tx,
        -- Rolling 24-hour transaction volume
        SUM(amount_usd) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_time 
            RANGE BETWEEN INTERVAL '24 HOURS' PRECEDING AND CURRENT ROW
        ) AS rolling_24h_volume
    FROM raw.transactions
)

SELECT 
    user_id,
    rolling_24h_volume,
    -- Flag accounts buying/selling massive volumes in under 10 seconds (Bot/Agentic Fraud)
    IFF(seconds_since_last_tx < 10 AND rolling_24h_volume > 50000, TRUE, FALSE) AS is_high_velocity_risk
FROM account_funding
WHERE is_high_velocity_risk = TRUE;
