# Manual de la CLI de Azure para Desarrollo de IA

## Tabla de Contenidos

- [Instalación y Configuración](#instalación-y-configuración)
- [Gestión de Recursos Básicos](#gestión-de-recursos-básicos)
- [Azure AI Services](#azure-ai-services)
  - [Azure AI Foundry](#azure-ai-foundry)
  - [Servicios de IA Individuales](#servicios-de-ia-individuales)
  - [Modelos de IA](#modelos-de-ia)
  - [RAG (Retrieval Augmented Generation)](#rag-retrieval-augmented-generation)
- [Azure Machine Learning](#azure-machine-learning)
- [Bases de Datos](#bases-de-datos)
- [Redes y Seguridad](#redes-y-seguridad)
- [Automatización y Scripts](#automatización-y-scripts)
- [Sistemas Multi-Agente](#sistemas-multi-agente)
- [Escenarios Avanzados](#escenarios-avanzados)
- [Solución de Problemas](#solución-de-problemas)
- [Recursos Adicionales](#recursos-adicionales)
- [Computer Vision Solutions](#computer-vision-solutions)
- [Procesamiento de Lenguaje Natural (NLP)](#procesamiento-de-lenguaje-natural-nlp)
- [IA Responsable](#ia-responsable)

## Instalación y Configuración

### Instalación

#### Windows

```powershell
# Instalar con winget
winget install -e --id Microsoft.AzureCLI

# O descargar e instalar manualmente
# https://learn.microsoft.com/cli/azure/install-azure-cli-windows
```

#### macOS (Homebrew)

```bash
# Instalar con Homebrew
brew update && brew install azure-cli

# O con curl
# https://learn.microsoft.com/cli/azure/install-azure-cli-macos
```

#### Linux (Ubuntu/Debian)

```bash
# Instalación en Ubuntu/Debian
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Para otras distribuciones:
# https://learn.microsoft.com/cli/azure/install-azure-cli-linux
```

### Configuración Inicial

```bash
# Iniciar sesión interactivo
az login

# Listar suscripciones disponibles
az account list --output table

# Establecer suscripción por defecto
az account set --subscription "<subscription-name-or-id>"

# Configurar parámetros por defecto
az config set defaults.group=<resource-group-name>
az config set defaults.location=<location>
```

## Gestión de Recursos Básicos

### Grupos de Recursos

```bash
# Crear grupo de recursos
az group create --name <resource-group-name> --location <location>
# https://learn.microsoft.com/cli/azure/group#az-group-create

# Listar grupos de recursos
az group list --output table
# https://learn.microsoft.com/cli/azure/group#az-group-list

# Eliminar grupo de recursos
az group delete --name <resource-group-name> --yes --no-wait
# https://learn.microsoft.com/cli/azure/group#az-group-delete
```

### Recursos Generales

```bash
# Listar todos los recursos en un grupo
az resource list --resource-group <resource-group-name>
# https://learn.microsoft.com/cli/azure/resource#az-resource-list

# Mostrar detalles de un recurso específico
az resource show --name <resource-name> --resource-group <resource-group-name> --resource-type <provider-namespace>/<resource-type>

# Eliminar un recurso específico
az resource delete --name <resource-name> --resource-group <resource-group-name> --resource-type <provider-namespace>/<resource-type>
```

## Azure AI Services

### Azure AI Foundry

#### Gestión de Proyectos

```bash
# Crear un nuevo proyecto de AI Foundry
az resource create \
  --resource-group mi-grupo-recursos \
  --name mi-proyecto-ai \
  --resource-type Microsoft.MachineLearningServices/workspaces \
  --is-full-object \
  --properties '{
    "location": "eastus",
    "properties": {
      "friendlyName": "Mi Proyecto AI",
      "description": "Proyecto para el laboratorio AI-102",
      "keyVault": "/subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.KeyVault/vaults/mi-keyvault",
      "applicationInsights": "/subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/microsoft.insights/components/mi-appinsights",
      "containerRegistry": "/subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.ContainerRegistry/registries/mi-registro"
    },
    "identity": {
      "type": "SystemAssigned"
    }
  }'

# Listar proyectos existentes
az resource list \
  --resource-group mi-grupo-recursos \
  --resource-type Microsoft.MachineLearningServices/workspaces
```

#### Configuración de Agentes

```bash
# Crear un agente de IA
az ml online-endpoint create \
  --name mi-agente-ia \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --file endpoint.yml \
  --set identity.type=SystemAssigned

# Configurar el despliegue del agente
az ml online-deployment create \
  --name blue \
  --endpoint-name mi-agente-ia \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --file deployment.yml \
  --all-traffic
```

### Servicios de IA Individuales

#### Azure AI Language

```bash
# Crear un recurso de Azure AI Language
az cognitiveservices account create \
  --name nombre-recurso-language \
  --resource-group mi-grupo-recursos \
  --kind TextAnalytics \
  --sku S \
  --location eastus \
  --yes

# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name nombre-recurso-language \
  --resource-group mi-grupo-recursos
```

#### Azure AI Vision

```bash
# Crear un recurso de Azure AI Vision
az cognitiveservices account create \
  --name nombre-recurso-vision \
  --resource-group mi-grupo-recursos \
  --kind ComputerVision \
  --sku S1 \
  --location eastus \
  --yes

# Obtener el punto de conexión
az cognitiveservices account show \
  --name nombre-recurso-vision \
  --resource-group mi-grupo-recursos \
  --query "properties.endpoint"
```

#### Azure OpenAI Service

```bash
# Solicitar acceso a Azure OpenAI
az cognitiveservices account create \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --kind OpenAI \
  --sku s0 \
  --location eastus \
  --custom-domain nombre-recurso-openai \
  --yes

# Listar modelos disponibles
az cognitiveservices account list-models \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos
```

#### Azure AI Search (anteriormente Cognitive Search)

```bash
# Crear un servicio de Azure AI Search
az search service create \
  --name nombre-busqueda \
  --resource-group mi-grupo-recursos \
  --sku standard \
  --partition-count 1 \
  --replica-count 1 \
  --location eastus

# Crear un índice de búsqueda
az search index create \
  --name mi-indice \
  --resource-group mi-grupo-recursos \
  --service-name nombre-busqueda \
  --fields \
    name=id type=Edm.String key=true \
    name=content type=Edm.String searchable=true
```

#### Azure Bot Service

```bash
# Crear un bot de Azure
az bot create \
  --resource-group mi-grupo-recursos \
  --name mi-bot \
  --kind registration \
  --appid "<app-id>" \
  --password "<app-password>" \
  --endpoint "https://<your-web-app>.azurewebsites.net/api/messages" \
  --sku F0

# Publicar un bot
az bot publish \
  --name mi-bot \
  --resource-group mi-grupo-recursos \
  --code-dir .
```

#### Azure Cognitive Services for Language

```bash
# Crear un recurso de Language Understanding (LUIS)
az cognitiveservices account create \
  --name nombre-recurso-luis \
  --resource-group mi-grupo-recursos \
  --kind LUIS \
  --sku S0 \
  --location westus \
  --yes

# Crear un recurso de QnA Maker
az cognitiveservices account create \
  --name nombre-recurso-qna \
  --resource-group mi-grupo-recursos \
  --kind QnAMaker \
  --sku S0 \
  --location westus \
  --yes
```

### Modelos de IA

#### Desplegar un modelo

```bash
# Desplegar un modelo de OpenAI
az cognitiveservices account deployment create \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --deployment-name mi-modelo-gpt \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard"

# Listar despliegues existentes
az cognitiveservices account deployment list \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos
```

#### Gestionar cuotas y límites

```bash
# Ver cuota de tokens
az cognitiveservices account list-usages \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos

# Aumentar cuota (solicitud)
az cognitiveservices account update \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --custom-domain nombre-recurso-openai \
  --sku-capacity 10
```

#### Monitoreo y análisis

```bash
# Ver métricas de uso
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.CognitiveServices/accounts/nombre-recurso-openai \
  --metric "TotalCalls" \
  --interval PT1H \
  --output table

# Configurar alertas
az monitor metrics alert create \
  --name "AltoUsoTokens" \
  --resource-group mi-grupo-recursos \
  --scopes /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.CognitiveServices/accounts/nombre-recurso-openai \
  --condition "avg TotalTokens > 1000" \
  --description "Uso alto de tokens detectado"
```

## Azure Machine Learning

```bash
# Instalar extensión de ML
az extension add -n ml

# Crear un workspace de Azure ML
az ml workspace create \
    --name <workspace-name> \
    --resource-group <resource-group-name> \
    --location <location>
# https://learn.microsoft.com/cli/azure/ml/workspace#az-ml-workspace-create

# Crear un entorno de computación
az ml compute create \
    --name <compute-name> \
    --resource-group <resource-group-name> \
    --workspace-name <workspace-name> \
    --type AmlCompute \
    --min-instances 0 \
    --max-instances 3 \
    --size Standard_DS3_v2
# https://learn.microsoft.com/cli/azure/ml/compute#az-ml-compute-create

# Entrenar un modelo
az ml job create \
    --file train.yml \
    --workspace-name <workspace-name> \
    --resource-group <resource-group-name>
# https://learn.microsoft.com/azure/machine-learning/how-to-train-cli
```

## Bases de Datos

### Azure Cosmos DB

```bash
# Crear una cuenta de Cosmos DB
az cosmosdb create \
  --name nombre-cuenta-cosmos \
  --resource-group mi-grupo-recursos \
  --locations regionName=eastus \
  --capabilities EnableServerless

# Crear una base de datos y contenedor
az cosmosdb sql database create \
  --account-name nombre-cuenta-cosmos \
  --name mi-base-datos \
  --resource-group mi-grupo-recursos

az cosmosdb sql container create \
  --account-name nombre-cuenta-cosmos \
  --database-name mi-base-datos \
  --name mi-contenedor \
  --partition-key-path "/id" \
  --resource-group mi-grupo-recursos
```

### Azure Database for PostgreSQL

```bash
# Crear un servidor PostgreSQL
az postgres server create \
  --name nombre-servidor-postgres \
  --resource-group mi-grupo-recursos \
  --location eastus \
  --admin-user adminuser \
  --admin-password P@ssw0rd! \
  --sku-name GP_Gen5_2 \
  --version 11

# Habilitar la extensión pgvector para IA
az postgres server configuration set \
  --resource-group mi-grupo-recursos \
  --server-name nombre-servidor-postgres \
  --name azure.extensions \
  --value vector
```

### Azure Database for MySQL

```bash
# Crear un servidor MySQL
az mysql server create \
  --name nombre-servidor-mysql \
  --resource-group mi-grupo-recursos \
  --location eastus \
  --admin-user adminuser \
  --admin-password P@ssw0rd! \
  --sku-name GP_Gen5_2 \
  --version 8.0

# Configurar parámetros del servidor
az mysql server configuration set \
  --name slow_query_log \
  --resource-group mi-grupo-recursos \
  --server nombre-servidor-mysql \
  --value ON
```

### Azure SQL Database

```bash
# Crear un servidor SQL lógico
az sql server create \
  --name nombre-servidor-sql \
  --resource-group mi-grupo-recursos \
  --location eastus \
  --admin-user adminuser \
  --admin-password P@ssw0rd!

# Crear una base de datos SQL
az sql db create \
  --name mi-base-datos-sql \
  --resource-group mi-grupo-recursos \
  --server nombre-servidor-sql \
  --service-objective S0 \
  --edition Standard
```

### Azure Cache for Redis

```bash
# Crear una instancia de Azure Cache for Redis
az redis create \
  --name nombre-cache-redis \
  --resource-group mi-grupo-recursos \
  --location eastus \
  --sku Basic \
  --vm-size c0 \
  --enable-non-ssl-port
```

## RAG (Retrieval Augmented Generation)

### Configuración básica de RAG

```bash
# Crear un índice de búsqueda cognitiva (requerido para RAG)
az search service create \
    --name <search-service-name> \
    --resource-group <resource-group-name> \
    --location <location> \
    --sku standard
# https://learn.microsoft.com/azure/search/search-create-service-portal

# Crear un índice de búsqueda
az search index create \
    --name <index-name> \
    --resource-group <resource-group-name> \
    --service-name <search-service-name> \
    --schema @schema.json
# https://learn.microsoft.com/azure/search/search-import-data-portal

# Indexar documentos
az search indexer create \
    --name <indexer-name> \
    --data-source-name <data-source-name> \
    --index-name <index-name> \
    --resource-group <resource-group-name> \
    --service-name <search-service-name>
# https://learn.microsoft.com/azure/search/search-howto-indexing-azure-blob-storage
```

## Redes y Seguridad

### Redes Virtuales

```bash
# Crear una red virtual
az network vnet create \
    --name <vnet-name> \
    --resource-group <resource-group-name> \
    --location <location> \
    --address-prefix 10.0.0.0/16 \
    --subnet-name <subnet-name> \
    --subnet-prefix 10.0.0.0/24
# https://learn.microsoft.com/cli/azure/network/vnet#az-network-vnet-create

# Configurar punto de conexión privado
az network private-endpoint create \
    --name <private-endpoint-name> \
    --resource-group <resource-group-name> \
    --vnet-name <vnet-name> \
    --subnet <subnet-name> \
    --private-connection-resource-id <resource-id> \
    --group-id <group-id> \
    --connection-name <connection-name>
# https://learn.microsoft.com/azure/private-link/create-private-endpoint-cli
```

## Automatización y Scripts

### Script de Creación Completo

```bash
#!/bin/bash

# Configuración
RANDOM_SUFFIX=$((RANDOM % 10000))
LOCATION="eastus"
RESOURCE_GROUP_NAME="ai-lab-rg-$RANDOM_SUFFIX"
AI_FOUNDRY_NAME="ai-foundry-$RANDOM_SUFFIX"
STORAGE_ACCOUNT_NAME="aistorage${RANDOM_SUFFIX}"
SEARCH_SERVICE_NAME="aisearch${RANDOM_SUFFIX}"

# Crear grupo de recursos
echo "Creando grupo de recursos $RESOURCE_GROUP_NAME..."
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Crear cuenta de almacenamiento
echo "Creando cuenta de almacenamiento $STORAGE_ACCOUNT_NAME..."
az storage account create \
    --name $STORAGE_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --location $LOCATION \
    --sku Standard_LRS

# Crear servicio de búsqueda
echo "Creando servicio de búsqueda $SEARCH_SERVICE_NAME..."
az search service create \
    --name $SEARCH_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --location $LOCATION \
    --sku standard

# Crear recurso de Azure AI Foundry
echo "Creando recurso de Azure AI Foundry $AI_FOUNDRY_NAME..."
az cognitiveservices account create \
    --name $AI_FOUNDRY_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --location $LOCATION \
    --kind OpenAI \
    --sku s0 \
    --custom-domain $AI_FOUNDRY_NAME

# Mostrar información de conexión
echo "\nRecursos creados exitosamente:"
echo "- Grupo de recursos: $RESOURCE_GROUP_NAME"
echo "- Cuenta de almacenamiento: $STORAGE_ACCOUNT_NAME"
echo "- Servicio de búsqueda: $SEARCH_SERVICE_NAME"
echo "- Recurso AI Foundry: $AI_FOUNDRY_NAME"
echo "\nPara eliminar estos recursos cuando termines, ejecuta:"
echo "az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait"
```

## Sistemas Multi-Agente

### Configuración de un Sistema Multi-Agente

```bash
# Crear un grupo de agentes
az ml online-endpoint create \
  --name grupo-agentes \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --auth-mode key \
  --identity-type SystemAssigned

# Desplegar múltiples agentes especializados
for agent in agente-analista agente-investigador agente-ejecutor; do
  az ml online-deployment create \
    --name $agent \
    --endpoint-name grupo-agentes \
    --resource-group mi-grupo-recursos \
    --workspace-name mi-proyecto-ai \
    --file deployment-$agent.yml \
    --all-traffic
    --no-wait
done
```

### Orquestación con Semantic Kernel

```bash
# Instalar el SDK de Semantic Kernel
pip install semantic-kernel

# Configurar la integración con Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://tu-recurso.openai.azure.com/"
export AZURE_OPENAI_API_KEY="tu-clave-api"

# Crear un kernel de Semantic Kernel
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel = Kernel()
kernel.add_chat_service(
    "gpt-4",
    AzureChatCompletion(
        "gpt-4",
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_API_KEY
    )
)

# Definir habilidades para los agentes
agente_analista = kernel.import_semantic_skill_from_directory(
    "skills", "analista"
)

agente_ejecutor = kernel.import_semantic_skill_from_directory(
    "skills", "ejecutor"
)

# Orquestar la interacción entre agentes
context = kernel.create_new_context()
context["input"] = "Analizar el último informe trimestral"

# El analista procesa la solicitud
analisis = await agente_analista["analizar"].invoke_async(context=context)

# El ejecutor actúa basado en el análisis
context["analisis"] = analisis.result
action = await agente_ejecutor["ejecutar"].invoke_async(context=context)
```

### Monitoreo de Sistemas Multi-Agente

```bash
# Configurar Application Insights para seguimiento distribuido
az monitor app-insights component create \
  --app monitoreo-agentes \
  --location eastus \
  --resource-group mi-grupo-recursos \
  --application-type web \
  --kind web

# Consultar trazas distribuidas
az monitor app-insights query \
  --app monitoreo-agentes \
  --resource-group mi-grupo-recursos \
  --analytics-query "traces | where operation_Name == 'ProcesarTarea' | order by timestamp desc"
```

## Escenarios Avanzados

### Entrenamiento Distribuido

```bash
# Configurar un clúster de entrenamiento distribuido
az ml compute create \
  --name cluster-entrenamiento \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --type AmlCompute \
  --size Standard_ND40rs_v2 \
  --min-instances 0 \
  --max-instances 4 \
  --idle-time-before-scale-down 3600

# Enviar trabajo de entrenamiento distribuido
az ml job create \
  --file distributed-training.yml \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --set environment_variables.NUM_GPUS=4 \
  --set resources.instance_count=4
```

### Inferencia de Baja Latencia

```bash
# Implementar con aceleración por hardware
az ml model deploy \
  --name modelo-acelerado \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --model mi-modelo:1 \
  --inference-config inference-config.yml \
  --deployment-config deployment-config.yml \
  --set environment_variables.INFERENCE_ACCELERATOR="FPGA" \
  --set environment_variables.OPTIMIZATION_LEVEL=3
```

### Implementación Híbrida Nube-Borde

```bash
# Empaquetar modelo para implementación en el borde
az ml model package \
  --name modelo-para-borde \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-proyecto-ai \
  --model mi-modelo:1 \
  --target-platform linux-arm64

# Implementar en dispositivo IoT Edge
az iot edge set-modules \
  --device-id mi-dispositivo \
  --hub-name mi-iot-hub \
  --content deployment.arm64.json
```

### Escalado Automático Avanzado

```bash
# Configurar escalado basado en métricas personalizadas
az monitor autoscale create \
  --resource-group mi-grupo-recursos \
  --resource mi-endpoint \
  --resource-type Microsoft.MachineLearningServices/onlineEndpoints \
  --name escalado-automatico-avanzado \
  --min-count 1 \
  --max-count 10 \
  --count 2 \
  --rules \
    "[{\"metricTrigger\": {\"metricName\": \"RequestLatency\", \"metricResourceUri\": \"/subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.MachineLearningServices/workspaces/mi-proyecto-ai/onlineEndpoints/mi-endpoint\", \"timeGrain\": \"PT1M\", \"statistic\": \"Average\", \"timeWindow\": \"PT5M\", \"timeAggregation\": \"Average\", \"operator\": \"GreaterThan\", \"threshold\": 100}, \"scaleAction\": {\"direction\": \"Increase\", \"type\": \"ChangeCount\", \"value\": \"1\", \"cooldown\": \"PT5M\"}}]"
```

## Solución de Problemas

### Comandos de diagnóstico

```bash
# Verificar estado de los servicios de Azure
az resource list --query "[?type=='Microsoft.Resources/subscriptions/resourceGroups'].name" --output tsv | xargs -I {} az resource list --resource-group {}

# Verificar cuotas de suscripción
az vm list-usage --location <location> --output table

# Verificar registros de actividad
az monitor activity-log list --resource-group <resource-group-name> --offset 90d

# Solución de problemas de conectividad
az network watcher test-connectivity --source-resource <vm-id> --dest-port 443 --dest-address <destination-ip>
```

## Recursos Adicionales

- [Documentación oficial de la CLI de Azure](https://learn.microsoft.com/cli/azure/)
- [Ejemplos de la CLI de Azure](https://learn.microsoft.com/cli/azure/sample-azure-cli)
- [Referencia de comandos de Azure CLI](https://learn.microsoft.com/cli/azure/reference-index)
- [Plantillas de Azure Resource Manager](https://learn.microsoft.com/azure/azure-resource-manager/templates/)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)

## Azure OpenAI

### Gestión de Modelos

```bash
# Listar modelos disponibles
az cognitiveservices account list-models \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --query "sort_by([].{name:name, version:version, status:model.status}, &name)" \
  --output table

# Implementar un modelo personalizado
az cognitiveservices account deployment create \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --deployment-name mi-modelo-gpt \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard" \
  --scale-settings-capacity 10
```

### Configuración de RAG (Retrieval Augmented Generation)

```bash
# Crear un índice de búsqueda para RAG
az search service create \
  --name mi-busqueda-rag \
  --resource-group mi-grupo-recursos \
  --location eastus \
  --sku standard \
  --partition-count 1 \
  --replica-count 1

# Crear fuente de datos para RAG
az search datasource create \
  --name mi-fuente-datos \
  --resource-group mi-grupo-recursos \
  --service-name mi-busqueda-rag \
  --type azureblob \
  --data-source-configuration '{"connectionString": "DefaultEndpointsProtocol=https;AccountName=micuenta;AccountKey=mi-clave;EndpointSuffix=core.windows.net", "container": {"name": "mi-contenedor"}}' \
  --data-deletion-detection-mode None
```

## Monitoreo y Análisis

### Application Insights

```bash
# Crear recurso de Application Insights
az monitor app-insights component create \
  --app mi-aplicacion-ai \
  --location eastus \
  --resource-group mi-grupo-recursos \
  --application-type web \
  --kind web \
  --retention-in-days 90

# Obtener la clave de instrumentación
az monitor app-insights component show \
  --app mi-aplicacion-ai \
  --resource-group mi-grupo-recursos \
  --query "instrumentationKey" \
  --output tsv
```

### Configuración de Alertas

```bash
# Crear una regla de alerta para uso de tokens
az monitor metrics alert create \
  --name "AltoUsoTokens" \
  --resource-group mi-grupo-recursos \
  --scopes /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.CognitiveServices/accounts/nombre-recurso-openai \
  --condition "avg TotalTokens > 1000" \
  --description "Uso alto de tokens detectado" \
  --evaluation-frequency 5m \
  --window-size 15m \
  --severity 2
```

## Seguridad y Control de Acceso

### Identidades Administradas

```bash
# Asignar una identidad administrada a un recurso
az cognitiveservices account identity assign \
  --name nombre-recurso-openai \
  --resource-group mi-grupo-recursos \
  --identities '[system]'

# Otorgar permisos a la identidad
az role assignment create \
  --assignee <object-id> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.Storage/storageAccounts/micuentastorage
```

### Puntos de Conexión Privados

```bash
# Crear un punto de conexión privado para Azure OpenAI
az network private-endpoint create \
  --name pe-openai \
  --resource-group mi-grupo-recursos \
  --vnet-name mi-vnet \
  --subnet mi-subnet \
  --private-connection-resource-id /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.CognitiveServices/accounts/nombre-recurso-openai \
  --group-account-id account \
  --connection-name mi-conexion-privada
```

## Integración Continua/Despliegue Continuo (CI/CD)

### Pipeline de Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: 'Mi-Suscripcion-Azure'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      # Desplegar modelo
      az cognitiveservices account deployment create \
        --name nombre-recurso-openai \
        --resource-group mi-grupo-recursos \
        --deployment-name mi-modelo-gpt \
        --model-name gpt-4 \
        --model-version "0613"
      
      # Actualizar configuración
      az cognitiveservices account update \
        --name nombre-recurso-openai \
        --resource-group mi-grupo-recursos \
        --custom-domain mi-dominio-personalizado

```

## Computer Vision Solutions

### Análisis de Imágenes Avanzado

```bash
# Configurar un recurso de Azure AI Vision
az cognitiveservices account create \
  --name mi-recurso-vision \
  --resource-group mi-grupo-recursos \
  --kind ComputerVision \
  --sku S1 \
  --location eastus \
  --yes

# Analizar una imagen
az cognitiveservices vision analyze \
  --name mi-recurso-vision \
  --resource-group mi-grupo-recursos \
  --image-url "https://example.com/image.jpg" \
  --visual-features "Description,Tags,Categories,Color,Objects,Faces,Adult,Brands"

# Extraer texto de imágenes (OCR)
az cognitiveservices vision ocr \
  --name mi-recurso-vision \
  --resource-group mi-grupo-recursos \
  --image-url "https://example.com/document.jpg" \
  --language en
```

### Modelos de Visión Personalizados

```bash
# Crear un proyecto de Custom Vision
az cognitiveservices account create \
  --name mi-custom-vision \
  --resource-group mi-grupo-recursos \
  --kind CustomVision.Training \
  --sku S0 \
  --location eastus \
  --yes

# Entrenar un modelo de clasificación de imágenes
az cognitiveservices custom-vision project create \
  --name "Clasificador de Productos" \
  --description "Clasificación de productos por categoría" \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-espacio-trabajo \
  --domain-id "ee85a74c-405e-4adc-bb47-ffa8ca0c9f31"  # General (compact)

# Publicar el modelo entrenado
az cognitiveservices custom-vision project publish \
  --name "Clasificador de Productos" \
  --resource-group mi-grupo-recursos \
  --workspace-name mi-espacio-trabajo \
  --prediction-resource-id /subscriptions/{subscription-id}/resourceGroups/mi-grupo-recursos/providers/Microsoft.CognitiveServices/accounts/mi-custom-vision-prediction \
  --publish-name produccion \
  --prediction-type Classification
```

### Análisis de Video

```bash
# Configurar Azure Video Indexer
az account set --subscription "mi-suscripcion-id"

# Obtener token de acceso para Video Indexer
az account get-access-token --resource "https://management.azure.com/"

# Indexar un video
curl -X POST "https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos?accessToken={accessToken}&name=mi-video&videoUrl={videoUrl}"

# Obtener información del video indexado
curl -X GET "https://api.videoindexer.ai/{location}/Accounts/{accountId}/Videos/{videoId}/Index?accessToken={accessToken}"
```

## Procesamiento de Lenguaje Natural (NLP)

### Análisis de Texto

```bash
# Analizar sentimiento y frases clave
az cognitiveservices language analyze-sentiment \
  --resource-group mi-grupo-recursos \
  --name mi-recurso-language \
  --text "El servicio fue excelente, pero la entrega se retrasó" \
  --query "[documents[0].sentiment,documents[0].confidenceScores]

# Extraer entidades
az cognitiveservices language recognize-entities \
  --resource-group mi-grupo-recursos \
  --name mi-recurso-language \
  --text "Microsoft fue fundada por Bill Gates en 1975"

# Detectar idioma
az cognitiveservices language detect-language \
  --resource-group mi-grupo-recursos \
  --name mi-recurso-language \
  --text "Bonjour, comment ça va?"
```

### Procesamiento de Voz

```bash
# Configurar Azure Speech Service
az cognitiveservices account create \
  --name mi-recurso-speech \
  --resource-group mi-grupo-recursos \
  --kind SpeechServices \
  --sku S0 \
  --location eastus \
  --yes

# Convertir texto a voz (TTS)
curl -X POST "https://{region}.tts.speech.microsoft.com/cognitiveservices/v1" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/ssml+xml" \
  -d "<speak version='1.0' xml:lang='es-ES'><voice name='es-ES-ElviraNeural'>Hola, esto es una prueba de texto a voz.</voice></speak>" \
  --output speech.wav

# Transcripción de voz a texto
curl -X POST "https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=es-ES" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: audio/wav" \
  --data-binary @audio.wav
```

### Modelos de Lenguaje Personalizados

```bash
# Crear un proyecto de Language Understanding (LUIS)
az cognitiveservices account create \
  --name mi-recurso-luis \
  --resource-group mi-grupo-recursos \
  --kind LUIS \
  --sku S0 \
  --location westus \
  --yes

# Entrenar un modelo de LUIS
az cognitiveservices luis train \
  --app-id {app-id} \
  --version-id "0.1" \
  --wait

# Publicar el modelo de LUIS
az cognitiveservices luis app publish \
  --app-id {app-id} \
  --version-id "0.1" \
  --staging
```

## IA Responsable

### Moderación de Contenido

```bash
# Configurar Azure Content Moderator
az cognitiveservices account create \
  --name mi-content-moderator \
  --resource-group mi-grupo-recursos \
  --kind ContentModerator \
  --sku S0 \
  --location global \
  --yes

# Moderar texto
az cognitiveservices contentmoderator text-moderation \
  --resource-group mi-grupo-recursos \
  --name mi-content-moderator \
  --text "Este es un texto ofensivo que debe ser moderado"

# Moderar imágenes
az cognitiveservices contentmoderator image-moderation \
  --resource-group mi-grupo-recursos \
  --name mi-content-moderator \n  --image-url "https://example.com/image.jpg"
```

### Configuración de IA Responsable

```bash
# Habilitar características de IA responsable en Azure OpenAI
az cognitiveservices account update \
  --name mi-recurso-openai \
  --resource-group mi-grupo-recursos \
  --custom-domain mi-dominio-personalizado \
  --content-filter "{\"filterType\": \"BlockList\", \"blockList\": [\"contenido-peligroso\"]}" \
  --safe-prompt "{\"enabled\": true}"

# Configurar límites de seguridad
az cognitiveservices account deployment update \
  --name mi-recurso-openai \
  --resource-group mi-grupo-recursos \
  --deployment-name mi-modelo-gpt \
  --content-filter-severity medium \
  --content-filter-type SelfHarm|Hate|Sexual|Violence
```
