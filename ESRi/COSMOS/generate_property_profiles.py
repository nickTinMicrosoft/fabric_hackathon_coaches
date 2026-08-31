import json
from datetime import date, timedelta
from pathlib import Path


OUTPUT = Path(__file__).with_name("property_profiles.json")
NEIGHBORHOODS = [
    ("NORTH", "North Ridge"),
    ("LAKE", "Lake Junction"),
    ("PINE", "Pine Crossing"),
    ("COPPER", "Copper Works"),
    ("VALLEY", "Valley East"),
    ("CENTRAL", "Central Sudsberry"),
]
STREETS = [
    "Aurora",
    "Boreal",
    "Copper",
    "Granite",
    "Juniper",
    "Northern Light",
    "Pinecone",
    "Silver Birch",
]
CONDITIONS = ["fair", "good", "good", "average", "excellent"]


def property_class(number: int) -> str:
    if number % 17 == 0:
        return "AGR"
    if number % 11 == 0:
        return "COM"
    if number % 7 == 0:
        return "MUR"
    return "RES"


def building_type(class_code: str, number: int) -> str:
    if class_code == "AGR":
        return "farmResidence"
    if class_code == "COM":
        return "commercialBuilding"
    if class_code == "MUR":
        return "multiUnitResidence"
    return ["detachedResidence", "semiDetachedResidence", "townhouse"][number % 3]


def make_profile(number: int) -> dict:
    neighborhood_id, neighborhood_name = NEIGHBORHOODS[number % len(NEIGHBORHOODS)]
    class_code = property_class(number)
    floor_area = (
        180 + number % 140
        if class_code == "AGR"
        else 300 + number % 900
        if class_code == "COM"
        else 260 + number % 500
        if class_code == "MUR"
        else 85 + number % 190
    )
    assessed_value = round(
        floor_area
        * {"AGR": 980, "COM": 1850, "MUR": 2100, "RES": 2450}[class_code]
        * 1.0475,
        2,
    )
    inspection_date = date(2026, 1, 5) + timedelta(days=(number * 7) % 210)
    condition = CONDITIONS[number % len(CONDITIONS)]

    return {
        "id": f"SUD-{number:05d}",
        "parcelId": f"SUD-{number:05d}",
        "documentType": "propertyProfile",
        "synthetic": True,
        "jurisdiction": {
            "name": "Sudsberry",
            "countryCode": "CA",
            "regionCode": "ON",
            "currencyCode": "CAD",
            "areaUnit": "squareMetres",
        },
        "neighborhoodId": neighborhood_id,
        "neighborhoodName": neighborhood_name,
        "location": {
            "type": "Point",
            "coordinates": [
                round(-81.060000 + (((number - 1) // 20) * 0.004200), 6),
                round(46.430000 + ((number % 20) * 0.003100), 6),
            ],
        },
        "site": {
            "syntheticAddress": (
                f"{100 + number} {STREETS[number % len(STREETS)]} "
                f"{['Road', 'Avenue', 'Lane', 'Drive'][number % 4]}"
            ),
            "propertyClassCode": class_code,
            "zoningCode": {"AGR": "AG-1", "COM": "C-2", "MUR": "RM-2", "RES": "R-1"}[
                class_code
            ],
            "lotAreaSquareMetres": (
                12000 + number * 83
                if class_code == "AGR"
                else 900 + number * 17
                if class_code == "COM"
                else 420 + number * 9
            ),
        },
        "building": {
            "type": building_type(class_code, number),
            "yearBuilt": 1955 + number % 69,
            "floorAreaSquareMetres": floor_area,
            "storeys": 1 + number % (4 if class_code in {"COM", "MUR"} else 2),
            "condition": condition,
            "attributes": {
                "energyRetrofitObserved": number % 9 == 0,
                "accessoryStructureObserved": number % 13 == 0,
                "renovationObserved": number % 8 == 0,
            },
        },
        "currentAssessment": {
            "taxYear": 2026,
            "assessedValue": assessed_value,
            "confidenceScore": round(0.76 + ((number * 37) % 2200) / 10000, 4),
            "status": "certified",
        },
        "inspections": [
            {
                "inspectionId": f"INS-{number:05d}-01",
                "inspectionDate": inspection_date.isoformat(),
                "inspectionType": "exteriorReview" if number % 4 else "fieldReview",
                "condition": condition,
                "observations": [
                    "building condition reviewed",
                    "site characteristics confirmed",
                    (
                        "renovation follow-up recommended"
                        if number % 8 == 0
                        else "no immediate follow-up required"
                    ),
                ],
                "followUpRequired": number % 8 == 0,
            }
        ],
    }


def main() -> None:
    profiles = [make_profile(number) for number in range(1, 241)]
    OUTPUT.write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(profiles)} property profiles to {OUTPUT}")


if __name__ == "__main__":
    main()

