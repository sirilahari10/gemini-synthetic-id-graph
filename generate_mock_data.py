"""
Generates messy, realistic user and transaction data to test the synthetic ID and velocity models.
Run this first to populate the /raw_data directory.
"""
import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

def create_mock_data():
    np.random.seed(42)
    
    # 1. Generate messy user data (Simulating synthetic IDs with slight name variations)
    users = [
        {"user_id": str(uuid.uuid4()), "first_name": "John", "last_name": "Smith", "device_id": "dev_123", "kyc_status": "verified"},
        {"user_id": str(uuid.uuid4()), "first_name": "Jon", "last_name": "Smyth", "device_id": "dev_123", "kyc_status": "verified"}, # Synthetic ID sharing device
        {"user_id": str(uuid.uuid4()), "first_name": "Alice", "last_name": "   Wond3rland  ", "device_id": "dev_999", "kyc_status": "pending"}, # Messy data
        {"user_id": str(uuid.uuid4()), "first_name": None, "last_name": None, "device_id": "dev_000", "kyc_status": "rejected"} # Missing data
    ]
    pd.DataFrame(users).to_csv("raw_users.csv", index=False)

    # 2. Generate transaction data (Simulating normal vs. bot velocity)
    now = datetime.utcnow()
    txs = []
    
    # Normal user behavior (Agentic Commerce / Regular buying)
    for _ in range(5):
        txs.append({"tx_id": str(uuid.uuid4()), "user_id": users[0]["user_id"], "amount_usd": np.random.uniform(10, 50), "tx_time": now - timedelta(hours=np.random.randint(1, 24))})
        
    # Bot / Wash Trading behavior (Rapid fire fiat-to-crypto dumping)
    for i in range(10):
        txs.append({"tx_id": str(uuid.uuid4()), "user_id": users[1]["user_id"], "amount_usd": 9900.00, "tx_time": now - timedelta(seconds=i*2)}) # Structuring just under $10k

    pd.DataFrame(txs).to_csv("raw_transactions.csv", index=False)
    print("Mock data generated: raw_users.csv and raw_transactions.csv")

if __name__ == "__main__":
    create_mock_data()
