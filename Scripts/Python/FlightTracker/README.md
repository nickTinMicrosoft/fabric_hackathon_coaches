# PiAware Flight Tracker

Streams live ADS-B aircraft data from a local PiAware/dump1090 device to Azure Event Hub for ingestion into Microsoft Fabric.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your Event Hub connection string to the `.env` file in the project root:
   ```
   EVENTHUB_FLIGHT_CONN_STR=<your-connection-string>
   EVENTHUB_FLIGHT_NAME=flight-tracker
   ```

## Usage

```bash
# Run with defaults (localhost:8080, 5s interval)
python flight_tracker.py

# Custom PiAware host and polling interval
python flight_tracker.py --host 192.168.1.50 --port 8080 --interval 2
```

## Controls

| Action | Command |
|--------|---------|
| Start  | `python flight_tracker.py` |
| Stop   | `Ctrl+C` (graceful shutdown) |

## Data Fields Sent

| Field | Description |
|-------|-------------|
| `hex` | ICAO 24-bit aircraft address |
| `flight` | Callsign / flight number |
| `lat` / `lon` | Position coordinates |
| `alt_baro` | Barometric altitude (ft) |
| `alt_geom` | Geometric altitude (ft) |
| `gs` | Ground speed (knots) |
| `track` | Heading (degrees) |
| `squawk` | Transponder code |
| `category` | Aircraft category |
| `rssi` | Signal strength (dBFS) |
| `timestamp` | UTC timestamp of the reading |

## Architecture

```
PiAware (dump1090) → flight_tracker.py → Azure Event Hub → Fabric Eventstream
```
