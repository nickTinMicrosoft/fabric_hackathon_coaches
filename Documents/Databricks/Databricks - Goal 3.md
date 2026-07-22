---
layout: page
title: Databricks Goal 3
---

GOAL 3 — Analyze Using SQL
🎯 What Users Are Doing
Business users query curated lake data using standard SQL.
❓ Why This Matters
    • Democratizes analytics
    • Removes need for Spark coding
    • Enables BI dashboards

Example SQL Analysis

SELECT State, COUNT(*) AS customer_count
FROM hackathon.bronze.customers
GROUP BY State
ORDER BY customer_count DESC;


Databricks SQL Overview
https://learn.microsoft.com/en-us/azure/databricks/sql/
CREATE TABLE (USING syntax)
https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-create-table-using
SQL Functions Reference
https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/
Dashboards (for demo visuals)
https://learn.microsoft.com/en-us/azure/databricks/sql/dashboards/


---

**Navigation:** [&larr; Previous: Goal 2 &mdash; Register Data in Unity Catalog](Databricks%20-%20Goal%202.md) &middot; [Next: Goal 4 &mdash; Build Curated Tables (Silver & Gold) &rarr;](Databricks%20-%20Goal%204.md)
