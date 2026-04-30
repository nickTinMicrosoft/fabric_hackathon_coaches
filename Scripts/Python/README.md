# Python Scripts

This folder contains Python streaming simulators, a multi-agent orchestrator, and data-generation utilities for the hackathon.

All apps load secrets from a `.env` file in the project root using `python-dotenv`.

---

## Apps

| Folder | Description |
|--------|-------------|
| [Hospital](Hospital/) | Simulates patient vitals and movement events → Azure Event Hub |
| [Metra](Metra/) | Simulates NYC metro train telemetry (3 lines) → Azure Event Hub or IoT Hub |
| [FlightTracker](FlightTracker/) | Streams live ADS-B aircraft data from a PiAware device → Azure Event Hub |
| [Orchistrator](Orchistrator/) | Multi-agent orchestrator using Azure OpenAI, AI Search, and Fabric Agents |
| [Tumor Data](Tumor%20Data/) | Generates a Parquet file from tumor images with synthetic medical metadata |

---

## Prerequisites

- Python 3.10+
- `python-dotenv` (`pip install python-dotenv`)
- App-specific dependencies listed in each folder's `requirements.txt`

---

## General Usage

```bash
# Install dependencies for a specific app
cd <app-folder>
pip install -r requirements.txt

# Run the app
python <script>.py
```

See each app's README for detailed setup and usage instructions.

---

[← Back to Scripts README](../README.md)
