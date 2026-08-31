import json
from datetime import date, timedelta
from pathlib import Path

import duckdb


DIRECTORY = Path(__file__).parent
JSON_OUTPUT = DIRECTORY / "assessment_appeals.json"
PARQUET_OUTPUT = DIRECTORY / "assessment_appeals.parquet"
NEIGHBORHOODS = ["NORTH", "LAKE", "PINE", "COPPER", "VALLEY", "CENTRAL"]
SCENARIOS = [
    {
        "reasonCode": "COMPARABLE_SALES",
        "sentiment": "negative",
        "narrative": (
            "The assessed value seems much higher than recent comparable sales "
            "in the neighbourhood. Please review the selected comparables and "
            "the adjustment for building condition."
        ),
    },
    {
        "reasonCode": "PROPERTY_CONDITION",
        "sentiment": "negative",
        "narrative": (
            "The current assessment does not appear to reflect the roof damage "
            "and unfinished interior repairs documented during the inspection. "
            "A prompt condition review is requested."
        ),
    },
    {
        "reasonCode": "DATA_CORRECTION",
        "sentiment": "neutral",
        "narrative": (
            "The property profile lists an additional finished level, but the "
            "lower level is unfinished storage. Please verify the recorded floor "
            "area and update the assessment record."
        ),
    },
    {
        "reasonCode": "CLASSIFICATION",
        "sentiment": "neutral",
        "narrative": (
            "The parcel is currently shown in a commercial class even though "
            "the permitted use changed. Supporting classification documents are "
            "available for assessor review."
        ),
    },
    {
        "reasonCode": "RENOVATION_TIMING",
        "sentiment": "negative",
        "narrative": (
            "The valuation includes renovation work that was not complete on the "
            "valuation date. The timing has created a substantial increase and "
            "requires correction before the next tax calculation."
        ),
    },
    {
        "reasonCode": "INFORMATION_REQUEST",
        "sentiment": "positive",
        "narrative": (
            "The online property summary was clear and helpful. Please provide "
            "the comparable-sales worksheet so the valuation can be reviewed "
            "before deciding whether further action is needed."
        ),
    },
]


def make_record(number: int) -> dict:
    scenario = SCENARIOS[number % len(SCENARIOS)]
    submitted = date(2026, 2, 1) + timedelta(days=(number * 3) % 180)
    status = ["submitted", "underReview", "resolved"][number % 3]
    resolved = submitted + timedelta(days=14 + number % 35) if status == "resolved" else None

    return {
        "appealId": f"APL-{number:05d}",
        "parcelId": f"SUD-{((number * 7) % 240) + 1:05d}",
        "neighborhoodId": NEIGHBORHOODS[number % len(NEIGHBORHOODS)],
        "taxYear": 2026,
        "submittedDate": submitted.isoformat(),
        "reasonCode": scenario["reasonCode"],
        "narrative": scenario["narrative"],
        "requestedAdjustmentPct": round(3.0 + ((number * 7) % 28) * 0.5, 2),
        "status": status,
        "outcome": (
            ["confirmed", "adjusted", "partiallyAdjusted"][number % 3]
            if status == "resolved"
            else None
        ),
        "resolvedDate": resolved.isoformat() if resolved else None,
        "groundTruthSentiment": scenario["sentiment"],
        "currencyCode": "CAD",
        "countryCode": "CA",
        "regionCode": "ON",
        "synthetic": True,
    }


def main() -> None:
    records = [make_record(number) for number in range(1, 301)]
    JSON_OUTPUT.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    json_path = str(JSON_OUTPUT).replace("\\", "/")
    parquet_path = str(PARQUET_OUTPUT).replace("\\", "/").replace("'", "''")
    with duckdb.connect() as connection:
        connection.execute(
            "CREATE TABLE appeals AS "
            "SELECT * FROM read_json_auto(?, format = 'array')",
            [json_path],
        )
        connection.execute(
            f"COPY appeals TO '{parquet_path}' "
            "(FORMAT PARQUET, COMPRESSION ZSTD)"
        )
    print(f"Wrote {len(records)} appeals to JSON and Parquet.")


if __name__ == "__main__":
    main()
