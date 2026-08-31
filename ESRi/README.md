# Sudsberry Property Assessment Data Platform

This folder contains a synthetic property-assessment data platform for the
fictional municipality of Sudsberry, Ontario. It demonstrates how operational
assessment records, flexible field-inspection documents, and appeal narratives
can be combined in Microsoft Fabric without using real people, addresses,
parcels, or tax records.

All values are fabricated for technical demonstrations. The tax calculations
and assessment classifications are not representations of Ontario law and must
not be used for actual valuation or taxation.

## Use cases

### 1. Property valuation and tax roll

Azure SQL Database stores the relational system of record:

- jurisdictions, neighbourhoods, and property classes
- synthetic parcels and building characteristics
- assessed land and improvement values by tax year
- comparable sales
- configurable tax rates
- an analytical tax-roll view with estimated taxes

This workload supports valuation trends, comparable-sales analysis,
assessment-to-sale ratios, and tax estimates.

### 2. Property and inspection profiles

Azure Cosmos DB for NoSQL stores denormalized property profiles containing:

- GeoJSON point locations
- flexible residential, commercial, and agricultural attributes
- current valuation summaries
- recent inspection observations
- condition and follow-up indicators

The document model supports field applications and property types whose
inspection attributes evolve independently.

### 3. Assessment appeal intelligence

Azure Data Lake Storage Gen2 stores the same synthetic appeal dataset in JSON
and Parquet. Appeal narratives contain controlled combinations of positive,
neutral, and negative language suitable for:

- sentiment analysis
- appeal-reason classification
- summarization
- urgency and follow-up detection
- recurring-theme analysis

The files are intended to be exposed to OneLake through an ADLS Gen2 shortcut
and enriched with Fabric AI functions.

## Architecture

```text
                           +----------------------+
                           | Microsoft Fabric     |
                           |                      |
Azure SQL Database ------->| Mirroring / pipeline |
  assessment system        |                      |
                           | Lakehouse / Warehouse|----> Semantic model
Azure Cosmos DB ---------->| Cosmos mirroring     |----> Power BI
  property profiles        |                      |----> Data agent
                           | OneLake shortcut     |
ADLS Gen2 ---------------->| AI enrichment        |
  appeal JSON + Parquet    | notebooks / AI funcs |
                           +----------------------+
```

### Azure resources

`deploy.ps1` provisions the following resources in `rg_esriHack`:

| Service | Configuration | Purpose |
|---|---|---|
| Azure SQL Database | Basic tier, Entra-only authentication | Relational assessment, sale, and tax-roll data |
| Azure Cosmos DB for NoSQL | 400 RU/s, session consistency | Property and inspection documents |
| ADLS Gen2 | StorageV2, hierarchical namespace, Standard LRS | Appeal JSON and Parquet files |

Resource names begin with `sudsberry` and receive a deterministic suffix based
on the active Azure subscription. SQL and storage use Canada Central by
default. Cosmos DB uses East US 2 by default because both Canadian Cosmos
regions can be restricted for workshop subscriptions. Only synthetic,
nonpersonal data is placed there, and `-CosmosLocation` can select a Canadian
region when capacity is available. The deployment requires TLS 1.2 or later,
disables public blob access, and does not write credentials to the repository.
Azure SQL permits Azure-service network connections but accepts only Entra
authentication.

### Data relationships

`parcelId` is the shared synthetic business key:

- SQL uses it for parcels, assessments, sales, and tax calculations.
- Cosmos documents use it as the document ID and include `neighborhoodId` as
  the logical partition key.
- Appeal files use it to associate narratives with assessed properties.

The model also carries explicit `countryCode`, `regionCode`, `currencyCode`,
and measurement-unit fields so another jurisdiction can be represented without
redesigning the datasets.

## Folder structure

```text
SQL/
  property_assessment.sql   Schema and deterministic relational seed
  validate.sql              SQL assertions and analytical smoke tests
COSMOS/
  generate_property_profiles.py
  seed_cosmos.py
  validate_cosmos.py
  property_profiles.json
  requirements.txt
ADLS/
  generate_appeals.py
  validate_appeals.py
  assessment_appeals.json
  assessment_appeals.parquet
  requirements.txt
deploy.ps1                  Azure resource provisioning
seed.ps1                    Data generation and cloud loading
validate.ps1                End-to-end validation
```

## Prerequisites

- Azure CLI authenticated with `az login`
- permission to create resource groups and role assignments
- Python 3.10 or later
- `sqlcmd` with the `ActiveDirectoryAzCli` authentication method

Install the Python dependencies:

```powershell
python -m pip install -r .\COSMOS\requirements.txt -r .\ADLS\requirements.txt
```

## Deploy, seed, and validate

Run these commands from this folder:

```powershell
.\deploy.ps1
.\seed.ps1
.\validate.ps1
```

The scripts accept optional `-ResourceGroup` and `-SubscriptionId` parameters.
The deployment also accepts `-Location` and `-CosmosLocation`. The deployment
and seeds are idempotent, so the commands can be rerun after an interrupted
session.

## Fabric integration

1. Create a Fabric workspace and Lakehouse.
2. Create an ADLS Gen2 shortcut to the `assessment-data/appeals` path.
3. Mirror the Azure SQL database and Cosmos DB database, or ingest them with
   Fabric pipelines when mirroring is not available.
4. Apply AI enrichment to `narrative` in the appeal dataset.
5. Join enriched appeals to property and assessment data using `parcelId`.
6. Build a semantic model for assessment equity, appeal volume, sentiment,
   neighbourhood trends, and estimated tax impact.

## Privacy and safety

- No names, email addresses, telephone numbers, or owner details are present.
- Addresses, parcel identifiers, coordinates, values, and narratives are
  synthetic.
- Coordinates form a fabricated map pattern and do not represent real parcel
  boundaries.
- Ground-truth sentiment is included only to evaluate enrichment quality.
- Generated tax estimates are illustrative and not legally authoritative.
