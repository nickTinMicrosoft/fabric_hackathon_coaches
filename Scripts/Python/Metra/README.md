# Metra Train Simulators

This folder contains two Python simulators that generate NYC metro train telemetry and stream it to Azure for ingestion into Microsoft Fabric.

---

## Apps

| Script | Description |
|--------|-------------|
| `trains_eventhub.py` | Sends train telemetry (position, speed, status) for 3 simulated trains to **Azure Event Hub** |
| `trains_iothub.py` | Sends the same telemetry to **Azure IoT Hub** using per-device connection strings |

Both scripts simulate Red, Blue, and Green train lines along realistic NYC routes. The Green line train occasionally experiences station delays.

---

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the following are set in the `.env` file at the project root:

   **For Event Hub version (`trains_eventhub.py`):**
   ```
   EVENTHUB_TRAIN_CONN_STR=<your-connection-string>
   EVENTHUB_TRAIN_NAME=metrotrain
   ```

   **For IoT Hub version (`trains_iothub.py`):**
   ```
   IOT_RED_LINE_CONN_STR=<your-device-connection-string>
   IOT_BLUE_LINE_CONN_STR=<your-device-connection-string>
   IOT_GREEN_LINE_CONN_STR=<your-device-connection-string>
   ```

## Usage

```bash
# Event Hub version
python trains_eventhub.py

# IoT Hub version
python trains_iothub.py
```

Press `Ctrl+C` to stop either simulator.

---

## Data Fields

| Field | Description |
|-------|-------------|
| `trainId` | Train identifier (e.g., Train-Red-1) |
| `line` | Line name — Red, Blue, or Green |
| `lat` / `lon` | GPS coordinates along the route |
| `speed` | Ground speed (mph) |
| `status` | OnTime or Delayed |
| `timestamp` | UTC timestamp |

---

## Notes

- The IoT Hub version requires 3 registered devices (`red-line`, `blue-line`, `green-line`) in your IoT Hub.
- The Event Hub version uses a shared connection with a single producer client.
- The IoT Hub version additionally requires `azure-iot-device` (`pip install azure-iot-device`).

---

[← Back to Python README](../README.md)
