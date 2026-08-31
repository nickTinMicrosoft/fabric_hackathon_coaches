[CmdletBinding()]
param(
    [string]$ResourceGroup = "rg_esriHack",
    [string]$Location = "canadacentral",
    [string]$CosmosLocation = "eastus2",
    [string]$SubscriptionId
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function Invoke-Az {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)

    & az @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Azure CLI command failed: az $($Arguments -join ' ')"
    }
}

function Test-Az {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments)

    & az @Arguments --output none 2>$null
    return $LASTEXITCODE -eq 0
}

if ($SubscriptionId) {
    Invoke-Az account set --subscription $SubscriptionId
}

$account = Invoke-Az account show --output json | ConvertFrom-Json
$currentUser = Invoke-Az ad signed-in-user show --output json | ConvertFrom-Json
$suffix = ($account.id -replace "-", "").Substring(0, 8).ToLowerInvariant()

$sqlServer = "sudsberrysql$suffix"
$sqlDatabase = "property-assessment"
$cosmosAccount = "sudsberrycosmos$suffix"
$cosmosDatabase = "property-profiles"
$cosmosContainer = "properties"
$storageAccount = "sudsberrydata$suffix"
$fileSystem = "assessment-data"

Write-Host "Creating resource group $ResourceGroup in $Location..."
Invoke-Az group create --name $ResourceGroup --location $Location --tags workload=sudsberry-assessment environment=hackathon --output none

if (-not (Test-Az sql server show --resource-group $ResourceGroup --name $sqlServer)) {
    Write-Host "Creating Entra-only Azure SQL logical server..."
    Invoke-Az sql server create `
        --resource-group $ResourceGroup `
        --name $sqlServer `
        --location $Location `
        --enable-ad-only-auth `
        --external-admin-principal-type User `
        --external-admin-name $currentUser.userPrincipalName `
        --external-admin-sid $currentUser.id `
        --enable-public-network true `
        --output none
}

if (-not (Test-Az sql db show --resource-group $ResourceGroup --server $sqlServer --name $sqlDatabase)) {
    Write-Host "Creating Azure SQL Database..."
    Invoke-Az sql db create `
        --resource-group $ResourceGroup `
        --server $sqlServer `
        --name $sqlDatabase `
        --service-objective Basic `
        --max-size 2GB `
        --backup-storage-redundancy Local `
        --output none
}

$clientIp = (Invoke-RestMethod -Uri "https://api.ipify.org").Trim()
Invoke-Az sql server firewall-rule create `
    --resource-group $ResourceGroup `
    --server $sqlServer `
    --name CurrentClient `
    --start-ip-address $clientIp `
    --end-ip-address $clientIp `
    --output none

Invoke-Az sql server firewall-rule create `
    --resource-group $ResourceGroup `
    --server $sqlServer `
    --name AllowAzureServices `
    --start-ip-address 0.0.0.0 `
    --end-ip-address 0.0.0.0 `
    --output none

$cosmosState = az cosmosdb show `
    --resource-group $ResourceGroup `
    --name $cosmosAccount `
    --query provisioningState `
    --output tsv 2>$null

if ($LASTEXITCODE -eq 0 -and $cosmosState -eq "Failed") {
    Write-Host "Removing failed Cosmos DB account before retry..."
    Invoke-Az cosmosdb delete `
        --resource-group $ResourceGroup `
        --name $cosmosAccount `
        --yes `
        --output none

    for ($attempt = 1; $attempt -le 60; $attempt++) {
        if (-not (Test-Az cosmosdb show --resource-group $ResourceGroup --name $cosmosAccount)) {
            break
        }
        if ($attempt -eq 60) {
            throw "Timed out waiting for the failed Cosmos DB account to be removed."
        }
        Start-Sleep -Seconds 5
    }
    $cosmosState = $null
}

if (-not $cosmosState) {
    Write-Host "Creating Cosmos DB account..."
    Invoke-Az cosmosdb create `
        --resource-group $ResourceGroup `
        --name $cosmosAccount `
        --locations regionName=$CosmosLocation failoverPriority=0 isZoneRedundant=False `
        --default-consistency-level Session `
        --output none
}

Invoke-Az cosmosdb sql database create `
    --resource-group $ResourceGroup `
    --account-name $cosmosAccount `
    --name $cosmosDatabase `
    --output none

if (-not (Test-Az cosmosdb sql container show --resource-group $ResourceGroup --account-name $cosmosAccount --database-name $cosmosDatabase --name $cosmosContainer)) {
    Invoke-Az cosmosdb sql container create `
        --resource-group $ResourceGroup `
        --account-name $cosmosAccount `
        --database-name $cosmosDatabase `
        --name $cosmosContainer `
        --partition-key-path "/neighborhoodId" `
        --throughput 400 `
        --output none
}

$cosmosRoleId = Invoke-Az cosmosdb sql role definition list `
    --resource-group $ResourceGroup `
    --account-name $cosmosAccount `
    --query "[?roleName=='Cosmos DB Built-in Data Contributor'].id | [0]" `
    --output tsv

$existingCosmosRole = az cosmosdb sql role assignment list `
    --resource-group $ResourceGroup `
    --account-name $cosmosAccount `
    --query "[?principalId=='$($currentUser.id)'] | [0].id" `
    --output tsv

if (-not $existingCosmosRole) {
    Invoke-Az cosmosdb sql role assignment create `
        --resource-group $ResourceGroup `
        --account-name $cosmosAccount `
        --role-definition-id $cosmosRoleId `
        --principal-id $currentUser.id `
        --scope "/" `
        --output none
}

if (-not (Test-Az storage account show --resource-group $ResourceGroup --name $storageAccount)) {
    Write-Host "Creating ADLS Gen2 storage account..."
    Invoke-Az storage account create `
        --resource-group $ResourceGroup `
        --name $storageAccount `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2 `
        --hns true `
        --allow-blob-public-access false `
        --min-tls-version TLS1_2 `
        --https-only true `
        --output none
}

$storageId = Invoke-Az storage account show `
    --resource-group $ResourceGroup `
    --name $storageAccount `
    --query id `
    --output tsv

$existingStorageRole = az role assignment list `
    --assignee-object-id $currentUser.id `
    --scope $storageId `
    --role "Storage Blob Data Contributor" `
    --query "[0].id" `
    --output tsv

if (-not $existingStorageRole) {
    Invoke-Az role assignment create `
        --assignee-object-id $currentUser.id `
        --assignee-principal-type User `
        --role "Storage Blob Data Contributor" `
        --scope $storageId `
        --output none
}

$storageKey = Invoke-Az storage account keys list `
    --resource-group $ResourceGroup `
    --account-name $storageAccount `
    --query "[0].value" `
    --output tsv

$fileSystemExists = Invoke-Az storage fs exists `
    --name $fileSystem `
    --account-name $storageAccount `
    --account-key $storageKey `
    --query exists `
    --output tsv

if ($fileSystemExists -ne "true") {
    Invoke-Az storage fs create `
        --name $fileSystem `
        --account-name $storageAccount `
        --account-key $storageKey `
        --output none
}

Write-Host ""
Write-Host "Deployment complete."
Write-Host "SQL:    $sqlServer.database.windows.net / $sqlDatabase"
Write-Host "Cosmos: https://$cosmosAccount.documents.azure.com:443/ / $cosmosDatabase / $cosmosContainer"
Write-Host "ADLS:   https://$storageAccount.dfs.core.windows.net/$fileSystem"
