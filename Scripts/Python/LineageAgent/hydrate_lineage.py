# Fabric Notebook — Lineage & Catalog Metadata Hydrator
#
# This notebook calls the Microsoft Fabric REST APIs (Scanner + Workspace APIs)
# to extract metadata about all items in your tenant, then writes the results
# as Delta tables in your Lakehouse. A Fabric Data Agent can then query these
# tables to answer natural-language questions like:
#
#   - "When was data X last updated?"
#   - "Who owns the sales lakehouse?"
#   - "What items are in the marketing workspace?"
#   - "Show me all pipelines that were modified this week"
#   - "Who has access to workspace Y?"
#
# Setup:
#   1. Import this file into a Fabric notebook
#   2. Attach it to a Lakehouse (the metadata tables will be created there)
#   3. Run manually or schedule via a Fabric Pipeline
#
# Authentication:
#   Uses mssparkutils to get an access token from your Fabric identity.
#   No Service Principal or .env file needed when running inside Fabric.

# ============================================================
# CELL 1 — Configuration
# ============================================================

# Lakehouse table names (will be created/overwritten on each run)
TABLE_WORKSPACES = "lineage_workspaces"
TABLE_ITEMS = "lineage_items"
TABLE_REFRESH_HISTORY = "lineage_refresh_history"
TABLE_ACCESS = "lineage_workspace_access"
TABLE_LINEAGE = "lineage_item_dependencies"
TABLE_SCAN_LOG = "lineage_scan_log"

# Fabric API base URL
FABRIC_API_BASE = "https://api.fabric.microsoft.com/v1"
ADMIN_API_BASE = "https://api.fabric.microsoft.com/v1/admin"

# Scanner API settings
SCAN_DATASET_SCHEMA = True        # Include table/column metadata for semantic models
SCAN_DATASOURCE_DETAILS = True    # Include connection details

print("Configuration loaded.")

# ============================================================
# CELL 2 — Authentication Helper
# ============================================================

import requests
import json
from datetime import datetime, timezone

def get_fabric_token():
    """Get an access token for the Fabric API using the notebook's identity."""
    return mssparkutils.credentials.getToken("https://api.fabric.microsoft.com")

