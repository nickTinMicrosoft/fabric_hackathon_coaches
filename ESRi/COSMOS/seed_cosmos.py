import argparse
import json
import time
from pathlib import Path

from azure.cosmos import CosmosClient
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
from azure.identity import AzureCliCredential


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed synthetic property profiles.")
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--container", required=True)
    parser.add_argument("--file", required=True, type=Path)
    return parser.parse_args()


def connect_with_retry(endpoint: str) -> CosmosClient:
    credential = AzureCliCredential()
    for attempt in range(1, 13):
        try:
            client = CosmosClient(endpoint, credential=credential)
            list(client.list_databases(max_item_count=1))
            return client
        except (ClientAuthenticationError, HttpResponseError) as exc:
            if attempt == 12:
                raise
            print(f"Waiting for Cosmos data-plane access ({attempt}/12): {exc}")
            time.sleep(10)
    raise RuntimeError("Cosmos DB connection retry loop ended unexpectedly.")


def main() -> None:
    args = parse_args()
    documents = json.loads(args.file.read_text(encoding="utf-8"))
    client = connect_with_retry(args.endpoint)
    container = client.get_database_client(args.database).get_container_client(args.container)

    for document in documents:
        container.upsert_item(document)

    count = list(
        container.query_items(
            "SELECT VALUE COUNT(1) FROM c",
            enable_cross_partition_query=True,
        )
    )[0]
    if count != len(documents):
        raise RuntimeError(f"Expected {len(documents)} documents, found {count}.")
    print(f"Seeded and verified {count} property profiles.")


if __name__ == "__main__":
    main()

