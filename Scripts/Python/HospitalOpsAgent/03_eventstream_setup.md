# Step 3 — Connect Event Hub to KQL Database via Eventstream

You need **two Eventstreams** — one for vitals and one for movement.

---

## Eventstream 1: Hospital Vitals

### Create the Eventstream

1. In your Fabric workspace, click **+ New item** → **Eventstream**.
2. Name it: `es-hospital-vitals`
3. Click **Create**.

### Add the Source (Event Hub)

1. In the Eventstream canvas, click **New source** → **Azure Event Hubs**.
2. Configure:
   - **Connection string**: Use the same connection string from `EVENTHUB_VITALS_CONN_STR` in your `.env` file.
   - **Event Hub name**: `hospital-vitals` (or the value of `EVENTHUB_VITALS_NAME`).
   - **Consumer group**: `$Default`
   - **Data format**: JSON
3. Click **Connect**.

### Add the Destination (KQL Database)

1. Click **New destination** → **KQL Database**.
2. Select your **HospitalOpsDB** (or whatever you named it in Step 1).
3. Configure:
   - **Table**: `HospitalVitals`
   - **Input data format**: JSON
   - **Mapping**: `HospitalVitals_mapping`
4. Click **Save**.

### Activate

1. Click **Publish** on the Eventstream toolbar.
2. Verify data is flowing — you should see events arriving in the preview pane.

---

## Eventstream 2: Hospital Movement

### Create the Eventstream

1. Click **+ New item** → **Eventstream**.
2. Name it: `es-hospital-movement`
3. Click **Create**.

### Add the Source (Event Hub)

1. Click **New source** → **Azure Event Hubs**.
2. Configure:
   - **Connection string**: Use `EVENTHUB_MOVEMENT_CONN_STR` from your `.env`.
   - **Event Hub name**: `hospital-movement` (or `EVENTHUB_MOVEMENT_NAME`).
   - **Consumer group**: `$Default`
   - **Data format**: JSON
3. Click **Connect**.

### Add the Destination (KQL Database)

1. Click **New destination** → **KQL Database**.
2. Select your **HospitalOpsDB**.
3. Configure:
   - **Table**: `HospitalMovement`
   - **Input data format**: JSON
   - **Mapping**: `HospitalMovement_mapping`
4. Click **Save**.

### Activate

1. Click **Publish**.
2. Verify data is flowing.

---

## Verify End-to-End

Run these queries in your KQL Database to confirm data is arriving:

```kql
HospitalVitals
| take 10

HospitalMovement
| take 10
```

You should see rows with recent timestamps if the simulators are running.

---

## Next Step

Proceed to [04_agent_instructions.md](04_agent_instructions.md) to build the Fabric Agent.
