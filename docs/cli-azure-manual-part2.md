# Manual de la CLI de Azure para Desarrollo de IA (AI-102) - Parte 2: Servicios de IA y RAG

Este manual, dividido en tres partes, está diseñado para preparar la certificación **AI-102: Designing and Implementing a Microsoft Azure AI Solution**, cubriendo todos los temas del [syllabus del curso AI-102](https://learn.microsoft.com/es-es/training/courses/ai-102t00#course-syllabus). La **Parte 2** se centra en la gestión de **Azure AI Services** (Lenguaje, Visión, OpenAI, Búsqueda y Bot Service) y **Retrieval-Augmented Generation (RAG)** usando la **Azure CLI**, eliminando la dependencia de interfaces gráficas como Azure AI Foundry. Incluye comandos para crear recursos, gestionar modelos, y configurar RAG, alineados con los objetivos de AI-102 para procesamiento de lenguaje natural, visión computacional, minería de conocimiento y IA conversacional. Los comandos están basados en Azure CLI 2.63.0 (agosto 2025), según la [documentación oficial](https://learn.microsoft.com/en-us/cli/azure/reference-docs-index?view=azure-cli-latest). La **Parte 1** cubrió fundamentos y gestión de recursos, mientras que la **Parte 3** abordará flujos de trabajo avanzados y IA responsable.

## Tabla de Contenidos

1. [Azure AI Services](#1-azure-ai-services)
   1. [Azure AI Language](#11-azure-ai-language)
   2. [Azure AI Vision](#12-azure-ai-vision)
   3. [Azure OpenAI Service](#13-azure-openai-service)
   4. [Azure AI Search](#14-azure-ai-search)
   5. [Azure Bot Service](#15-azure-bot-service)
2. [Retrieval-Augmented Generation (RAG)](#2-retrieval-augmented-generation-rag)
3. [Recursos Adicionales](#3-recursos-adicionales)

## 1. Azure AI Services

Esta sección cubre la creación y gestión de recursos de Azure AI Services usando Azure CLI, incluyendo servicios de lenguaje, visión, OpenAI, búsqueda y bots, esenciales para las soluciones de IA de AI-102.

### 1.1. Azure AI Language

Cree un recurso para Azure AI Language (anteriormente Cognitive Services Language) para tareas como análisis de texto, extracción de entidades y traducción.

```bash
az cognitiveservices account create \
  --name ai102-language \
  --resource-group ai102-group \
  --location eastus2 \
  --kind Language \
  --sku S0 \
  --yes
```

**Explicación**:
- `--kind Language`: Crea un recurso para análisis de lenguaje natural (e.g., análisis de sentimientos, NER, traducción).

Obtener clave y endpoint:

```bash
# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name ai102-language \
  --resource-group ai102-group

# Obtener el punto de conexión
az cognitiveservices account show \
  --name ai102-language \
  --resource-group ai102-group \
  --query properties.endpoint -o tsv
```

**Explicación**:
- `az cognitiveservices account keys list`: Devuelve las claves de API para autenticar solicitudes.
- `az cognitiveservices account show`: Obtiene el endpoint del recurso.

**Documentación**:
- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account keys list](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/keys?view=azure-cli-latest#az-cognitiveservices-account-keys-list)

### 1.2. Azure AI Vision

Cree un recurso para Azure AI Vision para análisis de imágenes y videos.

```bash
az cognitiveservices account create \
  --name ai102-vision \
  --resource-group ai102-group \
  --location eastus2 \
  --kind ComputerVision \
  --sku S0 \
  --yes
```

**Explicación**:
- `--kind ComputerVision`: Crea un recurso para tareas de visión como OCR, análisis de imágenes y detección de objetos.

Obtener clave y endpoint:

```bash
# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name ai102-vision \
  --resource-group ai102-group

# Obtener el punto de conexión
az cognitiveservices account show \
  --name ai102-vision \
  --resource-group ai102-group \
  --query properties.endpoint -o tsv
```

**Explicación**:
- Similar a Azure AI Language, estos comandos obtienen credenciales para interactuar con el servicio de visión.

**Documentación**:
- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account keys list](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/keys?view=azure-cli-latest#az-cognitiveservices-account-keys-list)

### 1.3. Azure OpenAI Service

Azure OpenAI Service permite acceder a modelos de lenguaje avanzados como GPT-4o, ya sea de forma independiente (standalone) o integrado con Azure AI Foundry.

#### 1.3.1. Standalone Azure OpenAI

Para aplicaciones que solo requieren modelos de OpenAI sin Azure AI Foundry:

```bash
# Crear un recurso Azure OpenAI
az cognitiveservices account create \
  --name openai-standalone \
  --resource-group ai102-group \
  --location eastus2 \
  --kind OpenAI \
  --sku S0 \
  --yes

# Desplegar el modelo GPT-4o
az cognitiveservices account deployment create \
  --name openai-standalone \
  --resource-group ai102-group \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version 2024-08-01 \
  --sku-name Standard \
  --sku-capacity 50
```

**Explicación**:
- `--kind OpenAI`: Crea un recurso Azure OpenAI independiente.
- `az cognitiveservices account deployment create`: Despliega el modelo `gpt-4o` con 50K TPM.

#### 1.3.2. Azure OpenAI en Azure AI Foundry

Para usar Azure OpenAI dentro de Azure AI Foundry, utilice el recurso creado en **Parte 1** (Section 3.4.2) y conéctelo al hub:

```bash
# Crear una conexión al recurso Azure AI Services
az ml connection create \
  --name openai-connection \
  --resource-group ai102-group \
  --workspace-name ai102-hub \
  --type AzureOpenAI \
  --target "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/ai102-group/providers/Microsoft.CognitiveServices/accounts/ai102-aiservices"
```

**Explicación**:
- `az ml connection create`: Conecta el recurso Azure AI Services (`ai102-aiservices`) al hub (`ai102-hub`) para usar modelos en proyectos basados en hub.

#### 1.3.3. Gestión de Modelos, Endpoints y Claves

##### Obtener Claves de Acceso y Endpoint

```bash
# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name ai102-aiservices \
  --resource-group ai102-group

# Obtener el punto de conexión
az cognitiveservices account show \
  --name ai102-aiservices \
  --resource-group ai102-group \
  --query properties.endpoint -o tsv
```

**Explicación**:
- `az cognitiveservices account keys list`: Devuelve las claves de API (key1 y key2) para autenticar solicitudes.
- `az cognitiveservices account show --query properties.endpoint`: Obtiene el endpoint del recurso Azure AI Services.

##### Listar Modelos Disponibles

Listar modelos que contengan "gpt" (insensible a mayúsculas):

```bash
az cognitiveservices account list-models \
  --name ai102-aiservices \
  --resource-group ai102-group | \
  jq '.[] | select(.name | test("gpt"; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    sku: .skus[0].name, 
    capacity: .skus[0].capacity.default,
    model_category: (
      if (.capabilities | type == "array") then
        if (.capabilities | contains(["ChatCompletion"])) then "Chat"
        elif (.capabilities | contains(["Embedding"])) then "Embeddings" 
        elif (.capabilities | contains(["Completion"])) then "Text Completion"
        else (.capabilities | join(", "))
        end
      else .capabilities
      end
    )
  }'
```

Listar modelos que contengan "ada" (insensible a mayúsculas):

```bash
az cognitiveservices account list-models \
  --name ai102-aiservices \
  --resource-group ai102-group | \
  jq '.[] | select(.name | test("ada"; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    capabilities: .capabilities
  }'
```

Listar modelos que contengan "gpt", "ada" o "davinci" (insensible a mayúsculas):

```bash
az cognitiveservices account list-models \
  --name ai102-aiservices \
  --resource-group ai102-group | \
  jq '.[] | select(.name | test("gpt|ada|davinci"; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    model_category: (
      if (.capabilities | type == "array") then
        if (.capabilities | contains(["ChatCompletion"])) then "Chat"
        elif (.capabilities | contains(["Embedding"])) then "Embeddings" 
        elif (.capabilities | contains(["Completion"])) then "Text Completion"
        else (.capabilities | join(", "))
        end
      else .capabilities
      end
    )
  }'
```

Listar modelos con un patrón específico (insensible a mayúsculas):

```bash
# Reemplaza "PATRON" con lo que quieras buscar
az cognitiveservices account list-models \
  --name ai102-aiservices \
  --resource-group ai102-group | \
  jq --arg pattern "PATRON" '.[] | select(.name | test($pattern; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    capabilities: .capabilities
  }'
```

**Explicación**:
- `az cognitiveservices account list-models`: Lista todos los modelos disponibles en el recurso Azure OpenAI.
- `jq`: Filtra y formatea la salida JSON para mostrar modelos que coincidan con patrones como "gpt", "ada", "davinci", o un patrón personalizado, con detalles como nombre, versión, formato y capacidades (e.g., Chat, Embeddings, Text Completion).
- Requiere `jq` instalado (ver **Parte 1**, Section 2.1).

**Documentación**:
- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account deployment create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest#az-cognitiveservices-account-deployment-create)
- [az ml connection create](https://learn.microsoft.com/en-us/cli/azure/ml/connection?view=azure-cli-latest#az-ml-connection-create)
- [az cognitiveservices account keys list](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/keys?view=azure-cli-latest#az-cognitiveservices-account-keys-list)
- [az cognitiveservices account list-models](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-list-models)

### 1.4. Azure AI Search

Cree un recurso Azure AI Search para indexación y recuperación de datos, usado en aplicaciones RAG.

```bash
az search service create \
  --name ai102-search \
  --resource-group ai102-group \
  --location eastus2 \
  --sku Standard \
  --partition-count 1 \
  --replica-count 1
```

**Explicación**:
- `az search service create`: Crea un servicio de búsqueda para indexar datos y habilitar búsqueda semántica.

Obtener clave y endpoint:

```bash
# Obtener la clave de administración
az search admin-key show \
  --service-name ai102-search \
  --resource-group ai102-group

# Obtener el punto de conexión
az search service show \
  --name ai102-search \
  --resource-group ai102-group \
  --query properties.url -o tsv
```

**Explicación**:
- `az search admin-key show`: Devuelve la clave para administrar el servicio de búsqueda.
- `az search service show`: Obtiene el endpoint del servicio.

**Documentación**:
- [az search service create](https://learn.microsoft.com/en-us/cli/azure/search/service?view=azure-cli-latest#az-search-service-create)
- [az search admin-key show](https://learn.microsoft.com/en-us/cli/azure/search/admin-key?view=azure-cli-latest#az-search-admin-key-show)

### 1.5. Azure Bot Service

Cree un bot para aplicaciones conversacionales:

```bash
az bot create \
  --name ai102-bot \
  --resource-group ai102-group \
  --location eastus2 \
  --kind WebApp \
  --sku S1 \
  --app-type SingleTenant \
  --app-id <app-id> \
  --password <app-password>
```

**Explicación**:
- `az bot create`: Crea un bot basado en una aplicación web.
- Reemplace `<app-id>` y `<app-password>` con credenciales de una aplicación registrada en Azure AD.

**Documentación**: [az bot create](https://learn.microsoft.com/en-us/cli/azure/bot?view=azure-cli-latest#az-bot-create)

## 2. Retrieval-Augmented Generation (RAG)

RAG combina recuperación de información con generación de texto para mejorar respuestas de modelos de lenguaje. Azure AI Search se usa para indexar datos, y Azure OpenAI proporciona el modelo generativo.

### 2.1. Configurar un Índice en Azure AI Search

Crear un índice para datos de ejemplo:

```bash
# Crear archivo JSON para el índice
cat > rag-index.json << EOF
{
  "name": "rag-index",
  "fields": [
    {"name": "id", "type": "Edm.String", "key": true, "searchable": false},
    {"name": "content", "type": "Edm.String", "searchable": true, "filterable": false},
    {"name": "metadata", "type": "Edm.String", "searchable": true}
  ]
}
EOF

# Crear el índice
az search index create \
  --name rag-index \
  --service-name ai102-search \
  --resource-group ai102-group \
  --definition @rag-index.json
```

**Explicación**:
- `rag-index.json`: Define un índice con campos para ID, contenido y metadatos.
- `az search index create`: Crea el índice en el servicio Azure AI Search.

### 2.2. Cargar Datos en el Índice

Cargar datos de ejemplo:

```bash
# Crear archivo JSON con datos
cat > rag-data.json << EOF
{
  "value": [
    {
      "id": "1",
      "content": "Azure AI Foundry es una plataforma para aplicaciones de IA generativa.",
      "metadata": "azure, ai, foundry"
    },
    {
      "id": "2",
      "content": "Azure OpenAI proporciona acceso a modelos como GPT-4o.",
      "metadata": "openai, gpt"
    }
  ]
}
EOF

# Cargar datos al índice
az search document create \
  --index-name rag-index \
  --service-name ai102-search \
  --resource-group ai102-group \
  --data @rag-data.json
```

**Explicación**:
- `rag-data.json`: Contiene documentos de ejemplo para indexar.
- `az search document create`: Carga los documentos al índice.

### 2.3. Integrar con Azure OpenAI

Utilice el endpoint y la clave de Azure OpenAI (`ai102-aiservices`) desde **Parte 1** (Section 3.4.4) y el índice de Azure AI Search para implementar RAG. Un ejemplo de código Python se cubrirá en **Parte 3** (Automatización y Scripts).

**Documentación**:
- [az search index create](https://learn.microsoft.com/en-us/cli/azure/search/index?view=azure-cli-latest#az-search-index-create)
- [az search document create](https://learn.microsoft.com/en-us/cli/azure/search/document?view=azure-cli-latest#az-search-document-create)

## 3. Recursos Adicionales

- [Documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Azure AI Foundry Concepts](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/)