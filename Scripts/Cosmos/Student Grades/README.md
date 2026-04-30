# Student Grades — Cosmos DB Seed Data

This folder contains the JSON seed data for the **Student Grades** Cosmos DB container.

---

## Contents

- **`student_grades_seed.json`** — An array of 100 student grade documents with the following schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique document identifier |
| `Student_ID` | integer | Student identifier (matches the SQL `students` table) |
| `Student_Name` | string | Student display name |
| `Class_Room` | string | Room assignment (`room_100`, `room_200`, `room_300`) |
| `Grade` | string | Letter grade (`A`, `B`, `C`) |

---

## How to Use

1. Create a Cosmos DB database and container (partition key: `/Class_Room`).
2. Import `student_grades_seed.json` using the Azure Portal Data Explorer, Azure CLI, or any Cosmos DB SDK.

---

[← Back to Cosmos README](../README.md)
