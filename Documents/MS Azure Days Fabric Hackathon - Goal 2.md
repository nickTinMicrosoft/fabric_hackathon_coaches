---
layout: page
title: Goal 2 - Transform Data into the Silver Lakehouse
---

# Transform Data into the Silver Lakehouse (2 hours)

Now that your raw data has landed in the **Bronze** layer, transform it into a clean, conformed **Silver Lakehouse**. In this goal you'll use **Notebooks** to shape the raw sources into analytics-ready Delta tables.

## What to Do

- Create (or attach) a **SilverLakehouse** to hold your transformed tables.
- Use **Notebooks** (Spark / PySpark) to read from your Bronze sources and clean, conform, and reshape the data.
- Standardize column names, enforce primary keys, and remove duplicates.
- Flatten nested or semi-structured fields (for example, JSON from a Cosmos mirror) into tidy tables.
- Write each result as a managed **Delta** table so it is idempotent and re-runnable.

While Notebooks are the focus here, Fabric also supports Dataflows, SQL, and views — the reference material below covers those options too.

> **Example notebooks:** See [`Notebooks/`](../Notebooks/) for two Silver examples —
> `1 - Normalize SIS to Silver Lakehouse` (Azure SQL → Silver) and
> `2 - Transform Grad Exams to Silver Lakehouse` (Cosmos → Silver).

## Notes and References

### 1. Transform with Dataflows (Visual / No-Code)

Description: Use Dataflow Gen2 to visually prepare and transform data using Power Query before landing it into your Lakehouse or curated tables. It is great for filtering, joins, type changes, and light cleansing at scale.

- [Tutorial - Copy data and transform with Dataflow](https://learn.microsoft.com/en-us/fabric/data-factory/tutorial-load-data-lakehouse-transform)

### 2. Transform with Notebooks (Code-Driven)

Description: Use Microsoft Fabric Notebooks (Spark Python/SQL) to clean, enrich, and reshape your data after ingestion. Notebooks give you full control with code and are ideal for complex transformations and machine learning preparation.

- [How to use Microsoft Fabric Notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)

### 3. Prepare and Transform in Lakehouse Using Notebooks

Description: A hands-on tutorial showing how to take raw files, transform them using Spark, write them as Delta tables, and then query with SQL within Fabric.

- [Transform data with Apache Spark and SQL in OneLake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-onecopy-quickstart)

### 4. Transform with Dataflow (Gen2 Detailed)

Description: Step-by-step guide to use Dataflow Gen2 to transform data from raw to gold tables using Power Query transformations.

- [Module - Transform with a dataflow in Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/tutorial-end-to-end-dataflow)

### 5. Transform Using SQL Queries

Description: Once data is stored in your Lakehouse, a SQL analytics endpoint lets you run familiar T-SQL queries to aggregate, filter, and prepare data for analytics or BI workloads.

- [Lakehouse SQL analytics endpoint overview](https://learn.microsoft.com/en-us/fabric/data-warehouse/get-started-lakehouse-sql-analytics-endpoint)

### 6. Create SQL Views for Analytics

Description: In Fabric, you can define SQL views over your transformed data to simplify query logic or expose curated datasets for BI tools or users.

- [Discussion: Create SQL views on Lakehouse tables](https://community.fabric.microsoft.com/t5/Data-Engineering/Create-SQL-views-with-Fabric-lakehouse-SQL-endpoint-from-Fabric/m-p/3977200)

### 7. Use Materialized Lake Views for Faster Analytics

Description: Materialized lake views let you define transformations in SQL and persist the results as Delta tables. Fabric manages refresh behavior and dependencies, which can improve performance and simplify downstream reporting.

- [What are materialized lake views in Microsoft Fabric?](https://learn.microsoft.com/fabric/data-engineering/materialized-lake-views/overview-materialized-lake-view)


---

**Navigation:** [&larr; Previous: Goal 1 &mdash; Ingest (Bronze)](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%201.md) &middot; [Next: Goal 3 &mdash; AI Insights &rarr;](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%203.md)
