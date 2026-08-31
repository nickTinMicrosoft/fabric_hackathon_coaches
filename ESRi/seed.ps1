[CmdletBinding()]
param(
    [string]$ResourceGroup = "rg_esriHack",
    [string]$SubscriptionId
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$root = $PSScriptRoot

if ($SubscriptionId) {
    az account set --subscription $SubscriptionId
    if ($LASTEXITCODE -ne 0) { throw "Unable to select subscription." }
}

$account = az account show --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw "Azure CLI authentication is required." }

$suffix = ($account.id -replace "-", "").Substring(0, 8).ToLowerInvariant()
$sqlServer = "sudsberrysql$suffix"
$sqlDatabase = "property-assessment"
$cosmosAccount = "sudsberrycosmos$suffix"
$storageAccount = "sudsberrydata$suffix"
$fileSystem = "assessment-data"

Write-Host "Generating deterministic synthetic datasets..."
python "$root\COSMOS\generate_property_profiles.py"
if ($LASTEXITCODE -ne 0) { throw "Cosmos dataset generation failed." }

python "$root\ADLS\generate_appeals.py"
if ($LASTEXITCODE -ne 0) { throw "Appeal dataset generation failed." }

Write-Host "Seeding Azure SQL Database..."
sqlcmd `
    -S "$sqlServer.database.windows.net" `
    -d $sqlDatabase `
    --authentication-method ActiveDirectoryAzCli `
    -N true `
    -b `
    -i "$root\SQL\property_assessment.sql"
if ($LASTEXITCODE -ne 0) { throw "Azure SQL seed failed." }

Write-Host "Seeding Cosmos DB..."
python "$root\COSMOS\seed_cosmos.py" `
    --endpoint "https://$cosmosAccount.documents.azure.com:443/" `
    --database "property-profiles" `
    --container "properties" `
    --file "$root\COSMOS\property_profiles.json"
if ($LASTEXITCODE -ne 0) { throw "Cosmos DB seed failed." }

Write-Host "Uploading appeal files to ADLS Gen2..."
$storageKey = az storage account keys list `
    --resource-group $ResourceGroup `
    --account-name $storageAccount `
    --query "[0].value" `
    --output tsv
if ($LASTEXITCODE -ne 0) { throw "Unable to obtain the storage account key." }

foreach ($file in @("assessment_appeals.json", "assessment_appeals.parquet")) {
    az storage fs file upload `
        --account-name $storageAccount `
        --account-key $storageKey `
        --file-system $fileSystem `
        --path "appeals/$file" `
        --source "$root\ADLS\$file" `
        --overwrite true `
        --output none
    if ($LASTEXITCODE -ne 0) { throw "ADLS upload failed for $file." }
}

Write-Host "All three services have been seeded."