def fabric_get(url, params=None):
    """Make an authenticated GET request to the Fabric API."""
    headers = {
        "Authorization": f"Bearer {get_fabric_token()}",
        "Content-Type": "application/json",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fabric_post(url, body=None):
    """Make an authenticated POST request to the Fabric API."""
    headers = {
        "Authorization": f"Bearer {get_fabric_token()}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    resp.raise_for_status()
    return resp.json() if resp.content else {}

def paginate_get(url, key="value", params=None):
    """Handle paginated Fabric API responses."""
    all_items = []
    next_url = url
    while next_url:
        data = fabric_get(next_url, params=params)
        all_items.extend(data.get(key, []))
        next_url = data.get("continuationUri") or data.get("@odata.nextLink")
        params = None  # params only needed on first request
    return all_items

print("Auth helpers ready.")

# ============================================================
# CELL 3 — Fetch Workspaces
# ============================================================

from pyspark.sql.types import StructType, StructField, StringType, TimestampType

def fetch_workspaces():
    """Fetch all workspaces the caller has access to."""
    workspaces = paginate_get(f"{FABRIC_API_BASE}/workspaces")

    rows = []
    for ws in workspaces:
        rows.append({
            "workspace_id": ws.get("id", ""),
            "workspace_name": ws.get("displayName", ""),
            "description": ws.get("description", ""),
            "type": ws.get("type", ""),
            "state": ws.get("state", ""),
            "capacity_id": ws.get("capacityId", ""),
            "scanned_at": datetime.now(timezone.utc).isoformat(),
        })

    print(f"Fetched {len(rows)} workspaces.")
    return rows

workspace_rows = fetch_workspaces()

# ============================================================
# CELL 4 — Fetch Items per Workspace
# ============================================================

def fetch_items(workspaces):
    """Fetch all items (lakehouses, warehouses, notebooks, etc.) for each workspace."""
    all_items = []

    for ws in workspaces:
        ws_id = ws["workspace_id"]
        ws_name = ws["workspace_name"]

        try:
            items = paginate_get(f"{FABRIC_API_BASE}/workspaces/{ws_id}/items")
            for item in items:
                all_items.append({
                    "workspace_id": ws_id,
                    "workspace_name": ws_name,
                    "item_id": item.get("id", ""),
                    "item_name": item.get("displayName", ""),
                    "item_type": item.get("type", ""),
                    "description": item.get("description", ""),
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                })
        except Exception as e:
            print(f"  Warning: could not fetch items for workspace '{ws_name}': {e}")

    print(f"Fetched {len(all_items)} items across {len(workspaces)} workspaces.")
    return all_items

item_rows = fetch_items(workspace_rows)

# ============================================================
# CELL 5 — Fetch Workspace Role Assignments (Access)
# ============================================================

def fetch_workspace_access(workspaces):
    """Fetch role assignments (who has access) for each workspace."""
    all_access = []

    for ws in workspaces:
        ws_id = ws["workspace_id"]
        ws_name = ws["workspace_name"]

        try:
            assignments = paginate_get(
                f"{FABRIC_API_BASE}/workspaces/{ws_id}/roleAssignments"
            )
            for ra in assignments:
                principal = ra.get("principal", {})
                all_access.append({
                    "workspace_id": ws_id,
                    "workspace_name": ws_name,
                    "principal_id": principal.get("id", ""),
                    "principal_name": principal.get("displayName", ""),
                    "principal_type": principal.get("type", ""),
                    "role": ra.get("role", ""),
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                })
        except Exception as e:
            print(f"  Warning: could not fetch access for workspace '{ws_name}': {e}")

    print(f"Fetched {len(all_access)} role assignments.")
    return all_access

access_rows = fetch_workspace_access(workspace_rows)

# ============================================================
# CELL 6 — Scanner API (Rich Metadata + Lineage)
# ============================================================

import time

def run_scanner(workspaces):
    """
    Use the Admin Scanner APIs to extract rich metadata:
    - Item details (owners, sensitivity labels, endorsement)
    - Dataset schemas (tables, columns, measures, DAX)
    - Data source connection details
    - Item-to-item dependencies (lineage)
    """
    ws_ids = [ws["workspace_id"] for ws in workspaces]

    # Step 1: Trigger scan
    print("Triggering metadata scan...")
    scan_body = {
        "workspaces": ws_ids,
        "datasetSchema": SCAN_DATASET_SCHEMA,
        "datasourceDetails": SCAN_DATASOURCE_DETAILS,
    }

    try:
        scan_response = fabric_post(f"{ADMIN_API_BASE}/workspaces/getInfo", body=scan_body)
    except requests.exceptions.HTTPError as e:
        print(f"Scanner API error: {e}")
        print("Note: Scanner APIs require Fabric Admin permissions.")
        return [], []

    scan_id = scan_response.get("id")
    if not scan_id:
        print("No scan ID returned. Check admin permissions.")
        return [], []

    # Step 2: Poll for completion
    print(f"Scan ID: {scan_id} — waiting for completion...")
    for _ in range(30):
        status = fabric_get(f"{ADMIN_API_BASE}/workspaces/scanStatus/{scan_id}")
        if status.get("status") == "Succeeded":
            print("Scan completed.")
            break
        time.sleep(5)
    else:
        print("Scan timed out after 150 seconds.")
        return [], []

    # Step 3: Get results
    result = fabric_get(f"{ADMIN_API_BASE}/workspaces/scanResult/{scan_id}")

    refresh_rows = []
    dependency_rows = []

    for ws in result.get("workspaces", []):
        ws_id = ws.get("id", "")
        ws_name = ws.get("name", "")

        # Extract datasets (semantic models) with refresh info
        for dataset in ws.get("datasets", []):
            refresh_rows.append({
                "workspace_id": ws_id,
                "workspace_name": ws_name,
                "item_id": dataset.get("id", ""),
                "item_name": dataset.get("name", ""),
                "item_type": "SemanticModel",
                "configured_by": dataset.get("configuredBy", ""),
                "is_refreshable": str(dataset.get("isRefreshable", "")),
                "last_refresh_time": dataset.get("refreshedDate", ""),
                "sensitivity_label": dataset.get("sensitivityLabel", {}).get("labelId", ""),
                "endorsement": dataset.get("endorsementDetails", {}).get("endorsement", ""),
                "scanned_at": datetime.now(timezone.utc).isoformat(),
            })

        # Extract other item types (reports, dashboards, dataflows, etc.)
        for item_type_key in ["reports", "dashboards", "dataflows", "datamarts"]:
            for item in ws.get(item_type_key, []):
                refresh_rows.append({
                    "workspace_id": ws_id,
                    "workspace_name": ws_name,
                    "item_id": item.get("id", ""),
                    "item_name": item.get("name", ""),
                    "item_type": item_type_key.rstrip("s").title(),
                    "configured_by": item.get("configuredBy", item.get("createdBy", "")),
                    "is_refreshable": "",
                    "last_refresh_time": item.get("modifiedDateTime", item.get("createdDateTime", "")),
                    "sensitivity_label": item.get("sensitivityLabel", {}).get("labelId", ""),
                    "endorsement": item.get("endorsementDetails", {}).get("endorsement", ""),
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                })

        # Extract upstream dependencies (lineage)
        for dataset in ws.get("datasets", []):
            for upstream in dataset.get("upstreamDatasets", []):
                dependency_rows.append({
                    "workspace_id": ws_id,
                    "workspace_name": ws_name,
                    "item_id": dataset.get("id", ""),
                    "item_name": dataset.get("name", ""),
                    "item_type": "SemanticModel",
                    "depends_on_id": upstream.get("targetDatasetId", ""),
                    "dependency_type": "upstreamDataset",
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                })

            for source in dataset.get("datasourceUsages", []):
                dependency_rows.append({
                    "workspace_id": ws_id,
                    "workspace_name": ws_name,
                    "item_id": dataset.get("id", ""),
                    "item_name": dataset.get("name", ""),
                    "item_type": "SemanticModel",
                    "depends_on_id": source.get("datasourceInstanceId", ""),
                    "dependency_type": "datasource",
                    "scanned_at": datetime.now(timezone.utc).isoformat(),
                })

    print(f"Scanner extracted {len(refresh_rows)} item details, {len(dependency_rows)} dependencies.")
    return refresh_rows, dependency_rows

refresh_rows, dependency_rows = run_scanner(workspace_rows)

# ============================================================
# CELL 7 — Write All Tables to Lakehouse
# ============================================================

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

def write_to_lakehouse(rows, table_name):
    """Write a list of dicts as a Delta table in the attached Lakehouse."""
    if not rows:
        print(f"  Skipping {table_name} — no data.")
        return

    df = spark.createDataFrame(rows)
    df.write.mode("overwrite").format("delta").saveAsTable(table_name)
    print(f"  ✅ {table_name}: {len(rows)} rows written.")

print("Writing tables to Lakehouse...")
write_to_lakehouse(workspace_rows, TABLE_WORKSPACES)
write_to_lakehouse(item_rows, TABLE_ITEMS)
write_to_lakehouse(access_rows, TABLE_ACCESS)
write_to_lakehouse(refresh_rows, TABLE_REFRESH_HISTORY)
write_to_lakehouse(dependency_rows, TABLE_LINEAGE)

# Write a scan log entry
scan_log = [{
    "scan_timestamp": datetime.now(timezone.utc).isoformat(),
    "workspaces_scanned": len(workspace_rows),
    "items_scanned": len(item_rows),
    "access_entries": len(access_rows),
    "refresh_entries": len(refresh_rows),
    "dependency_entries": len(dependency_rows),
}]
write_to_lakehouse(scan_log, TABLE_SCAN_LOG)

print("\n🎉 Hydration complete! Tables are ready for your Data Agent.")

# ============================================================
# CELL 8 — Sample Queries (for testing / Data Agent reference)
# ============================================================

# Uncomment any of these to verify the data:

# -- "When was the sales model last refreshed?"
# spark.sql("""
#     SELECT item_name, last_refresh_time, configured_by
#     FROM lineage_refresh_history
#     WHERE LOWER(item_name) LIKE '%sales%'
#     ORDER BY last_refresh_time DESC
# """).show(truncate=False)

# -- "Who has access to the marketing workspace?"
# spark.sql("""
#     SELECT principal_name, principal_type, role
#     FROM lineage_workspace_access
#     WHERE LOWER(workspace_name) LIKE '%marketing%'
# """).show(truncate=False)

# -- "What items are in the analytics workspace?"
# spark.sql("""
#     SELECT item_name, item_type
#     FROM lineage_items
#     WHERE LOWER(workspace_name) LIKE '%analytics%'
#     ORDER BY item_type, item_name
# """).show(truncate=False)

# -- "Show all items modified in the last 7 days"
# spark.sql("""
#     SELECT item_name, item_type, workspace_name, last_refresh_time
#     FROM lineage_refresh_history
#     WHERE last_refresh_time >= date_sub(current_date(), 7)
#     ORDER BY last_refresh_time DESC
# """).show(truncate=False)

# -- "What are the upstream dependencies for model X?"
# spark.sql("""
#     SELECT item_name, depends_on_id, dependency_type
#     FROM lineage_item_dependencies
#     WHERE LOWER(item_name) LIKE '%model_name%'
# """).show(truncate=False)

print("Sample queries available in Cell 8 (uncomment to run).")
