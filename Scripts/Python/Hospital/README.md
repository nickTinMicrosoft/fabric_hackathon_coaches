# Hospital Simulators

This folder contains two Python simulators that generate realistic hospital data and stream it to Azure Event Hub for ingestion into Microsoft Fabric.

---

## Apps

| Script | Description |
|--------|-------------|
| `hospital_vitals.py` | Simulates vital-sign readings (heart rate, blood pressure, SpO2, temperature, respiratory rate) for 15 patients with conditions that shift over time |
| `hospital_movement.py` | Simulates patient movement events — admissions, room transfers, X-Ray visits, and discharges |

Both simulators use the same `PAT-XXXXX` patient IDs, so the data can be joined in Fabric.

---

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the following are set in the `.env` file at the project root:
   ```
   EVENTHUB_VITALS_CONN_STR=<your-connection-string>
   EVENTHUB_VITALS_NAME=hospital-vitals
   EVENTHUB_MOVEMENT_CONN_STR=<your-connection-string>
   EVENTHUB_MOVEMENT_NAME=hospital-movement
   ```

## Usage

```bash
# Start the vitals simulator
python hospital_vitals.py

# Start the movement simulator
python hospital_movement.py
```

Press `Ctrl+C` to stop either simulator.

---

## Data Fields

### Vitals (`hospital_vitals.py`)

| Field | Description |
|-------|-------------|
| `patient_id` | De-identified patient ID (PAT-XXXXX) |
| `condition` | Patient condition — stable, elevated, or critical |
| `heart_rate` | Beats per minute |
| `bp_systolic` / `bp_diastolic` | Blood pressure |
| `temperature_f` | Body temperature (°F) |
| `spo2` | Oxygen saturation (%) |
| `respiratory_rate` | Breaths per minute |

### Movement (`hospital_movement.py`)

| Field | Description |
|-------|-------------|
| `patient_id` | De-identified patient ID (PAT-XXXXX) |
| `event_type` | Admitted, Transferred, Sent to X-Ray, Returned from X-Ray, Discharged |
| `from_location` / `to_location` | Room or area |
| `diagnosis_code` / `diagnosis_desc` | ICD-10 code and description |

---

[← Back to Python README](../README.md)
