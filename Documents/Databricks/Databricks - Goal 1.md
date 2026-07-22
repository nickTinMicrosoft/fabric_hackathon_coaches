---
layout: page
title: Databricks Goal 1
---

GOAL 1 — Ingest SQL → ADLS Gen2 (Parquet) using PySpark
🎯 What Users Are Doing
Users are extracting structured enterprise data from SQL systems and landing it in a scalable cloud data lake.
❓ Why This Matters
    • Decouples analytics from operational databases
    • Enables big data scale
    • Reduces SQL server load
    • Standardizes data into open Parquet format

Architecture
SQL Database → Azure Databricks (PySpark) → ADLS Gen2 (Parquet)

Step 1: Read from SQL via JDBC (PySpark)

jdbc_url = "jdbc:sqlserver://<server>.database.windows.net:1433;database=<db>;encrypt=true;trustServerCertificate=false;loginTimeout=30;"

connection_properties = {
    "user": "<username>",
    "password": "<password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

df_customers = (spark.read
    .format("jdbc")
    .option("url", jdbc_url)
    .option("dbtable", "dbo.Customers")
    .options(**connection_properties)
    .load())

display(df_customers)

Step 2: Write as Parquet to ADLS

base_path = "abfss://hackathon@<storage>.dfs.core.windows.net/bronze/customers"

df_customers.write \
    .mode("overwrite") \
    .format("parquet") \
    .save(base_path)
Connect Azure Databricks to Azure SQL
https://learn.microsoft.com/en-us/azure/databricks/connect/external-systems/azure-sql-database
Spark JDBC (for PySpark ingestion)
https://learn.microsoft.com/en-us/azure/databricks/connect/external-systems/jdbc
Access Azure Data Lake Gen2 from Databricks
https://learn.microsoft.com/en-us/azure/databricks/connect/storage/azure-storage
Use ADLS Gen2 with Databricks (end-to-end example)
https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-use-databricks-spark


---

**Navigation:** [Databricks Home](README.md) &middot; [Next: Goal 2 &mdash; Register Data in Unity Catalog &rarr;](Databricks%20-%20Goal%202.md)
