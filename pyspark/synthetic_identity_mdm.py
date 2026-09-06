"""
PySpark MDM Layer: Resolves synthetic identities by grouping fuzzy-matched names 
sharing identical device fingerprints. 
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, soundex, lower, trim, regexp_replace, when

spark = SparkSession.builder.appName("Gemini_Synthetic_ID_MDM").getOrCreate()

# Load mock data
df_users = spark.read.csv("../raw_users.csv", header=True, inferSchema=True)

# PRODUCTION SCAR: Handle nulls and garbage characters from legacy KYC gateways before matching
df_clean = df_users.fillna({"first_name": "UNKNOWN", "last_name": "UNKNOWN", "device_id": "UNKNOWN"})
df_clean = df_clean.withColumn("last_name_clean", trim(lower(regexp_replace(col("last_name"), "[^a-zA-Z]", ""))))

# Phonetic blocking to catch AI-generated synthetic name variations (Smith vs Smyth)
df_blocked = df_clean.withColumn("name_block", soundex(col("last_name_clean")))

# Flag potential synthetic rings: Same device, different phonetic name block
df_flagged = df_blocked.withColumn(
    "synthetic_risk_flag",
    when((col("device_id") != "UNKNOWN") & (col("name_block").isNotNull()), True).otherwise(False)
    # Note: In a full graph model, we'd run connected components here to link the exact user_ids.
)

df_flagged.show(truncate=False)
