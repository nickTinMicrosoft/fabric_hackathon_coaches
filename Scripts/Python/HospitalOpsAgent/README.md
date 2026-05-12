# Hospital Operations Agent — Fabric RTI Data Agent

This folder contains everything you need to build a **Hospital Operations Agent** in Microsoft Fabric. The agent monitors real-time patient vitals and movement data streamed from the [Hospital simulators](../Hospital/) and answers operational questions using natural language.

---

## Prerequisites

Before building the agent you need the following Fabric artifacts already running:

| Artifact | Purpose |
|----------|---------|
| **Eventstream** (vitals) | Ingests `hospital-vitals` events from Event Hub |
| **Eventstream** (movement) | Ingests `hospital-movement` events from Event Hub |
| **KQL Database** | Destination for both eventstreams (real-time analytics) |
| **KQL Tables** | `HospitalVitals` and `HospitalMovement` (see schemas below) |

> The simulators (`hospital_vitals.py` and `hospital_movement.py`) must be running and sending data to Event Hub for the agent to have data to query.

---

## Quick Start

1. **Create a KQL Database** in your Fabric workspace (see [01_kql_setup.md](01_kql_setup.md)).
2. **Create the KQL tables** using the scripts in [02_kql_tables.kql](02_kql_tables.kql).
3. **Connect the Eventstreams** to the KQL database (see [03_eventstream_setup.md](03_eventstream_setup.md)).
4. **Create the Fabric Agent** and paste in the instructions from [04_agent_instructions.md](04_agent_instructions.md).
5. **Add the KQL Database** as a data source in the agent.
6. **Test the agent** with the sample prompts in [05_sample_prompts.md](05_sample_prompts.md).

---

## Folder Contents

| File | Description |
|------|-------------|
| [01_kql_setup.md](01_kql_setup.md) | Step-by-step guide to create the KQL Database in Fabric |
| [02_kql_tables.kql](02_kql_tables.kql) | KQL scripts to create the `HospitalVitals` and `HospitalMovement` tables |
| [03_eventstream_setup.md](03_eventstream_setup.md) | How to connect Event Hub → Eventstream → KQL Database |
| [04_agent_instructions.md](04_agent_instructions.md) | **Copy-paste agent instructions** for the Fabric Data Agent |
| [05_sample_prompts.md](05_sample_prompts.md) | Ready-to-use test prompts and expected behavior |
| [06_agent_guidelines.md](06_agent_guidelines.md) | Behavioral guidelines, guardrails, and response-format rules |

---

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌───────────────┐
│ hospital_vitals │────▶│  Event Hub   │────▶│  Eventstream     │────▶│  KQL Database │
│ hospital_move   │     │  (Azure)     │     │  (Fabric)        │     │  (Fabric RTI) │
└─────────────────┘     └──────────────┘     └──────────────────┘     └───────┬───────┘
                                                                              │
                                                                              ▼
                                                                     ┌───────────────┐
                                                                     │ Fabric Agent  │
                                                                     │ (Ops Agent)   │
                                                                     └───────────────┘
```

---

[← Back to Python README](../README.md)
