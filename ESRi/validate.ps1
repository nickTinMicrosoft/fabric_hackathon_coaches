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
$cosmosAccount = "sudsberrycosmos$suffix"
$storageAccount = "sudsberrydata$suffix"

Write-Host "Validating generated appeal files..."
python "$root\ADLS\validate_appeals.py"
if ($LASTEXITCODE -ne 0) { throw "Local appeal validation failed." }

Write-Host "Validating Azure SQL Database..."
sqlcmd `
    -S "$sqlServer.database.windows.net" `
    -d "property-assessment" `
    --authentication-method ActiveDirectoryAzCli `
    -N true `
    -b `
    -i "$root\SQL\validate.sql"
if ($LASTEXITCODE -ne 0) { throw "Azure SQL validation failed." }

Write-Host "Validating Cosmos DB..."
python "$root\COSMOS\validate_cosmos.py" `
    --endpoint "https://$cosmosAccount.documents.azure.com:443/" `
    --database "property-profiles" `
    --container "properties"
if ($LASTEXITCODE -ne 0) { throw "Cosmos DB validation failed." }

Write-Host "Validating ADLS Gen2 uploads..."
$storageKey = az storage account keys list `
    --resource-group $ResourceGroup `
    --account-name $storageAccount `
    --query "[0].value" `
    --output tsv
if ($LASTEXITCODE -ne 0) { throw "Unable to obtain the storage account key." }

$remoteFiles = az storage fs file list `
    --account-name $storageAccount `
    --account-key $storageKey `
    --file-system "assessment-data" `
    --path "appeals" `
    --query "[].{name:name,size:contentLength}" `
    --output json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw "Unable to list ADLS files." }

$expectedFiles = @("appeals/assessment_appeals.json", "appeals/assessment_appeals.parquet")
foreach ($expected in $expectedFiles) {
    $match = $remoteFiles | Where-Object { $_.name -eq $expected -and $_.size -gt 0 }
    if (-not $match) { throw "Missing or empty ADLS file: $expected" }
}

Write-Host "Validation complete: SQL, Cosmos DB, and ADLS Gen2 passed."

