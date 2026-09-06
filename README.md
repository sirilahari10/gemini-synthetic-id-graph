# 🕵️‍♀️ Synthetic Identity & Fraud Detection Platform
A hybrid Data Engineering & Data Science Proof of Work designed to detect synthetic identities and crypto/fiat money laundering vectors. 

**Core Architecture:**
*   **Identity Resolution (PySpark):** Utilizes phonetic blocking and fuzzy matching to catch synthetic identities sharing fragmented PII across accounts.
*   **Feature Engineering (Advanced SQL):** Snowflake/dbt models calculating high-velocity fiat-to-crypto wash trading and account takeover (ATO) signals.
*   **Agentic Fraud Analysis:** Integrates an LLM-based agent to evaluate whether high-frequency transaction patterns resemble automated "Agentic Commerce" (bread, milk, eggs) or malicious bot-driven asset stripping.
