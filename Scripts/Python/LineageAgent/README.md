# Lineage Agent — Fabric Catalog & Lineage Hydrator

Hydrates a Fabric Lakehouse with metadata from the Fabric REST APIs so a **Data Agent** can answer natural-language governance questions.

---

## What It Does

This notebook calls Fabric APIs to extract and store:

| Lakehouse Table | Source API | What It Contains |
|-----------------|-----------|------------------|
| `lineage_workspaces` | Workspaces API | All workspaces — name, type, state, capacity |
| `lineage_items` | Items API | Every item (lakehouse, warehouse, notebook, report, etc.) per workspace |
| `lineage_workspace_access` | Role Assignments API | Who has access to each workspace and their role |
| `lineage_refresh_history` | Scanner API | Item owners, last refresh time, sensitivity labels, endorsement |
| `lineage_item_dependencies` | Scanner API | Upstream dataset and datasource dependencies (lineage) |
| `lineage_scan_log` | — | Audit log of each hydration run |

---

## Questions Your Data Agent Can Answer

Once hydrated, point a Fabric Data Agent at these tables to answer:

- *"When was the sales dataset last refreshed?"*
- *"Who has access to the marketing workspace?"*
- *"What items are in the analytics workspace?"*
- *"Show me all semantic models modified this week"*
- *"What are the upstream dependencies for the revenue model?"*
- *"Which workspaces have no sensitivity labels applied?"*
- *"List all items configured by user X"*

---

## Setup

### Prerequisites

- **Fabric capacity** (F2 or higher)
- **Fabric Admin role** (required for Scanner APIs — workspace and item APIs work for any user)
- A **Lakehouse** attached to the notebook

### Steps

1. Copy `hydrate_lineage.py` into a new Fabric Notebook
2. Attach the notebook to your target Lakehouse
3. Run all cells
4. Verify tables appear in the Lakehouse SQL endpoint

### Scheduling

To keep metadata fresh, schedule the notebook in a **Fabric Pipeline**:

1. Create a new Pipeline in your workspace
2. Add a **Notebook activity** pointing to this notebook
3. Set a schedule trigger (e.g., every 6 hours or daily)

---

## Architecture

```
Fabric Pipeline (scheduled)
  └── Notebook: hydrate_lineage
        ├── GET  /workspaces                          → lineage_workspaces
        ├── GET  /workspaces/{id}/items               → lineage_items
        ├── GET  /workspaces/{id}/roleAssignments     → lineage_workspace_access
        ├── POST /admin/workspaces/getInfo (Scanner)  → lineage_refresh_history
        │                                             → lineage_item_dependencies
        └── Writes Delta tables to attached Lakehouse

Fabric Data Agent
  └── Queries Lakehouse tables via SQL
  └── Returns natural-language answers
```

---

## Tables Schema

### `lineage_workspaces`
| Column | Description |
|--------|-------------|
| `workspace_id` | Workspace GUID |
| `workspace_name` | Display name |
| `description` | Workspace description |
| `type` | Workspace type |
| `state` | Active, Deleted, etc. |
| `capacity_id` | Assigned capacity |
| `scanned_at` | Timestamp of this scan |

### `lineage_items`
| Column | Description |
|--------|-------------|
| `workspace_id` / `workspace_name` | Parent workspace |
| `item_id` | Item GUID |
| `item_name` | Display name |
| `item_type` | Lakehouse, Warehouse, Report, Notebook, etc. |
| `description` | Item description |
| `scanned_at` | Timestamp of this scan |

### `lineage_workspace_access`
| Column | Description |
|--------|-------------|
| `workspace_id` / `workspace_name` | Workspace |
| `principal_id` | User/group/SP GUID |
| `principal_name` | Display name |
| `principal_type` | User, Group, ServicePrincipal |
| `role` | Admin, Member, Contributor, Viewer |
| `scanned_at` | Timestamp of this scan |

### `lineage_refresh_history`
| Column | Description |
|--------|-------------|
| `item_id` / `item_name` | Item details |
| `item_type` | SemanticModel, Report, Dashboard, etc. |
| `configured_by` | Who last configured/modified |
| `is_refreshable` | Whether the item supports refresh |
| `last_refresh_time` | Last refresh or modification timestamp |
| `sensitivity_label` | Applied sensitivity label ID |
| `endorsement` | Promoted, Certified, or empty |
| `scanned_at` | Timestamp of this scan |

### `lineage_item_dependencies`
| Column | Description |
|--------|-------------|
| `item_id` / `item_name` | Source item |
| `depends_on_id` | Upstream item or datasource ID |
| `dependency_type` | upstreamDataset or datasource |
| `scanned_at` | Timestamp of this scan |

---

## Notes

- **Scanner APIs** require Fabric Admin permissions. If you don't have admin access, the notebook will still hydrate workspaces, items, and access tables — just skip the scanner cells.
- **No .env file needed** — authentication uses `mssparkutils.credentials.getToken()` built into Fabric notebooks.
- Tables are **overwritten** on each run (full snapshot). For incremental history, change the write mode to `append`.

---

[← Back to Python README](../README.md)
