# Student DB — SQL Server Scripts

This folder contains the SQL scripts to create and seed the **Student Info System** database.

---

## Contents

- **`hackathonSqlCreateandSeed.sql`** — Creates the following tables and inserts sample data:

### Tables

| Table | Description |
|-------|-------------|
| `students` | 100 student records with cartoon-themed names |
| `classes` | 3 classes — Microbiology, Economics, Cartoon Studies |
| `enrollments` | Links students to classes (many-to-many relationship) |

### Key Constraints

- Students have unique names
- Classes are assigned to one of three rooms: `room_100`, `room_200`, `room_300`
- Enrollments enforce a unique `(student_id, class_id)` pair to prevent duplicates

---

## How to Use

1. Connect to your SQL Server or Azure SQL database.
2. Run `hackathonSqlCreateandSeed.sql` to create the schema and seed the data.

```sql
-- Example using sqlcmd
sqlcmd -S your_server -d your_database -i hackathonSqlCreateandSeed.sql
```

---

[← Back to SQL README](../README.md)
