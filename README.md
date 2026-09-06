# 🕵️‍♀️ Synthetic Identity & Fraud Graph Pipeline

I built this repo to explore some recent thoughts on **GenAI Synthetic Identities** and **Agentic Commerce**. As AI makes it easier to spoof KYC documents, catching fraud is no longer just about document verification—it’s a massive data engineering and Master Data Management (MDM) problem. 

This is a lightweight Proof of Work demonstrating how I approach building fraud data pipelines to detect these vectors.

## How it works:

1. **The PySpark MDM Layer (`synthetic_identity_mdm.py`)**
   Synthetic IDs often share underlying infrastructure (like device fingerprints or IPs) while using AI-generated phonetic variations of names (e.g., Jon Smyth vs. John Smith). I use PySpark to clean garbage data, apply phonetic blocking (Soundex), and prep the data for graph clustering without blowing up the cluster with Cartesian joins.

2. **The SQL Velocity Layer (`fraud_feature_engineering.sql`)**
   Not all high-velocity purchasing is fraud—some of it is legitimate Agentic Commerce (AI buying groceries). I built dbt/Snowflake window functions to isolate bot-driven wash trading and AML structuring (rapid-fire transactions just under the $10k threshold) from normal user behavior.

## Want to run it?
I included a `generate_mock_data.py` script. Run that first to generate the synthetic users and rapid-fire bot transactions, then run the PySpark script to watch it flag the synthetic ring. 

