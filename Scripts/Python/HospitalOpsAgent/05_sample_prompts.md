# Step 5 — Sample Prompts to Test the Agent

Use these prompts to validate that your Hospital Operations Agent is working correctly. Copy and paste them into the agent chat.

---

## 🟢 Basic Queries

| # | Prompt |
|---|--------|
| 1 | **How many patients are currently in the hospital?** |
| 2 | **Show me all patients currently in Room 105.** |
| 3 | **Which patients were admitted in the last 30 minutes?** |
| 4 | **List all recent discharges.** |
| 5 | **What is the current room occupancy breakdown?** |

---

## 🟡 Vitals & Clinical Queries

| # | Prompt |
|---|--------|
| 6 | **Are any patients in critical condition right now?** |
| 7 | **Show me the latest vitals for PAT-10001.** |
| 8 | **Which patients have an SpO2 below 92%?** |
| 9 | **Who has the highest heart rate right now?** |
| 10 | **Are there any patients with a fever above 101°F?** |
| 11 | **Show me the condition distribution — how many stable, elevated, and critical patients do we have?** |

---

## 🔴 Operational / Cross-Data Queries

| # | Prompt |
|---|--------|
| 12 | **Give me a full status report on PAT-10003 — location, vitals, and movement history.** |
| 13 | **Which patients are currently in X-Ray?** |
| 14 | **Show me the vitals trend for PAT-10005 over the last hour.** |
| 15 | **Are there any critical patients in the ICU right now?** |
| 16 | **How many patients have been transferred more than twice?** |
| 17 | **Give me a hospital operations summary — census, critical alerts, and recent activity.** |

---

## 🟣 Trend & Analytical Queries

| # | Prompt |
|---|--------|
| 18 | **Has any patient's condition changed in the last 30 minutes?** |
| 19 | **Show me the average heart rate by condition type over the last hour.** |
| 20 | **Which diagnosis codes are most common among current patients?** |
| 21 | **Plot the SpO2 trend for all critical patients over the last 30 minutes.** |

---

## Expected Behavior

- The agent should respond with **concise summaries** and **tables** for multi-patient results.
- **Critical patients** should be flagged proactively.
- When asked about a specific patient, the agent should **join vitals + movement data** for a complete picture.
- Time-based queries should clearly state the **time window** used.
- If no data is found, the agent should say so clearly rather than returning empty results silently.
