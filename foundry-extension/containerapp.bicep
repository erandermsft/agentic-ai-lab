@description('Name of the Container App')
param containerAppName string = 'ailzlab-app'

@description('Unique identifier to append to app name to avoid collisions')
param uniqueIdentifier string = uniqueString(resourceGroup().id)

@description('Location for all resources')
param location string = resourceGroup().location

@description('Name of the Container Apps Environment')
param environmentName string

@description('Name of the Azure Container Registry')
param acrName string

@description('Resource ID of the existing user-assigned managed identity')
param managedIdentityId string

@description('Container image to deploy')
param containerImage string = '${acrName}.azurecr.io/ailzlab-${uniqueIdentifier}:latest'

@description('Target port for the container')
param targetPort int = 8000

@description('Ingress type: internal or external')
@allowed([
  'internal'
  'external'
])
param ingressType string = 'internal'

// Reference existing Container Apps Environment
resource environment 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: environmentName
}

// Reference existing Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: acrName
}

// Reference existing user-assigned managed identity
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' existing = {
  name: last(split(managedIdentityId, '/'))
}

// Container App with user-assigned managed identity
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${containerAppName}-${uniqueIdentifier}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }
  properties: {
    environmentId: environment.id
    configuration: {
      ingress: {
        external: ingressType == 'external'
        targetPort: targetPort
        transport: 'auto'
      }
      registries: [
        {
          server: '${acrName}.azurecr.io'
          identity: managedIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'ailzlab'
          image: containerImage
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            {
              name: 'AZURE_CLIENT_ID'
              value: managedIdentity.properties.clientId
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      ]
    }
  }
}

output containerAppName string = containerApp.name
output managedIdentityId string = managedIdentity.id
output fqdn string = containerApp.properties.configuration.ingress.fqdn
