# Hackathon Documentation

This folder contains all the guides and reference materials for the **MS Azure Days — Fabric Hackathon**. Work through the documents in the order listed below.

---

## Overview & Setup

Start here before diving into the goals:

| Document | Description |
|----------|-------------|
| [Intro](MS%20Azure%20Days%20Fabric%20Hackathon%20-%200%20-%20Intro.md) | Hackathon overview, prerequisites, environment setup, and rules |
| [Architecture](MS%20Azure%20Days%20Fabric%20Hackathon%20-%200%20-%20Architecture.pdf) | End-to-end solution architecture and design reference |

---

## Hackathon Goals

Complete these challenges in order:

| Goal | Document |
|------|----------|
| Goal 1 | [Ingest Data from Two Sources (Bronze)](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%201.md) |
| Goal 2 | [Transform Data into the Silver Lakehouse](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%202.md) |
| Goal 3 | [Use AI to Discover Intelligence in Semi-Structured Data](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%203.md) |
| Goal 4 | [Build the Gold Lakehouse and Serve It](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%204.md) |

> **Example notebooks:** ready-to-import `.ipynb` files for the Silver, AI, and Gold goals are in the [`Notebooks/`](../Notebooks/) folder — see the [Notebooks README](../Notebooks/README.md).

---

## Databricks Hackathon

The Databricks hackathon guides are in the [`Databricks/`](Databricks/) folder. See the [Databricks README](Databricks/README.md) for a full index.

| Goal | Document | Description |
|------|----------|-------------|
| Goal 1 | [Databricks - Goal 1](Databricks/Databricks%20-%20Goal%201.md) | Ingest SQL → ADLS Gen2 (Parquet) using PySpark |
| Goal 2 | [Databricks - Goal 2](Databricks/Databricks%20-%20Goal%202.md) | Register Data in Unity Catalog |
| Goal 3 | [Databricks - Goal 3](Databricks/Databricks%20-%20Goal%203.md) | Analyze Using SQL |
| Goal 4 | [Databricks - Goal 4](Databricks/Databricks%20-%20Goal%204.md) | Build Curated Tables (Silver & Gold) |
| Goal 5 | [Databricks - Goal 5](Databricks/Databricks%20-%20Goal%205.md) | Add AI Agent Layer (Natural Language Data Access) |
| Goal 6 | [Databricks - Goal 6](Databricks/Databricks%20-%20Goal%206.md) | Mirror to Microsoft Fabric |
| Goal 7 | [Databricks - Goal 7](Databricks/Databricks%20-%20Goal%207.md) | Model the Data & Build a Report / Dashboard |

---

## Suggested Workflow

### Fabric Hackathon
```
Intro → Architecture → Goal 1 → Goal 2 → Goal 3 → Goal 4
```

1. Read the **Intro** to set up your environment
2. Study the **Architecture** to understand what you're building
3. Work through **Goals 1–4** sequentially — each builds on the previous

### Databricks Hackathon
```
Goal 1 → Goal 2 → Goal 3 → Goal 4 → Goal 5 → Goal 6 → Goal 7
```

1. Work through **Goals 1–7** sequentially — each builds on the previous

---

[← Back to main README](../README.md)
