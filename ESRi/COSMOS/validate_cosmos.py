import argparse

from azure.cosmos import CosmosClient
from azure.identity import AzureCliCredential


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate property profiles.")
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--container", required=True)
    return parser.parse_args()


def scalar(container, query: str) -> int:
    return list(
        container.query_items(query, enable_cross_partition_query=True)
    )[0]


def main() -> None:
    args = parse_args()
    client = CosmosClient(args.endpoint, credential=AzureCliCredential())
    container = client.get_database_client(args.database).get_container_client(args.container)

    total = scalar(container, "SELECT VALUE COUNT(1) FROM c")
    synthetic = scalar(container, "SELECT VALUE COUNT(1) FROM c WHERE c.synthetic = true")
    geojson = scalar(
        container,
        "SELECT VALUE COUNT(1) FROM c WHERE c.location.type = 'Point'",
    )
    follow_up = scalar(
        container,
        "SELECT VALUE COUNT(1) FROM c JOIN i IN c.inspections "
        "WHERE i.followUpRequired = true",
    )

    if total != 240 or synthetic != total or geojson != total or follow_up == 0:
        raise RuntimeError(
            f"Validation failed: total={total}, synthetic={synthetic}, "
            f"geojson={geojson}, followUp={follow_up}"
        )
    print(
        f"PASS: {total} synthetic profiles, {geojson} GeoJSON locations, "
        f"{follow_up} follow-up inspections."
    )


if __name__ == "__main__":
    main()

