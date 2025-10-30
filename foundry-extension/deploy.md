# Deploy to Azure Container Apps

## Prerequisites
```powershell
# Login to Azure
az login

# Set your subscription (replace with your subscription ID)
az account set --subscription <subscription-id>

# Set your variables
$ACR_NAME="<your-acr-name>"
$RESOURCE_GROUP="<your-resource-group>"
$ENVIRONMENT="<your-container-app-environment>"
$MANAGED_IDENTITY_ID="<resource-id-of-your-umi>"
$APP_NAME="ailzlab-app"
```

## Step 1: Build Docker Image Locally
```powershell
docker build -t ailzlab:latest .
```

## Step 2: Tag and Push to Existing ACR
```powershell
# Login to ACR
az acr login --name $ACR_NAME

# Generate unique identifier (same as what Bicep will use)
$UNIQUE_ID = az group show --name $RESOURCE_GROUP --query id -o tsv | ForEach-Object { [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($_))) -replace '-','' } | ForEach-Object { $_.Substring(0,13).ToLower() }

# Tag the image with unique identifier
docker tag ailzlab:latest "$ACR_NAME.azurecr.io/ailzlab-$UNIQUE_ID:latest"

# Push to ACR
docker push "$ACR_NAME.azurecr.io/ailzlab-$UNIQUE_ID:latest"
```

## Step 3: Deploy to Existing Container Apps Environment

### Using Bicep with Existing User-Assigned Managed Identity (Recommended)
```powershell
# Deploy using existing UMI (which already has ACR pull permissions)
az deployment group create `
  --resource-group $RESOURCE_GROUP `
  --template-file containerapp.bicep `
  --parameters `
    containerAppName=$APP_NAME `
    environmentName=$ENVIRONMENT `
    acrName=$ACR_NAME `
    managedIdentityId=$MANAGED_IDENTITY_ID `
    ingressType='internal'
```

This approach:
- Uses an existing user-assigned managed identity (which already has ACR pull permissions)
- Deploys the container app with your image and a unique identifier to avoid name collisions
- Single deployment with no circular dependencies!

### Option A: Using ACR Admin Credentials (Alternative)
```powershell
# Deploy directly with admin credentials
az containerapp create `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT `
  --image "$ACR_NAME.azurecr.io/ailzlab:latest" `
  --registry-server "$ACR_NAME.azurecr.io" `
  --registry-username $ACR_NAME `
  --registry-password (az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv) `
  --target-port 8000 `
  --ingress internal `
  --query properties.configuration.ingress.fqdn
```

### Option B: Using Managed Identity Manually (Alternative)
```powershell
# Step 1: Create container app with a public image first
az containerapp create `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT `
  --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest `
  --target-port 80 `
  --ingress internal

# Step 2: Enable system-assigned managed identity
az containerapp identity assign `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --system-assigned

# Step 3: Get the principal ID
$PRINCIPAL_ID = az containerapp identity show `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query principalId -o tsv

# Step 4: Get ACR resource ID
$ACR_ID = az acr show --name $ACR_NAME --query id -o tsv

# Step 5: Grant AcrPull permission
az role assignment create `
  --assignee $PRINCIPAL_ID `
  --role AcrPull `
  --scope $ACR_ID

# Wait a moment for role assignment to propagate
Start-Sleep -Seconds 30

# Step 6: Update container app with your image using managed identity
az containerapp update `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --image "$ACR_NAME.azurecr.io/ailzlab:latest" `
  --set-env-vars "TARGET_PORT=8000"

az containerapp ingress update `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --target-port 8000

az containerapp registry set `
  --name $APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --server "$ACR_NAME.azurecr.io" `
  --identity system
```

## Update the Container App (after making changes)
```powershell
# Rebuild locally
docker build -t ailzlab:latest .

# Generate unique identifier (same as what Bicep will use)
$UNIQUE_ID = az group show --name $RESOURCE_GROUP --query id -o tsv | ForEach-Object { [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($_))) -replace '-','' } | ForEach-Object { $_.Substring(0,13).ToLower() }

# Tag and push
docker tag ailzlab:latest "$ACR_NAME.azurecr.io/ailzlab-$UNIQUE_ID:latest"
docker push "$ACR_NAME.azurecr.io/ailzlab-$UNIQUE_ID:latest"

# Get the deployed app name (includes unique identifier)
$DEPLOYED_APP_NAME = az containerapp list `
  --resource-group $RESOURCE_GROUP `
  --query "[?starts_with(name, '$APP_NAME')].name" -o tsv

# Update the container app
az containerapp update `
  --name $DEPLOYED_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --image "$ACR_NAME.azurecr.io/ailzlab-$UNIQUE_ID:latest"
```

## Get the App URL
```powershell
# Get the deployed app name (includes unique identifier)
$DEPLOYED_APP_NAME = az containerapp list `
  --resource-group $RESOURCE_GROUP `
  --query "[?starts_with(name, '$APP_NAME')].name" -o tsv

az containerapp show `
  --name $DEPLOYED_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query properties.configuration.ingress.fqdn -o tsv
```
