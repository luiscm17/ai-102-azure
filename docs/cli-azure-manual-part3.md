# Manual de la CLI de Azure para Desarrollo de IA (AI-102) - Parte 3: Flujos de Trabajo Avanzados y IA Responsable

Este manual, dividido en tres partes, está diseñado para preparar la certificación **AI-102: Designing and Implementing a Microsoft Azure AI Solution**, cubriendo todos los temas del [syllabus del curso AI-102](https://learn.microsoft.com/es-es/training/courses/ai-102t00#course-syllabus). La **Parte 3** abarca flujos de trabajo avanzados, incluyendo Azure Machine Learning, bases de datos para IA, redes y seguridad, sistemas multi-agente, automatización, soluciones de visión computacional, procesamiento de lenguaje natural (NLP), IA responsable, y solución de problemas, usando la **Azure CLI** sin depender de interfaces gráficas como Azure AI Foundry. Los comandos están basados en Azure CLI 2.63.0 (agosto 2025), según la [documentación oficial](https://learn.microsoft.com/en-us/cli/azure/reference-docs-index?view=azure-cli-latest). La **Parte 1** cubrió fundamentos y gestión de recursos, y la **Parte 2** abordó servicios de IA y RAG.

## Tabla de Contenidos

1. [Azure Machine Learning](#1-azure-machine-learning)
   1. [Crear un Espacio de Trabajo](#11-crear-un-espacio-de-trabajo)
   2. [Gestionar Recursos de Cómputo](#12-gestionar-recursos-de-cómputo)
   3. [Entrenar y Desplegar Modelos](#13-entrenar-y-desplegar-modelos)
2. [Bases de Datos para IA](#2-bases-de-datos-para-ia)
   1. [Azure Cosmos DB](#21-azure-cosmos-db)
   2. [Azure Database for PostgreSQL](#22-azure-database-for-postgresql)
   3. [Azure Database for MySQL](#23-azure-database-for-mysql)
   4. [Azure SQL Database](#24-azure-sql-database)
3. [Redes y Seguridad](#3-redes-y-seguridad)
   1. [Redes Virtuales](#31-redes-virtuales)
   2. [Identidades Administradas](#32-identidades-administradas)
   3. [Puntos de Conexión Privados](#33-puntos-de-conexión-privados)
4. [Sistemas Multi-Agente](#4-sistemas-multi-agente)
5. [Automatización y Scripts](#5-automatización-y-scripts)
6. [Computer Vision Solutions](#6-computer-vision-solutions)
   1. [Análisis de Imágenes](#61-análisis-de-imágenes)
   2. [Modelos de Visión Personalizados](#62-modelos-de-visión-personalizados)
7. [Procesamiento de Lenguaje Natural (NLP)](#7-procesamiento-de-lenguaje-natural-nlp)
8. [IA Responsable](#8-ia-responsable)
   1. [Moderación de Contenido](#81-moderación-de-contenido)
   2. [Configuración de IA Responsable](#82-configuración-de-ia-responsable)
9. [Solución de Problemas](#9-solución-de-problemas)
10. [Recursos Adicionales](#10-recursos-adicionales)

## 1. Azure Machine Learning

Azure Machine Learning (AML) permite entrenar, desplegar y gestionar modelos de IA, integrado con Azure AI Foundry hubs y proyectos (ver **Parte 1**, Section 3.4).

### 1.1. Crear un Espacio de Trabajo

El hub y proyecto de Azure AI Foundry creados en **Parte 1** (Section 3.4.1) son espacios de trabajo AML. Para un espacio de trabajo independiente:

```bash
az ml workspace create \
  --name ai102-aml-workspace \
  --resource-group ai102-group \
  --location eastus2 \
  --kind default \
  --display-name "AI102 AML Workspace"
```

**Explicación**:
- `--kind default`: Crea un espacio de trabajo AML estándar, sin las capacidades de hub de Azure AI Foundry.

### 1.2. Gestionar Recursos de Cómputo

Crear un clúster de cómputo:

```bash
az ml compute create \
  --name ai102-compute \
  --resource-group ai102-group \
  --workspace-name ai102-hub \
  --type AmlCompute \
  --size Standard_DS3_v2 \
  --min-instances 0 \
  --max-instances 4
```

**Explicación**:
- `az ml compute create`: Crea un clúster de cómputo escalable para entrenamiento y despliegue en el hub `ai102-hub`.

### 1.3. Entrenar y Desplegar Modelos

Crear un archivo YAML para un trabajo de entrenamiento:

```bash
cat > train-job.yaml << EOF
code: ./code
command: python train.py
environment: azureml:AzureML-sklearn-1.0:1
compute: azureml:ai102-compute
experiment_name: ai102-experiment
EOF
```

Ejecutar el trabajo:

```bash
az ml job create \
  --file train-job.yaml \
  --resource-group ai102-group \
  --workspace-name ai102-hub
```

Desplegar un modelo entrenado:

```bash
cat > deploy-model.yaml << EOF
name: ai102-model
endpoint_name: ai102-endpoint
model: azureml:ai102-model:1
instance_type: Standard_DS3_v2
instance_count: 1
EOF

az ml online-deployment create \
  --file deploy-model.yaml \
  --resource-group ai102-group \
  --workspace-name ai102-hub
```

**Explicación**:
- `az ml job create`: Ejecuta un trabajo de entrenamiento en el clúster de cómputo.
- `az ml online-deployment create`: Despliega un modelo entrenado en un endpoint existente (`ai102-endpoint`).

**Documentación**:
- [az ml workspace](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest)
- [az ml compute](https://learn.microsoft.com/en-us/cli/azure/ml/compute?view=azure-cli-latest)
- [az ml job](https://learn.microsoft.com/en-us/cli/azure/ml/job?view=azure-cli-latest)
- [az ml online-deployment](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest)

## 2. Bases de Datos para IA

Las bases de datos de Azure son esenciales para almacenar datos para aplicaciones de IA.

### 2.1. Azure Cosmos DB

Crear una cuenta Cosmos DB:

```bash
az cosmosdb create \
  --name ai102-cosmos \
  --resource-group ai102-group \
  --locations regionName=eastus2 failoverPriority=0
```

Crear una base de datos y contenedor:

```bash
az cosmosdb sql database create \
  --account-name ai102-cosmos \
  --resource-group ai102-group \
  --name ai102-db

az cosmosdb sql container create \
  --account-name ai102-cosmos \
  --resource-group ai102-group \
  --database-name ai102-db \
  --name ai102-container \
  --partition-key-path /id
```

**Explicación**:
- `az cosmosdb create`: Crea una cuenta Cosmos DB para datos NoSQL.
- `az cosmosdb sql database/container create`: Configura una base de datos y contenedor.

### 2.2. Azure Database for PostgreSQL

```bash
az postgres flexible-server create \
  --name ai102-postgres \
  --resource-group ai102-group \
  --location eastus2 \
  --admin-user ai102admin \
  --admin-password <password> \
  --sku-name Standard_D2s_v3
```

**Explicación**:
- `az postgres flexible-server create`: Crea un servidor PostgreSQL flexible.

### 2.3. Azure Database for MySQL

```bash
az mysql flexible-server create \
  --name ai102-mysql \
  --resource-group ai102-group \
  --location eastus2 \
  --admin-user ai102admin \
  --admin-password <password> \
  --sku-name Standard_D2s_v3
```

**Explicación**:
- `az mysql flexible-server create`: Crea un servidor MySQL flexible.

### 2.4. Azure SQL Database

```bash
az sql server create \
  --name ai102-sqlserver \
  --resource-group ai102-group \
  --location eastus2 \
  --admin-user ai102admin \
  --admin-password <password>

az sql db create \
  --resource-group ai102-group \
  --server ai102-sqlserver \
  --name ai102-sqldb \
  --service-objective S0
```

**Explicación**:
- `az sql server/db create`: Crea un servidor y base de datos SQL.

**Documentación**:
- [az cosmosdb](https://learn.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest)
- [az postgres](https://learn.microsoft.com/en-us/cli/azure/postgres?view=azure-cli-latest)
- [az mysql](https://learn.microsoft.com/en-us/cli/azure/mysql?view=azure-cli-latest)
- [az sql](https://learn.microsoft.com/en-us/cli/azure/sql?view=azure-cli-latest)

## 3. Redes y Seguridad

### 3.1. Redes Virtuales

Crear una red virtual y subred:

```bash
az network vnet create \
  --name ai102-vnet \
  --resource-group ai102-group \
  --location eastus2 \
  --address-prefix 10.0.0.0/16

az network vnet subnet create \
  --name ai102-subnet \
  --vnet-name ai102-vnet \
  --resource-group ai102-group \
  --address-prefixes 10.0.1.0/24
```

**Explicación**:
- `az network vnet/subnet create`: Configura una red virtual para aislar recursos.

### 3.2. Identidades Administradas

Asignar una identidad administrada al hub:

```bash
az ml workspace update \
  --name ai102-hub \
  --resource-group ai102-group \
  --identity-type SystemAssigned
```

**Explicación**:
- `az ml workspace update`: Asigna una identidad administrada para autenticación segura.

### 3.3. Puntos de Conexión Privados

Crear un punto de conexión privado para Azure AI Services:

```bash
az network private-endpoint create \
  --name ai102-private-endpoint \
  --resource-group ai102-group \
  --vnet-name ai102-vnet \
  --subnet ai102-subnet \
  --private-connection-resource-id "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/ai102-group/providers/Microsoft.CognitiveServices/accounts/ai102-aiservices" \
  --group-id account \
  --connection-name ai102-connection
```

**Explicación**:
- `az network private-endpoint create`: Restringe el acceso al recurso Azure AI Services a la red virtual.

**Documentación**:
- [az network vnet](https://learn.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest)
- [az ml workspace update](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest)
- [az network private-endpoint](https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint?view=azure-cli-latest)

## 4. Sistemas Multi-Agente

Configurar un sistema multi-agente en Azure AI Foundry:

```bash
cat > multi-agent.yaml << EOF
name: multi-agent-flow
type: flow
agents:
  - name: agent1
    model: azureml:ai102-model:1
  - name: agent2
    model: azureml:gpt-4o:2024-08-01
EOF

az ml flow create \
  --file multi-agent.yaml \
  --resource-group ai102-group \
  --workspace-name ai102-hub
```

**Explicación**:
- `az ml flow create`: Define un flujo multi-agente que combina múltiples modelos en el hub.

**Documentación**: [az ml flow](https://learn.microsoft.com/en-us/cli/azure/ml/flow?view=azure-cli-latest)

## 5. Automatización y Scripts

Crear un script Python para RAG, integrando Azure AI Search y Azure OpenAI:

```bash
cat > rag-script.py << EOF
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_deployment = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")

search_client = SearchClient(search_endpoint, "rag-index", AzureKeyCredential(search_key))
openai_client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    api_key=openai_key,
    api_version="2024-08-01"
)

query = input("Enter your query: ")
results = search_client.search(search_text=query, top=3)
context = "\n".join([result["content"] for result in results])

response = openai_client.chat.completions.create(
    model=openai_deployment,
    messages=[
        {"role": "system", "content": "Answer based on this context: " + context},
        {"role": "user", "content": query}
    ]
)
print(response.choices[0].message.content)
EOF
```

Ejecutar el script:

```bash
# Actualizar .env con Azure AI Search
AZURE_SEARCH_ENDPOINT=$(az search service show --name ai102-search --resource-group ai102-group --query properties.url -o tsv)
AZURE_SEARCH_KEY=$(az search admin-key show --service-name ai102-search --resource-group ai102-group --query primaryKey -o tsv)
echo "AZURE_SEARCH_ENDPOINT=$AZURE_SEARCH_ENDPOINT" >> .env
echo "AZURE_SEARCH_KEY=$AZURE_SEARCH_KEY" >> .env

python rag-script.py
```

**Explicación**:
- `rag-script.py`: Integra Azure AI Search para recuperar documentos y Azure OpenAI para generar respuestas basadas en el contexto.
- Usa `.env` de **Parte 1** (Section 3.4.4) y agrega credenciales de Azure AI Search.

**Documentación**: [Azure SDK for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/)

## 6. Computer Vision Solutions

### 6.1. Análisis de Imágenes

Analizar una imagen usando Azure AI Vision:

```bash
az cognitiveservices account vision analyze \
  --name ai102-vision \
  --resource-group ai102-group \
  --image-url "https://example.com/image.jpg" \
  --visual-features Tags,Description
```

**Explicación**:
- `az cognitiveservices account vision analyze`: Analiza imágenes para etiquetas y descripciones.

### 6.2. Modelos de Visión Personalizados

Crear un proyecto de Custom Vision:

```bash
az cognitiveservices account create \
  --name ai102-customvision \
  --resource-group ai102-group \
  --location eastus2 \
  --kind CustomVision.Training \
  --sku S0 \
  --yes
```

**Explicación**:
- `--kind CustomVision.Training`: Crea un recurso para entrenar modelos de visión personalizados.

**Documentación**: [az cognitiveservices account](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest)

## 7. Procesamiento de Lenguaje Natural (NLP)

Realizar análisis de texto:

```bash
az cognitiveservices account language text-analytics \
  --name ai102-language \
  --resource-group ai102-group \
  --text "Este producto es excelente!" \
  --kind SentimentAnalysis
```

**Explicación**:
- `az cognitiveservices account language text-analytics`: Analiza sentimientos u otras tareas de NLP.

**Documentación**: [az cognitiveservices account language](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest)

## 8. IA Responsable

### 8.1. Moderación de Contenido

Crear un recurso Content Moderator:

```bash
az cognitiveservices account create \
  --name ai102-contentmoderator \
  --resource-group ai102-group \
  --location global \
  --kind ContentModerator \
  --sku S0 \
  --yes
```

Moderar texto:

```bash
az cognitiveservices contentmoderator text-moderation \
  --name ai102-contentmoderator \
  --resource-group ai102-group \
  --text "Texto a moderar"
```

**Explicación**:
- `az cognitiveservices contentmoderator text-moderation`: Detecta contenido inapropiado.

### 8.2. Configuración de IA Responsable

Configurar filtros de contenido en Azure OpenAI:

```bash
az cognitiveservices account update \
  --name ai102-aiservices \
  --resource-group ai102-group \
  --custom-properties "{\"contentFilter\": {\"filterType\": \"BlockList\", \"blockList\": [\"contenido-peligroso\"]}}"
```

**Explicación**:
- `az cognitiveservices account update`: Aplica filtros de contenido para cumplir con políticas de IA responsable.

**Documentación**:
- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest)
- [az cognitiveservices contentmoderator](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/contentmoderator?view=azure-cli-latest)

## 9. Solución de Problemas

Verificar el estado de los recursos:

```bash
az resource list --resource-group ai102-group --output table
```

Consultar registros de actividad:

```bash
az monitor activity-log list --resource-group ai102-group --offset 90d
```

**Explicación**:
- `az resource list`: Muestra el estado de los recursos.
- `az monitor activity-log list`: Diagnostica problemas mediante registros.

**Documentación**:
- [az resource list](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest)
- [az monitor activity-log](https://learn.microsoft.com/en-us/cli/azure/monitor/activity-log?view=azure-cli-latest)

## 10. Recursos Adicionales

- [Documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Azure AI Foundry Concepts](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/)