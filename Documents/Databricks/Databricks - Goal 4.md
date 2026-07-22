---
layout: page
title: Databricks Goal 4
---

GOAL 4 — Build Curated Tables (Silver & Gold)
🎯 What Users Are Doing
They clean, normalize, and aggregate raw data into business-ready tables.
❓ Why This Matters
    • Removes duplicates
    • Enforces data standards
    • Improves performance
    • Creates reusable business models

Create Silver (Delta)

CREATE SCHEMA hackathon.silver;

CREATE OR REPLACE TABLE hackathon.silver.customers
AS
SELECT
  CAST(CustomerId AS STRING) AS CustomerId,
  UPPER(State) AS State,
  CreatedDate
FROM hackathon.bronze.customers;

Create Gold (Aggregated)

CREATE SCHEMA hackathon.gold;

CREATE OR REPLACE TABLE hackathon.gold.customers_by_state
AS
SELECT State, COUNT(*) AS total_customers
FROM hackathon.silver.customers
GROUP BY State;
Medallion Architecture
https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
Delta Lake on Azure Databricks
https://learn.microsoft.com/en-us/azure/databricks/delta/
Convert Parquet to Delta
https://learn.microsoft.com/en-us/azure/databricks/delta/convert-to-delta
Delta Optimization (OPTIMIZE, ZORDER)
https://learn.microsoft.com/en-us/azure/databricks/delta/optimizations/file-mgmt

---

**Navigation:** [&larr; Previous: Goal 3 &mdash; Analyze Using SQL](Databricks%20-%20Goal%203.md) &middot; [Next: Goal 5 &mdash; Add AI Agent Layer &rarr;](Databricks%20-%20Goal%205.md)
