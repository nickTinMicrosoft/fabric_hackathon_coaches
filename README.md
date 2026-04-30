# Fabric Hackathon — Coaches Repository

Welcome to the **MS Azure Days — Fabric Hackathon** coaches repository. This repo contains all data files, scripts, documentation, and live demo simulators needed to run and support the hackathon.

---

## Repository Structure

| Folder | Description |
|--------|-------------|
| [DataFiles](DataFiles/) | Raw data files used across hackathon challenges (Parquet, images, etc.) |
| [Documents](Documents/) | Hackathon guides, architecture references, and goal instructions (PDFs) |
| [Scripts](Scripts/) | Database scripts, data-generation utilities, and live streaming simulators |

---

## Quick Start

1. **Read the docs** — Start with the [Documents](Documents/) folder for the hackathon intro and architecture overview.
2. **Provision databases** — Use the scripts in [Scripts/SQL](Scripts/SQL/) and [Scripts/Cosmos](Scripts/Cosmos/) to create and seed your databases.
3. **Load data** — The [DataFiles](DataFiles/) folder contains pre-built Parquet files and images for the tumor-data challenge.
4. **Configure secrets** — Copy `.env.example` or create a `.env` file in the project root with your connection strings and API keys (see below).
5. **Run simulators** — Launch the Python streaming apps in [Scripts/Python](Scripts/Python/) to generate live data for Fabric Eventstreams.

---

## Environment Setup

All Python scripts load secrets from a `.env` file in the project root. This file is **gitignored** and must be created locally.

Required variables (fill in your values):

```
# Azure OpenAI
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_CHAT_MODEL=gpt-4o-mini

# Azure AI Search
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_SEARCH_INDEX_NAME=

# IoT Hub (Metra trains)
IOT_RED_LINE_CONN_STR=
IOT_BLUE_LINE_CONN_STR=
IOT_GREEN_LINE_CONN_STR=

# Event Hubs
EVENTHUB_TRAIN_CONN_STR=
EVENTHUB_VITALS_CONN_STR=
EVENTHUB_MOVEMENT_CONN_STR=
EVENTHUB_FLIGHT_CONN_STR=
```

---

## Folder Overview

### DataFiles
Contains the raw data assets participants will ingest into Microsoft Fabric. Currently includes Parquet files with tumor image metadata and the corresponding images.

### Documents
All hackathon PDFs — introduction, architecture diagram, and Goals 1 through 4. Work through them sequentially.

### Scripts
Organized by technology:
- **Cosmos** — JSON seed data for Azure Cosmos DB
- **SQL** — DDL and seed scripts for SQL databases
- **Python** — Live streaming simulators and data-generation utilities:

| App | Description |
|-----|-------------|
| [Hospital](Scripts/Python/Hospital/) | Simulates patient vitals and movement → Event Hub |
| [Metra](Scripts/Python/Metra/) | Simulates NYC metro train telemetry → Event Hub / IoT Hub |
| [FlightTracker](Scripts/Python/FlightTracker/) | Streams live ADS-B aircraft data from PiAware → Event Hub |
| [LineageAgent](Scripts/Python/LineageAgent/) | Fabric notebook — hydrates Lakehouse with catalog & lineage metadata for a Data Agent |
| [Orchistrator](Scripts/Python/Orchistrator/) | Multi-agent orchestrator using Azure OpenAI + AI Search + Fabric Agents |
| [Tumor Data](Scripts/Python/Tumor%20Data/) | Generates Parquet files from tumor images with synthetic metadata |

---

[View the Documents README →](Documents/README.md)
