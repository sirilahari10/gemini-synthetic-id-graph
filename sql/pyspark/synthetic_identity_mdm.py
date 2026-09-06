"""
Detects Synthetic Identities by clustering users who share overlapping 
but slightly obfuscated PII (e.g., same device fingerprint, fuzzy-matched names, 
but different SSNs) without causing Cartesian explosions.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, soundex

spark = SparkSession.builder.appName("Gemini_Synthetic_ID_Detection").getOrCreate()

df_users = spark.read.parquet("s3://gemini-datalake/users/")

# Apply phonetic blocking to catch AI-generated synthetic names 
# tied to the same underlying device/IP clusters
df_blocked = df_users.withColumn("name_block", soundex(col("last_name")))

# (In production: graph-based clustering would resolve these into a single Fraud Entity ID)
df_blocked.write.mode("overwrite").parquet("s3://processed-zone/fraud_entities/")
