# temp-sql-sandbox — Intelligent University SQL DB

A **sandbox** (deliberately outside `fy27_student_demos`) that reimagines the
university SQL schema so **intelligence is discoverable** — not just records, but
outcomes and the leading indicators that predict them.

It replaces Brian Darcy's flat registrar model with a small **star schema**:
dimensions describe *who/what*, fact tables carry *outcomes* and *signals* you can
`GROUP BY`.

## Why this shape

| Business question | What makes it answerable here |
|---|---|
| **Retention** — who drops out? | `StudentTermStatus` (one row per student per term) + demographics + engagement signals (attendance, LMS logins) |
| **Graduation / time-to-degree** | `CumCreditsEarned` vs `Program.RequiredCredits` per term |
| **Cost-effectiveness** | `CourseSection` carries instructor + room cost and seats filled → cost per *completed* credit |
| **AI / the "why"** | `CourseReviewSignal` = AI-distilled sentiment/themes from the free-text course reviews in Blob Storage |

`StudentID` (1..55) and `CrsID` (1..54) match the reference data, so this DB
**joins the Cosmos grad-exam documents on `StudentID`** — SQL = structured drivers,
Cosmos = outcomes, Storage = the unstructured voice.

## Files

| File | Purpose |
|---|---|
| `sql/01_schema.sql` | DDL — drops existing objects (incl. legacy Brian tables) then creates the star schema + indexes |
| `generate_seed.py` | Deterministic generator that bakes real correlations into the data; writes `sql/02_seed.sql` |
| `sql/02_seed.sql` | Generated INSERTs (regenerate with the script; do not hand-edit) |
| `sql/03_queries.sql` | Ready-to-run "intelligence" queries (retention, cost, reviews) |

## The correlations that are baked in

A latent student **ability** (from `AdmissionScore`) drives grades, attendance and
engagement. From that:

- **Dropouts** cluster on low term-1 GPA, low attendance, higher financial-aid need
  and first-gen status (verified: dropped-out avg term-1 GPA **1.99** vs **2.51**;
  attendance **76** vs **84**; first-gen **59%** vs **21%**).
- **Two "weak" professors** run low-quality sections → lower grades, more
  withdrawals, and the most negative reviews.
- **Review sentiment tracks grades**: A/B **+0.55** → C **+0.11** → D/F **−0.29**
  (recommend rate 95% → 53% → 14%).

## Run it (recreates the objects in `appdb`)

The demo SQL server is **Entra-only** (no password), so use **go-sqlcmd** with an
`az login` session (`winget install Microsoft.Sqlcmd`). On Windows arm64 this is the
only client that works — `Invoke-Sqlcmd` and `pyodbc`/ODBC 17 fail with an
arch mismatch.

```powershell
$sqlcmd = "C:\Program Files\sqlcmd\sqlcmd.exe"
$srv = "sql-studemo-yltzci2mbevla.database.windows.net"   # your SQL server FQDN
$db  = "appdb"

# 0. (once) regenerate the seed if you changed the generator
python generate_seed.py

# 1. drop + recreate schema
& $sqlcmd -S $srv -d $db --authentication-method ActiveDirectoryAzCli -i "sql\01_schema.sql"

# 2. load the seed data
& $sqlcmd -S $srv -d $db --authentication-method ActiveDirectoryAzCli -i "sql\02_seed.sql"

# 3. explore
& $sqlcmd -S $srv -d $db --authentication-method ActiveDirectoryAzCli -i "sql\03_queries.sql"
```

> Needs a firewall rule for your client IP on the SQL server, and an
> `az login` to the subscription that owns it.

## Data volume (deterministic)

5 departments · 5 programs · 12 professors · 54 courses · 4 terms · 10 rooms ·
55 students · 153 sections · 408 enrollments · 136 term-status rows · 273 reviews.
Outcomes: **32 graduated · 22 withdrawn · 1 still active**.

## Status

This is a throwaway design sandbox. It is **not** part of `fy27_student_demos` and is
not committed there. If the design proves out, promote the schema + generator into
`seeding-scripts/` as the next-gen SQL seed.
