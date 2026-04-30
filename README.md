# Fabric Hackathon — Coaches Repository

Welcome to the **MS Azure Days — Fabric Hackathon** coaches repository. This repo contains all data files, scripts, and documentation needed to run and support the hackathon.

---

## Repository Structure

| Folder | Description |
|--------|-------------|
| [DataFiles](DataFiles/) | Raw data files used across hackathon challenges (Parquet, images, etc.) |
| [Documents](Documents/) | Hackathon guides, architecture references, and goal instructions |
| [Scripts](Scripts/) | Database scripts and data-generation utilities (SQL, Cosmos DB, Python) |

---

## Quick Start

1. **Read the docs** — Start with the [Documents](Documents/) folder for the hackathon intro and architecture overview.
2. **Provision databases** — Use the scripts in [Scripts](Scripts/) to create and seed your SQL and Cosmos DB databases.
3. **Load data** — The [DataFiles](DataFiles/) folder contains pre-built Parquet files and images for the tumor-data challenge.

---

## Folder Overview

### DataFiles
Contains the raw data assets participants will ingest into Microsoft Fabric. Currently includes Parquet files with tumor image metadata and the corresponding images.

### Documents
All hackathon PDFs — introduction, architecture diagram, and Goals 1 through 4. Work through them sequentially.

### Scripts
Automation and seed scripts organized by target technology:
- **Cosmos** — JSON seed data for Azure Cosmos DB
- **Python** — Data-generation utilities (e.g., Parquet file creation)
- **SQL** — DDL and seed scripts for SQL databases

---

[View the Documents README →](Documents/README.md)
