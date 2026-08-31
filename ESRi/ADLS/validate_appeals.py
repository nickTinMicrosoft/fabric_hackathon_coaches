import json
from pathlib import Path

import duckdb


DIRECTORY = Path(__file__).parent
JSON_FILE = DIRECTORY / "assessment_appeals.json"
PARQUET_FILE = DIRECTORY / "assessment_appeals.parquet"
PROHIBITED_FIELDS = {"name", "email", "phone", "owner", "appellantName"}
REQUIRED_FIELDS = {
    "appealId",
    "parcelId",
    "neighborhoodId",
    "taxYear",
    "narrative",
    "reasonCode",
    "groundTruthSentiment",
    "synthetic",
}


def main() -> None:
    json_records = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    with duckdb.connect() as connection:
        parquet_count = connection.execute(
            "SELECT COUNT(*) FROM read_parquet(?)", [str(PARQUET_FILE)]
        ).fetchone()[0]
        parquet_fields = {
            row[0]
            for row in connection.execute(
                "DESCRIBE SELECT * FROM read_parquet(?)", [str(PARQUET_FILE)]
            ).fetchall()
        }

    if len(json_records) != 300 or parquet_count != 300:
        raise RuntimeError("JSON and Parquet must each contain 300 records.")
    if not REQUIRED_FIELDS.issubset(json_records[0]) or not REQUIRED_FIELDS.issubset(
        parquet_fields
    ):
        raise RuntimeError("A required appeal field is missing.")
    if PROHIBITED_FIELDS.intersection(json_records[0]) or PROHIBITED_FIELDS.intersection(
        parquet_fields
    ):
        raise RuntimeError("A prohibited personal-information field is present.")
    if any(not record["synthetic"] or not record["narrative"] for record in json_records):
        raise RuntimeError("Every appeal must be synthetic and contain a narrative.")

    sentiments = {record["groundTruthSentiment"] for record in json_records}
    if sentiments != {"positive", "neutral", "negative"}:
        raise RuntimeError(f"Unexpected sentiment coverage: {sentiments}")

    print(
        f"PASS: {len(json_records)} matching synthetic appeals with "
        f"{len(sentiments)} sentiment classes."
    )


if __name__ == "__main__":
    main()
