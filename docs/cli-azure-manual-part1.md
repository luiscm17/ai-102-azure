# Manual de la CLI de Azure para Desarrollo de IA (AI-102) - Parte 1: Fundamentos y Gestión de Recursos

Este manual, dividido en tres partes, está diseñado para preparar la certificación **AI-102: Designing and Implementing a Microsoft Azure AI Solution**, cubriendo todos los temas del [syllabus del curso AI-102](https://learn.microsoft.com/es-es/training/courses/ai-102t00#course-syllabus). Se enfoca en el uso de la **Azure CLI** para gestionar recursos de Azure relacionados con inteligencia artificial, eliminando la dependencia de interfaces gráficas como Azure AI Foundry. La **Parte 1** cubre la introducción, instalación, configuración y gestión de recursos básicos, incluyendo Azure AI Foundry y sus tipos de recursos. Las partes siguientes abordarán servicios de IA, RAG, y temas avanzados como sistemas multi-agente y IA responsable. Cada sección incluye explicaciones didácticas, comandos actualizados según la [documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/reference-docs-index?view=azure-cli-latest) para Azure CLI 2.63.0 (agosto 2025), y enlaces a documentación.

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Instalación y Configuración](#2-instalación-y-configuración)
   1. [Instalación](#21-instalación)
   2. [Configuración Inicial](#22-configuración-inicial)
3. [Gestión de Recursos Básicos](#3-gestión-de-recursos-básicos)
   1. [Tipos de Recursos de Azure para IA](#31-tipos-de-recursos-de-azure-para-ia)
   2. [Grupos de Recursos](#32-grupos-de-recursos)
   3. [Recursos Generales](#33-recursos-generales)
   4. [Azure AI Foundry](#34-azure-ai-foundry)
4. [Recursos Adicionales](#4-recursos-adicionales)

## 1. Introducción

La certificación **AI-102** valida habilidades para diseñar e implementar soluciones de IA en Azure, incluyendo visión computacional, procesamiento de lenguaje natural (NLP), minería de conocimiento, IA conversacional, y prácticas de IA responsable. Este manual utiliza la **Azure CLI** para gestionar recursos y flujos de trabajo, eliminando la dependencia del portal Azure AI Foundry. La **Parte 1** cubre la configuración inicial y la gestión de recursos básicos, incluyendo la creación de un hub y proyecto en Azure AI Foundry, esenciales para aplicaciones de IA generativa. Los comandos están basados en Azure CLI 2.63.0, asegurando compatibilidad con los últimos servicios de Azure.

**Documentación**: [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)

## 2. Instalación y Configuración

### 2.1. Instalación

Instale Azure CLI 2.63.0 para gestionar recursos de Azure:

```bash
# Linux/macOS
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
```

Instale la extensión `ml` para Azure Machine Learning y `jq` para procesar JSON:

```bash
az extension add -n ml
# Linux/macOS
sudo apt-get install jq  # Debian/Ubuntu
brew install jq         # macOS
# Windows
choco install jq
```

**Explicación**:
- La extensión `ml` es necesaria para comandos como `az ml workspace`, `az ml online-endpoint`, y `az ml online-deployment`, usados en Azure AI Foundry y Azure Machine Learning.
- `jq` es requerido para filtrar listas de modelos en Azure OpenAI (e.g., `az cognitiveservices account list-models`).
- Verifique la instalación con `az --version` y `jq --version`.

**Documentación**: 
- [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [az extension add](https://learn.microsoft.com/en-us/cli/azure/extension?view=azure-cli-latest#az-extension-add)
- [jq Installation](https://stedolan.github.io/jq/download/)

### 2.2. Configuración Inicial

Autentíquese en Azure con permisos de **Owner**:

```bash
az login
```

Configure el entorno por defecto:

```bash
az configure --defaults group=ai102-group location=eastus2
```

**Explicación**:
- `az login`: Autentica al usuario con credenciales de Azure.
- `az configure`: Establece valores por defecto para el grupo de recursos y la región, simplificando comandos posteriores.

**Documentación**: 
- [az login](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-login)
- [az configure](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-configure)

## 3. Gestión de Recursos Básicos

### 3.1. Tipos de Recursos de Azure para IA

Azure soporta varios tipos de recursos para aplicaciones de IA, cada uno con propósitos específicos según el caso de uso, relevantes para la certificación AI-102:

- **Azure AI Foundry resource**: Recurso principal para desarrollar, desplegar y gestionar aplicaciones de IA generativa. Proporciona acceso a servicios de agentes, modelos con hosting serverless, evaluaciones y Azure OpenAI APIs. Es el recurso recomendado para aplicaciones avanzadas en Azure AI Foundry.
- **Azure AI Hub**: Un espacio de trabajo de Azure Machine Learning especializado para hosting y ajuste fino de modelos open-source, junto con capacidades de Azure Machine Learning. Al crear un hub, se provisiona automáticamente un recurso Azure AI Foundry. Se usa para proyectos basados en hubs (hub-based projects).
- **Azure OpenAI**: Recurso especializado para acceder a modelos de OpenAI (e.g., GPT-4o). Puede usarse de forma independiente (standalone) o conectado a Azure AI Foundry para acceder a modelos desde proyectos basados en hubs.
- **Azure AI Search**: Recurso para indexación y recuperación de datos, usado en aplicaciones de Retrieval-Augmented Generation (RAG) conectadas a Azure AI Foundry.

**Cuándo usar cada recurso**:
- **Standalone Azure OpenAI**: Para aplicaciones que solo requieren modelos de OpenAI sin las capacidades completas de Azure AI Foundry (e.g., aplicaciones simples de chat).
- **Azure AI Foundry con Hub**: Para aplicaciones de IA generativa avanzadas que requieren agentes, modelos personalizados, ajuste fino, o integración con Azure Machine Learning.
- **Azure AI Search**: Para aplicaciones que implementan RAG o búsqueda semántica.

**Documentación**: [Choose an Azure resource type for AI foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/resource-types)

### 3.2. Grupos de Recursos

Crear un grupo de recursos:

```bash
az group create --name ai102-group --location eastus2
```

Eliminar un grupo de recursos:

```bash
az group delete --name ai102-group --yes --no-wait
```

**Explicación**:
- `az group create`: Crea un contenedor para todos los recursos de Azure.
- `az group delete`: Elimina el grupo y todos los recursos asociados, útil para limpiar después de pruebas.

**Documentación**: 
- [az group create](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-create)
- [az group delete](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-delete)

### 3.3. Recursos Generales

Crear un recurso genérico, como una cuenta de almacenamiento:

```bash
az resource create \
  --resource-group ai102-group \
  --resource-type Microsoft.Storage/storageAccounts \
  --name ai102storage \
  --location eastus2 \
  --properties '{"sku": {"name": "Standard_LRS"}, "kind": "StorageV2"}'
```

**Explicación**:
- `az resource create`: Crea recursos genéricos especificando el tipo y propiedades, útil para recursos no cubiertos por comandos específicos.

**Documentación**: [az resource create](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-create)

### 3.4. Azure AI Foundry

Azure AI Foundry es una plataforma para desarrollar aplicaciones de IA generativa, utilizando hubs y proyectos basados en hubs para organizar cargas de trabajo. Esta sección muestra cómo crear un hub, un proyecto, y un recurso Azure AI Services para OpenAI, configurando variables de entorno para su uso.

#### 3.4.1. Crear un Azure AI Foundry Hub y Proyecto

```bash
# Crear un grupo de recursos
az group create --name ai102-group --location eastus2

# Crear un Azure AI Foundry hub
az ml workspace create \
  --kind hub \
  --name ai102-hub \
  --resource-group ai102-group \
  --location eastus2 \
  --display-name "AI102 Hub"

# Crear un proyecto basado en hub
az ml workspace create \
  --kind project \
  --name ai102-project \
  --resource-group ai102-group \
  --location eastus2 \
  --hub-id "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/ai102-group/providers/Microsoft.MachineLearningServices/workspaces/ai102-hub" \
  --display-name "AI102 Project"
```

**Explicación**:
- `az ml workspace create --kind hub`: Crea un hub, que es un espacio de trabajo de Azure Machine Learning con capacidades adicionales para IA generativa, provisionando automáticamente un recurso Azure AI Foundry.
- `az ml workspace create --kind project`: Crea un proyecto bajo el hub, usado para organizar cargas de trabajo de IA.
- `--hub-id`: Vincula el proyecto al hub. Reemplace `$AZURE_SUBSCRIPTION_ID` con su ID de suscripción (obtenga con `az account show --query id -o tsv`).

#### 3.4.2. Crear un Recurso Azure AI Services para OpenAI en Azure AI Foundry

```bash
az cognitiveservices account create \
  --name ai102-aiservices \
  --resource-group ai102-group \
  --location eastus2 \
  --kind OpenAI \
  --sku S0 \
  --yes
```

**Explicación**:
- `--kind OpenAI`: Crea un recurso Azure AI Services para acceder a modelos como GPT-4o, integrable con Azure AI Foundry.

#### 3.4.3. Desplegar un Modelo en Azure AI Foundry

Despliegue el modelo `gpt-4o` en el proyecto:

```bash
# Crear archivo YAML para el despliegue
cat > chat-deployment.yaml << EOF
name: gpt-4o
endpoint_name: ai102-endpoint
model:
  name: gpt-4o
  version: 2024-08-01
sku_name: Standard
sku_capacity: 50
EOF

# Crear un endpoint
az ml online-endpoint create \
  --name ai102-endpoint \
  --resource-group ai102-group \
  --workspace-name ai102-hub

# Desplegar el modelo
az ml online-deployment create \
  --file chat-deployment.yaml \
  --resource-group ai102-group \
  --workspace-name ai102-hub
```

**Explicación**:
- `chat-deployment.yaml`: Define el despliegue del modelo `gpt-4o` con capacidad de 50K TPM (Tokens Per Minute).
- `az ml online-endpoint create`: Crea un endpoint para el modelo.
- `az ml online-deployment create`: Despliega el modelo en el endpoint.

#### 3.4.4. Configurar Variables de Entorno

```bash
AI_SERVICES_NAME=ai102-aiservices
AZURE_OPENAI_ENDPOINT=$(az cognitiveservices account show --name $AI_SERVICES_NAME --resource-group ai102-group --query properties.endpoint -o tsv)
AZURE_OPENAI_API_KEY=$(az cognitiveservices account keys list --name $AI_SERVICES_NAME --resource-group ai102-group --query key1 -o tsv)
cat > .env << EOF
AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY
AZURE_OPENAI_MODEL_DEPLOYMENT=gpt-4o
AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID
AZURE_RESOURCE_GROUP=ai102-group
AZURE_LOCATION=eastus2
AZURE_AI_HUB_NAME=ai102-hub
AZURE_AI_PROJECT_NAME=ai102-project
EOF
```

**Explicación**:
- `az cognitiveservices account show`: Obtiene el endpoint del recurso Azure AI Services.
- `az cognitiveservices account keys list`: Obtiene la clave de API.
- Actualiza `.env` con los valores necesarios para aplicaciones de IA, como chatbots.

**Documentación**:
- [az ml workspace](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest)
- [az cognitiveservices account](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest)
- [az ml online-endpoint](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest)
- [az ml online-deployment](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest)

## 4. Recursos Adicionales

- [Documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Choose an Azure resource type for AI foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/resource-types)