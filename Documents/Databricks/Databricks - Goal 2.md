---
layout: page
title: Databricks Goal 2
---

GOAL 2 — Register Data in Unity Catalog
🎯 What Users Are Doing
Users register cloud storage data into a governed metastore.
❓ Why This Matters
    • Centralized governance
    • Access control (RBAC)
    • Data lineage
    • Secure sharing

Catalog might be created just create schema username_Schema
Step 1: Create Catalog & Schema

CREATE CATALOG hackathon;
CREATE SCHEMA hackathon.bronze;

Step 2: Register External Table

CREATE TABLE hackathon.bronze.customers
USING PARQUET
LOCATION 'abfss://hackathon@<storage>.dfs.core.windows.net/bronze/customers';

Unity Catalog Docs
https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/
Create Catalogs & Schemas
https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-syntax-ddl-create-catalog
Create External Locations (for ADLS)
https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/external-locations
Create External Tables
https://learn.microsoft.com/en-us/azure/databricks/tables/external
Manage Permissions (RBAC)
https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/


Optional use Notbook and mount the storage and load it in catalog

Use Azure Data Lake Storage Gen2 with Azure Databricks
https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-use-databricks-spark
Mount ADLS Gen2 to Databricks
https://learn.microsoft.com/en-us/azure/databricks/dbfs/mounts
Access ADLS using ABFSS (Recommended)
https://learn.microsoft.com/en-us/azure/databricks/connect/storage/azure-storage


---

**Navigation:** [&larr; Previous: Goal 1 &mdash; Ingest SQL to ADLS (Parquet)](Databricks%20-%20Goal%201.md) &middot; [Next: Goal 3 &mdash; Analyze Using SQL &rarr;](Databricks%20-%20Goal%203.md)
