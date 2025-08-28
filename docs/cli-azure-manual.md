# Manual de la CLI de Azure para Desarrollo de IA (AI-102)

Este manual está diseñado para preparar la certificación **AI-102: Designing and Implementing a Microsoft Azure AI Solution**, cubriendo todos los temas del [syllabus del curso AI-102](https://learn.microsoft.com/es-es/training/courses/ai-102t00#course-syllabus). Se enfoca en el uso de la **Azure CLI** para gestionar recursos de Azure relacionados con inteligencia artificial, eliminando la dependencia de interfaces gráficas como Azure AI Foundry. El manual abarca desde tareas básicas (instalación, autenticación, gestión de recursos) hasta temas avanzados como **Retrieval-Augmented Generation (RAG)**, agentes de IA, sistemas multi-agente, visión computacional, procesamiento de lenguaje natural (NLP), minería de conocimiento, IA conversacional, y prácticas de IA responsable. Cada sección incluye explicaciones didácticas, comandos actualizados según la [documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/reference-docs-index?view=azure-cli-latest), y enlaces directos a la documentación correspondiente.

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Instalación y Configuración](#2-instalación-y-configuración)
   1. [Instalación](#21-instalación)
   2. [Configuración Inicial](#22-configuración-inicial)
3. [Gestión de Recursos Básicos](#3-gestión-de-recursos-básicos)
   1. [Grupos de Recursos](#31-grupos-de-recursos)
   2. [Recursos Generales](#32-recursos-generales)
   3. [Azure AI Foundry](#33-azure-ai-foundry)
4. [Azure AI Services](#4-azure-ai-services)
   1. [Azure AI Language](#41-azure-ai-language)
   2. [Azure AI Vision](#42-azure-ai-vision)
   3. [Azure OpenAI Service](#43-azure-openai-service)
   4. [Azure AI Search](#44-azure-ai-search)
   5. [Azure Bot Service](#45-azure-bot-service)
5. [Retrieval-Augmented Generation (RAG)](#5-retrieval-augmented-generation-rag)
6. [Azure Machine Learning](#6-azure-machine-learning)
   1. [Crear un Espacio de Trabajo](#61-crear-un-espacio-de-trabajo)
   2. [Desplegar un Modelo](#62-desplegar-un-modelo)
7. [Bases de Datos para IA](#7-bases-de-datos-para-ia)
   1. [Azure Cosmos DB](#71-azure-cosmos-db)
   2. [Azure Database for PostgreSQL](#72-azure-database-for-postgresql)
   3. [Azure Database for MySQL](#73-azure-database-for-mysql)
   4. [Azure SQL Database](#74-azure-sql-database)
8. [Redes y Seguridad](#8-redes-y-seguridad)
   1. [Redes Virtuales](#81-redes-virtuales)
   2. [Identidades Administradas](#82-identidades-administradas)
   3. [Puntos de Conexión Privados](#83-puntos-de-conexión-privados)
9. [Sistemas Multi-Agente](#9-sistemas-multi-agente)
10. [Automatización y Scripts](#10-automatización-y-scripts)
11. [Computer Vision Solutions](#11-computer-vision-solutions)
    1. [Análisis de Imágenes](#111-análisis-de-imágenes)
    2. [Modelos de Visión Personalizados](#112-modelos-de-visión-personalizados)
12. [Procesamiento de Lenguaje Natural (NLP)](#12-procesamiento-de-lenguaje-natural-nlp)
    1. [Análisis de Texto](#121-análisis-de-texto)
    2. [Procesamiento de Voz](#122-procesamiento-de-voz)
    3. [Modelos de Lenguaje Personalizados](#123-modelos-de-lenguaje-personalizados)
13. [IA Responsable](#13-ia-responsable)
    1. [Moderación de Contenido](#131-moderación-de-contenido)
    2. [Configuración de IA Responsable](#132-configuración-de-ia-responsable)
14. [Solución de Problemas](#14-solución-de-problemas)
15. [Recursos Adicionales](#15-recursos-adicionales)

## 1. Introducción

La **Azure CLI** es una herramienta de línea de comandos que permite gestionar recursos de Azure de forma eficiente, ideal para automatización y preparación para la certificación AI-102. Este manual cubre todos los módulos del curso AI-102:

1. **Planificación y gestión de soluciones de IA**: Crear y administrar recursos de Azure AI.
2. **Soluciones de visión computacional**: Implementar Azure AI Vision y Custom Vision.
3. **Procesamiento de lenguaje natural (NLP)**: Configurar Azure AI Language, Speech Services y LUIS.
4. **Minería de conocimiento**: Usar Azure AI Search y RAG.
5. **IA conversacional**: Crear bots con Azure Bot Service.
6. **IA responsable**: Implementar moderación de contenido y límites de seguridad.

Cada sección incluye comandos prácticos, explicaciones de parámetros y enlaces a la documentación oficial.

## 2. Instalación y Configuración

### 2.1. Instalación

La Azure CLI es compatible con Windows, macOS y Linux. Instala la versión más reciente según tu sistema operativo.

#### Windows

```bash
# Instalar con winget
winget install -e --id Microsoft.AzureCLI
```

**Explicación**: Usa `winget`, el administrador de paquetes de Windows. La opción `-e` asegura una coincidencia exacta con el ID del paquete.

**Documentación**: [Instalar Azure CLI en Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?view=azure-cli-latest)

#### macOS (Homebrew)

```bash
# Instalar con Homebrew
brew update && brew install azure-cli
```

**Explicación**: `brew update` actualiza Homebrew, y `brew install azure-cli` instala la CLI.

**Documentación**: [Instalar Azure CLI en macOS](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-macos?view=azure-cli-latest)

#### Linux (Ubuntu/Debian)

```bash
# Instalación en Ubuntu/Debian
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Explicación**: Descarga y ejecuta el script de instalación oficial con permisos de administrador.

**Documentación**: [Instalar Azure CLI en Linux](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest)

### 2.2. Configuración Inicial

Configura tu entorno autenticándote y estableciendo valores predeterminados.

```bash
# Iniciar sesión interactiva
az login

# Listar suscripciones disponibles
az account list --output table

# Establecer suscripción por defecto
az account set --subscription "<subscription-name-or-id>"

# Configurar grupo de recursos y región por defecto
az config set defaults.group=<resource-group-name> defaults.location=<location>
```

**Explicación**:

1. `az login`: Abre un navegador para autenticarte en Azure.
2. `az account list`: Muestra tus suscripciones en formato tabla.
3. `az account set`: Selecciona una suscripción activa usando su nombre o ID.
4. `az config set`: Establece valores predeterminados para el grupo de recursos (`defaults.group`) y la región (`defaults.location`, ej., `eastus`).

**Documentación**:

- [az login](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-login)
- [az account list](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-list)
- [az account set](https://learn.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-set)
- [az config set](https://learn.microsoft.com/en-us/cli/azure/config?view=azure-cli-latest#az-config-set)

## 3. Gestión de Recursos Básicos

### 3.1. Grupos de Recursos

Los grupos de recursos organizan recursos de Azure de manera lógica.

```bash
# Crear un grupo de recursos
az group create --name <resource-group-name> --location <location>

# Listar grupos de recursos
az group list --output table

# Eliminar un grupo de recursos
az group delete --name <resource-group-name> --yes --no-wait
```

**Explicación**:

1. `az group create`: Crea un grupo de recursos con un nombre (`--name`) y una región (`--location`, ej., `eastus`).
2. `az group list`: Muestra todos los grupos de recursos en formato tabla.
3. `az group delete`: Elimina un grupo. `--yes` omite la confirmación, y `--no-wait` ejecuta en segundo plano.

**Documentación**:

- [az group create](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-create)
- [az group list](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-list)
- [az group delete](https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-delete)

### 3.2. Recursos Generales

Gestiona recursos individuales dentro de un grupo.

```bash
# Listar todos los recursos en un grupo
az resource list --resource-group <resource-group-name> --output table

# Mostrar detalles de un recurso específico
az resource show --name <resource-name> --resource-group <resource-group-name> --resource-type <provider-namespace>/<resource-type>

# Eliminar un recurso específico
az resource delete --name <resource-name> --resource-group <resource-group-name> --resource-type <provider-namespace>/<resource-type>
```

**Explicación**:

1. `az resource list`: Enumera todos los recursos en un grupo.
2. `az resource show`: Muestra detalles de un recurso, especificando su nombre, grupo y tipo (ej., `Microsoft.CognitiveServices/accounts`).
3. `az resource delete`: Elimina un recurso específico.

**Documentación**:

- [az resource list](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-list)
- [az resource show](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-show)
- [az resource delete](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-delete)

### 3.3. Azure AI Foundry

Azure AI Foundry proporciona herramientas para gestionar proyectos de IA, incluyendo la creación de proyectos, despliegue de modelos y gestión de recursos.

#### Listar modelos disponibles

Antes de desplegar un modelo, es útil listar los modelos disponibles en tu cuenta de Cognitive Services:

```bash
# Listar modelos disponibles con detalles relevantes (usando jq para formateo)
az cognitiveservices account list-models \
  -n <account-name> \
  -g <resource-group-name> | \
  jq '.[] | { 
    name: .name, 
    format: .format, 
    version: .version, 
    sku: .skus[0].name, 
    capacity: .skus[0].capacity.default 
  }'
```

**Nota sobre jq**:

- `jq` es una herramienta de línea de comandos para procesar JSON. Si no la tienes instalada, puedes instalarla con:
  - **Linux**: `sudo apt-get install jq` (Debian/Ubuntu) o `sudo yum install jq` (RHEL/CentOS)
  - **macOS**: `brew install jq`
  - **Windows**: Usa Chocolatey: `choco install jq` o descárgala de [la página oficial de jq](https://stedolan.github.io/jq/)

**Alternativa sin jq**:

```bash
# Usando solo la CLI de Azure (sin jq)
az cognitiveservices account list-models \
  --name <account-name> \
  --resource-group <resource-group-name> \
  --query "[].{ 
    name: name, 
    format: format, 
    version: version, 
    sku: skus[0].name, 
    capacity: skus[0].capacity.default 
  }" \
  --output json
```

**Ejemplo de salida**:

```json
{
  "name": "Phi-3.5-vision-instruct",
  "format": "Microsoft",
  "version": "2",
  "sku": "GlobalStandard",
  "capacity": 1
}
```

**Listar modelos disponibles con detalles relevantes (usando jq para formateo)**:

```bash
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
  jq '.[] | { 
    name: .name, 
    format: .format, 
    version: .version, 
    sku: .skus[0].name, 
    capacity: .skus[0].capacity.default,
    capabilities: .capabilities,
    model_type: (.capabilities | if type == "array" then join(", ") else . end)
  }'
```

**Si quieres ser más específico y categorizar los modelos basándose en sus capacidades, puedes usar esta versión más avanzada**:

```bash
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
  jq '.[] | { 
    name: .name, 
    format: .format, 
    version: .version, 
    sku: .skus[0].name, 
    capacity: .skus[0].capacity.default,
    capabilities: .capabilities,
    model_category: (
      if (.capabilities | type == "array") then
        if (.capabilities | contains(["ChatCompletion"])) then "Chat"
        elif (.capabilities | contains(["Embedding"])) then "Embeddings" 
        elif (.capabilities | contains(["Completion"])) then "Text Completion"
        elif (.capabilities | contains(["ImageGeneration"])) then "Image Generation"
        elif (.capabilities | contains(["TextToSpeech"])) then "Text-to-Speech"
        elif (.capabilities | contains(["SpeechToText"])) then "Speech-to-Text"
        else (.capabilities | join(", "))
        end
      else .capabilities
      end
    )
  }'
```

**Explicación de los campos**:

- `name`: Nombre del modelo (ej. "Phi-3.5-vision-instruct")
- `format`: Formato del modelo (generalmente "Microsoft" para modelos propietarios)
- `version`: Versión del modelo
- `sku`: SKU del modelo (ej. "GlobalStandard")
- `capacity`: Capacidad predeterminada del modelo
- `capabilities`: Capacidad del modelo
- `model_type`: Tipo del modelo
- `model_category`: Categoría del modelo

```bash
# Crear un nuevo proyecto en AI Foundry
az ai project create \
  --name <project-name> \
  --resource-group <resource-group-name> \
  --location <location> \
  --description "Descripción del proyecto"

# Listar todos los proyectos en un grupo de recursos
az ai project list \
  --resource-group <resource-group-name> \
  --output table

# Obtener detalles de un proyecto específico
az ai project show \
  --name <project-name> \
  --resource-group <resource-group-name>

# Crear un despliegue de modelo
az ai model deployment create \
  --name <deployment-name> \
  --project <project-name> \
  --resource-group <resource-group-name> \
  --model-id <model-id> \
  --compute <compute-target> \
  --instance-type <instance-type>

# Listar despliegues en un proyecto
az ai model deployment list \
  --project <project-name> \
  --resource-group <resource-group-name> \
  --output table

# Obtener claves de API y endpoints
az ai project show-keys \
  --name <project-name> \
  --resource-group <resource-group-name>

# Actualizar un proyecto
az ai project update \
  --name <project-name> \
  --resource-group <resource-group-name> \
  --set properties.description="Nueva descripción"

# Eliminar un proyecto (y sus recursos asociados)
az ai project delete \
  --name <project-name> \
  --resource-group <resource-group-name> \
  --yes
```

**Explicación**:

1. `az ai project create`: Crea un nuevo proyecto en AI Foundry con nombre, ubicación y descripción.
2. `az ai project list`: Muestra todos los proyectos en un grupo de recursos.
3. `az ai model deployment create`: Despliega un modelo en el proyecto especificado.
4. `az ai project show-keys`: Muestra las claves de API y endpoints para acceder al proyecto.
5. `az ai project update`: Actualiza las propiedades de un proyecto existente.
6. `az ai project delete`: Elimina un proyecto y sus recursos asociados.

**Documentación**:

- [az ai project](https://learn.microsoft.com/en-us/cli/azure/ai/project?view=azure-cli-latest)
- [az ai model deployment](https://learn.microsoft.com/en-us/cli/azure/ai/model/deployment?view=azure-cli-latest)

## 4. Azure AI Services

Los Azure AI Services ofrecen herramientas para visión, lenguaje, búsqueda y más, esenciales para AI-102.

### 4.1. Azure AI Language

Proporciona capacidades de análisis de texto, como detección de sentimientos y extracción de entidades.

```bash
# Crear un recurso de Azure AI Language
az cognitiveservices account create \
  --name <language-resource-name> \
  --resource-group <resource-group-name> \
  --kind TextAnalytics \
  --sku S \
  --location eastus \
  --yes

# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name <language-resource-name> \
  --resource-group <resource-group-name>

# Obtener el punto de conexión
az cognitiveservices account show \
  --name <language-resource-name> \
  --resource-group <resource-group-name> \
  --query "properties.endpoint"
```

**Buscar modelos que contengan "gpt" (insensible a mayúsculas)**:

```bash
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
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

**Buscar modelos que contengan "ada" (insensible a mayúsculas)**:

```bash
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
  jq '.[] | select(.name | test("ada"; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    capabilities: .capabilities
  }'
```

**Buscar modelos que contengan "gpt", "ada" o "davinci" (insensible a mayúsculas)**:

```bash
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
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

**Buscar modelos que contengan un patrón específico (insensible a mayúsculas)**:

```bash
# Reemplaza "PATRON" con lo que quieras buscar
az cognitiveservices account list-models \
  -n rag-openai-gpt41 \
  -g rg-rag-sdk | \
  jq --arg pattern "PATRON" '.[] | select(.name | test($pattern; "i")) | { 
    name: .name, 
    format: .format, 
    version: .version, 
    capabilities: .capabilities
  }'
```

**Explicación**:

1. `az cognitiveservices account create`: Crea un recurso de tipo `TextAnalytics`. `--sku S` selecciona el nivel estándar, y `--yes` omite confirmaciones.
2. `az cognitiveservices account keys list`: Lista las claves API para autenticar solicitudes.
3. `az cognitiveservices account show`: Obtiene el endpoint del recurso.

**Documentación**:

- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account keys list](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/keys?view=azure-cli-latest#az-cognitiveservices-account-keys-list)
- [az cognitiveservices account show](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-show)

### 4.2. Azure AI Vision

Permite análisis de imágenes y OCR.

```bash
# Crear un recurso de Azure AI Vision
az cognitiveservices account create \
  --name <vision-resource-name> \
  --resource-group <resource-group-name> \
  --kind ComputerVision \
  --sku S1 \
  --location eastus \
  --yes

# Obtener el punto de conexión
az cognitiveservices account show \
  --name <vision-resource-name> \
  --resource-group <resource-group-name> \
  --query "properties.endpoint"
```

**Explicación**:

1. `--kind ComputerVision`: Especifica el servicio de visión.
2. `--sku S1`: Selecciona el nivel estándar para visión.

**Documentación**:

- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account show](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-show)

### 4.3. Azure OpenAI Service

Proporciona acceso a modelos de lenguaje avanzados, como GPT-4o.

```bash
# Crear un recurso de Azure OpenAI
az cognitiveservices account create \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --custom-domain <openai-resource-name> \
  --yes

# Listar modelos disponibles
az cognitiveservices account list-models \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --output table

# Crear un deployment de modelo (ejemplo: GPT-4o)
az cognitiveservices account deployment create \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --deployment-name gpt4o-deployment \
  --model-name gpt-4o \
  --model-version "2024-05-13" \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 1

# Obtener las claves de acceso
az cognitiveservices account keys list \
  --name <openai-resource-name> \
  --resource-group <resource-group-name>

# Obtener el punto de conexión
az cognitiveservices account show \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --query "properties.endpoint"
```

**Explicación**:

1. `--kind OpenAI`: Especifica el servicio OpenAI.
2. `--custom-domain`: Define un nombre personalizado para el endpoint.
3. `az cognitiveservices account list-models`: Lista modelos disponibles para verificar versiones.
4. `az cognitiveservices account deployment create`: Despliega un modelo. `--sku-capacity 1` es adecuado para pruebas.

**Documentación**:

- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices account list-models](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-list-models)
- [az cognitiveservices account deployment create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/deployment?view=azure-cli-latest#az-cognitiveservices-account-deployment-create)
- [az cognitiveservices account keys list](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/keys?view=azure-cli-latest#az-cognitiveservices-account-keys-list)
- [az cognitiveservices account show](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-show)

### 4.4. Azure AI Search

Soporta búsqueda semántica y minería de conocimiento, clave para RAG.

```bash
# Crear un servicio de Azure AI Search
az search service create \
  --name <search-service-name> \
  --resource-group <resource-group-name> \
  --sku Standard \
  --partition-count 1 \
  --replica-count 1 \
  --location eastus

# Crear un índice de búsqueda
az search index create \
  --name <index-name> \
  --resource-group <resource-group-name> \
  --service-name <search-service-name> \
  --fields \
    name=id type=Edm.String key=true \
    name=content type=Edm.String searchable=true
```

**Explicación**:

1. `--sku Standard`: Selecciona el nivel estándar para búsqueda.
2. `az search index create`: Crea un índice con campos como `id` (clave primaria) y `content` (buscable).

**Documentación**:

- [az search service create](https://learn.microsoft.com/en-us/cli/azure/search/service?view=azure-cli-latest#az-search-service-create)
- [az search index create](https://learn.microsoft.com/en-us/cli/azure/search/index?view=azure-cli-latest#az-search-index-create)

### 4.5. Azure Bot Service

Permite crear bots conversacionales integrados con Azure AI.

```bash
# Crear un bot de Azure
az bot create \
  --resource-group <resource-group-name> \
  --name <bot-name> \
  --kind registration \
  --appid "<app-id>" \
  --password "<app-password>" \
  --endpoint "https://<your-web-app>.azurewebsites.net/api/messages" \
  --sku F0

# Publicar el bot
az bot publish \
  --name <bot-name> \
  --resource-group <resource-group-name> \
  --code-dir .
```

**Explicación**:

1. `--kind registration`: Registra un bot sin hosting en Azure.
2. `--appid` y `--password`: Credenciales de Microsoft App Service.
3. `az bot publish`: Publica el código del bot desde el directorio local.

**Documentación**:

- [az bot create](https://learn.microsoft.com/en-us/cli/azure/bot?view=azure-cli-latest#az-bot-create)
- [az bot publish](https://learn.microsoft.com/en-us/cli/azure/bot?view=azure-cli-latest#az-bot-publish)

## 5. Retrieval-Augmented Generation (RAG)

RAG combina búsqueda semántica con generación de texto para respuestas contextualizadas, un tema clave en AI-102.

```bash
# Crear un servicio de Azure AI Search
az search service create \
  --name <search-service-name> \
  --resource-group <resource-group-name> \
  --location eastus \
  --sku Standard \
  --partition-count 1 \
  --replica-count 1

# Crear un índice de búsqueda para RAG
az search index create \
  --name <index-name> \
  --resource-group <resource-group-name> \
  --service-name <search-service-name> \
  --schema @schema.json
```

**schema.json** (ejemplo):

```json
{
  "name": "mi-indice",
  "fields": [
    { "name": "id", "type": "Edm.String", "key": true },
    { "name": "content", "type": "Edm.String", "searchable": true, "retrievable": true },
    { "name": "vector", "type": "Collection(Edm.Single)", "searchable": true, "retrievable": true }
  ]
}
```

```bash
# Crear una fuente de datos para RAG
az search datasource create \
  --name <data-source-name> \
  --resource-group <resource-group-name> \
  --service-name <search-service-name> \
  --type azureblob \
  --data-source-configuration '{"connectionString": "DefaultEndpointsProtocol=https;AccountName=<storage-account>;AccountKey=<storage-key>;EndpointSuffix=core.windows.net", "container": {"name": "<container-name>"}}'

# Crear un indexador para procesar datos
az search indexer create \
  --name <indexer-name> \
  --resource-group <resource-group-name> \
  --service-name <search-service-name> \
  --data-source-name <data-source-name> \
  --target-index-name <index-name>
```

**Explicación**:

1. `az search service create`: Configura un servicio de búsqueda estándar.
2. `az search index create`: Crea un índice con un esquema JSON que define campos para búsqueda semántica.
3. `az search datasource create`: Conecta el índice a un contenedor de Azure Blob Storage.
4. `az search indexer create`: Procesa y carga datos en el índice.

**Documentación**:

- [az search service create](https://learn.microsoft.com/en-us/cli/azure/search/service?view=azure-cli-latest#az-search-service-create)
- [az search index create](https://learn.microsoft.com/en-us/cli/azure/search/index?view=azure-cli-latest#az-search-index-create)
- [az search datasource create](https://learn.microsoft.com/en-us/cli/azure/search/datasource?view=azure-cli-latest#az-search-datasource-create)
- [az search indexer create](https://learn.microsoft.com/en-us/cli/azure/search/indexer?view=azure-cli-latest#az-search-indexer-create)

## 6. Azure Machine Learning

Azure Machine Learning (AML) permite entrenar, implementar y gestionar modelos de IA.

### 6.1. Crear un Espacio de Trabajo

```bash
# Crear un espacio de trabajo de AML
az ml workspace create \
  --name <workspace-name> \
  --resource-group <resource-group-name> \
  --location eastus
```

**Explicación**:

1. `--name`: Nombre del espacio de trabajo.
2. `--location`: Región donde se creará.

**Documentación**: [az ml workspace create](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest#az-ml-workspace-create)

### 6.2. Desplegar un Modelo

```bash
# Crear un endpoint en línea
az ml online-endpoint create \
  --name <endpoint-name> \
  --resource-group <resource-group-name> \
  --workspace-name <workspace-name> \
  --auth-mode key \
  --identity-type SystemAssigned

# Desplegar un modelo
az ml online-deployment create \
  --name <deployment-name> \
  --endpoint-name <endpoint-name> \
  --resource-group <resource-group-name> \
  --workspace-name <workspace-name> \
  --model <model-name>:1 \
  --instance-type Standard_DS3_v2 \
  --no-wait
```

**Explicación**:

1. `az ml online-endpoint create`: Crea un endpoint para inferencia en tiempo real.
2. `az ml online-deployment create`: Despliega un modelo en el endpoint.

**Documentación**:

- [az ml online-endpoint create](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest#az-ml-online-endpoint-create)
- [az ml online-deployment create](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest#az-ml-online-deployment-create)

## 7. Bases de Datos para IA

Las bases de datos son esenciales para almacenar datos de entrenamiento y resultados de modelos.

### 7.1. Azure Cosmos DB

Ideal para datos NoSQL escalables, compatible con RAG.

```bash
# Crear una cuenta de Cosmos DB
az cosmosdb create \
  --name <cosmos-account-name> \
  --resource-group <resource-group-name> \
  --location eastus

# Crear una base de datos SQL
az cosmosdb sql database create \
  --account-name <cosmos-account-name> \
  --name <database-name> \
  --resource-group <resource-group-name>

# Crear un contenedor
az cosmosdb sql container create \
  --account-name <cosmos-account-name> \
  --database-name <database-name> \
  --name <container-name> \
  --partition-key-path "/id" \
  --resource-group <resource-group-name>
```

**Explicación**:

1. `az cosmosdb create`: Crea una cuenta de Cosmos DB.
2. `az cosmosdb sql database create`: Crea una base de datos SQL.
3. `az cosmosdb sql container create`: Crea un contenedor con una clave de partición.

**Documentación**:

- [az cosmosdb create](https://learn.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest#az-cosmosdb-create)
- [az cosmosdb sql database create](https://learn.microsoft.com/en-us/cli/azure/cosmosdb/sql/database?view=azure-cli-latest#az-cosmosdb-sql-database-create)
- [az cosmosdb sql container create](https://learn.microsoft.com/en-us/cli/azure/cosmosdb/sql/container?view=azure-cli-latest#az-cosmosdb-sql-container-create)

### 7.2. Azure Database for PostgreSQL

Soporta `pgvector` para embeddings de IA.

```bash
# Crear un servidor PostgreSQL
az postgres flexible-server create \
  --name <postgres-server-name> \
  --resource-group <resource-group-name> \
  --location eastus \
  --admin-user <admin-user> \
  --admin-password <admin-password> \
  --sku-name Standard_D2s_v3 \
  --version 15

# Habilitar la extensión pgvector
az postgres flexible-server parameter set \
  --name azure.extensions \
  --value vector \
  --resource-group <resource-group-name> \
  --server-name <postgres-server-name>
```

**Explicación**:

1. `az postgres flexible-server create`: Crea un servidor flexible de PostgreSQL.
2. `az postgres flexible-server parameter set`: Activa `pgvector` para embeddings.

**Documentación**:

- [az postgres flexible-server create](https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server?view=azure-cli-latest#az-postgres-flexible-server-create)
- [az postgres flexible-server parameter set](https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server/parameter?view=azure-cli-latest#az-postgres-flexible-server-parameter-set)

### 7.3. Azure Database for MySQL

Base de datos relacional para aplicaciones de IA.

```bash
# Crear un servidor MySQL
az mysql flexible-server create \
  --name <mysql-server-name> \
  --resource-group <resource-group-name> \
  --location eastus \
  --admin-user <admin-user> \
  --admin-password <admin-password> \
  --sku-name Standard_B1ms \
  --version 8.0
```

**Explicación**:

1. `az mysql flexible-server create`: Crea un servidor flexible de MySQL.

**Documentación**: [az mysql flexible-server create](https://learn.microsoft.com/en-us/cli/azure/mysql/flexible-server?view=azure-cli-latest#az-mysql-flexible-server-create)

### 7.4. Azure SQL Database

Base de datos relacional para datos estructurados.

```bash
# Crear un servidor SQL lógico
az sql server create \
  --name <sql-server-name> \
  --resource-group <resource-group-name> \
  --location eastus \
  --admin-user <admin-user> \
  --admin-password <admin-password>

# Crear una base de datos SQL
az sql db create \
  --name <database-name> \
  --resource-group <resource-group-name> \
  --server <sql-server-name> \
  --edition Standard \
  --service-objective S0
```

**Explicación**:

1. `az sql server create`: Crea un servidor lógico SQL.
2. `az sql db create`: Crea una base de datos en el servidor.

**Documentación**:

- [az sql server create](https://learn.microsoft.com/en-us/cli/azure/sql/server?view=azure-cli-latest#az-sql-server-create)
- [az sql db create](https://learn.microsoft.com/en-us/cli/azure/sql/db?view=azure-cli-latest#az-sql-db-create)

## 8. Redes y Seguridad

### 8.1. Redes Virtuales

```bash
# Crear una red virtual
az network vnet create \
  --name <vnet-name> \
  --resource-group <resource-group-name> \
  --location eastus \
  --address-prefix 10.0.0.0/16 \
  --subnet-name <subnet-name> \
  --subnet-prefix 10.0.0.0/24

# Crear un punto de conexión privado
az network private-endpoint create \
  --name <private-endpoint-name> \
  --resource-group <resource-group-name> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id <resource-id> \
  --group-id account \
  --connection-name <connection-name>
```

**Explicación**:

1. `az network vnet create`: Crea una red virtual con un prefijo de dirección y una subred.
2. `az network private-endpoint create`: Configura un endpoint privado para conectar recursos de forma segura.

**Documentación**:

- [az network vnet create](https://learn.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest#az-network-vnet-create)
- [az network private-endpoint create](https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint?view=azure-cli-latest#az-network-private-endpoint-create)

### 8.2. Identidades Administradas

```bash
# Asignar una identidad administrada
az cognitiveservices account identity assign \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --identities '[system]'

# Otorgar permisos a la identidad
az role assignment create \
  --assignee <object-id> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>
```

**Explicación**:

1. `az cognitiveservices account identity assign`: Asigna una identidad administrada al recurso.
2. `az role assignment create`: Otorga permisos a la identidad para acceder a recursos, como blobs de almacenamiento.

**Documentación**:

- [az cognitiveservices account identity assign](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account/identity?view=azure-cli-latest#az-cognitiveservices-account-identity-assign)
- [az role assignment create](https://learn.microsoft.com/en-us/cli/azure/role/assignment?view=azure-cli-latest#az-role-assignment-create)

### 8.3. Puntos de Conexión Privados

```bash
# Crear un punto de conexión privado para Azure OpenAI
az network private-endpoint create \
  --name <private-endpoint-name> \
  --resource-group <resource-group-name> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id /subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.CognitiveServices/accounts/<openai-resource-name> \
  --group-id account \
  --connection-name <connection-name>
```

**Explicación**:

1. `az network private-endpoint create`: Crea un endpoint privado para conectar de forma segura a Azure OpenAI.

**Documentación**: [az network private-endpoint create](https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint?view=azure-cli-latest#az-network-private-endpoint-create)

## 9. Sistemas Multi-Agente

Los sistemas multi-agente coordinan múltiples agentes de IA para tareas complejas.

```bash
# Crear un endpoint para un grupo de agentes
az ml online-endpoint create \
  --name <agent-group-name> \
  --resource-group <resource-group-name> \
  --workspace-name <workspace-name> \
  --auth-mode key \
  --identity-type SystemAssigned

# Desplegar agentes especializados
for agent in analyst researcher executor; do
  az ml online-deployment create \
    --name $agent \
    --endpoint-name <agent-group-name> \
    --resource-group <resource-group-name> \
    --workspace-name <workspace-name> \
    --model <model-name>:1 \
    --instance-type Standard_DS3_v2 \
    --no-wait
done
```

**Explicación**:

1. `az ml online-endpoint create`: Crea un endpoint para agentes.
2. `az ml online-deployment create`: Despliega agentes especializados (analista, investigador, ejecutor).

**Documentación**:

- [az ml online-endpoint create](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest#az-ml-online-endpoint-create)
- [az ml online-deployment create](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest#az-ml-online-deployment-create)

## 10. Automatización y Scripts

Automatiza la creación de recursos con un script Bash.

```bash
#!/bin/bash

# Configuración
RANDOM_SUFFIX=$((RANDOM % 10000))
LOCATION="eastus"
RESOURCE_GROUP_NAME="ai-lab-rg-$RANDOM_SUFFIX"
OPENAI_NAME="openai-$RANDOM_SUFFIX"
SEARCH_NAME="aisearch-$RANDOM_SUFFIX"

# Crear grupo de recursos
echo "Creando grupo de recursos $RESOURCE_GROUP_NAME..."
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Crear recurso de Azure OpenAI
echo "Creando recurso de Azure OpenAI $OPENAI_NAME..."
az cognitiveservices account create \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --kind OpenAI \
  --sku S0 \
  --location $LOCATION \
  --custom-domain $OPENAI_NAME \
  --yes

# Crear servicio de búsqueda
echo "Creando servicio de búsqueda $SEARCH_NAME..."
az search service create \
  --name $SEARCH_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --sku Standard \
  --location $LOCATION

# Mostrar información
echo "Recursos creados:"
echo "- Grupo de recursos: $RESOURCE_GROUP_NAME"
echo "- Azure OpenAI: $OPENAI_NAME"
echo "- Azure AI Search: $SEARCH_NAME"
```

**Explicación**:

1. El script crea un grupo de recursos, un recurso de Azure OpenAI y un servicio de búsqueda.
2. Usa un sufijo aleatorio para evitar conflictos de nombres.

**Documentación**: [Scripting con Azure CLI](https://learn.microsoft.com/en-us/cli/azure/use-cli-effectively)

## 11. Computer Vision Solutions

### 11.1. Análisis de Imágenes

```bash
# Analizar una imagen
az cognitiveservices vision analyze \
  --name <vision-resource-name> \
  --resource-group <resource-group-name> \
  --image-url "https://example.com/image.jpg" \
  --visual-features "Description,Tags,Categories"
```

**Explicación**:

1. `az cognitiveservices vision analyze`: Analiza imágenes para obtener descripciones, etiquetas y categorías.

**Documentación**: [az cognitiveservices vision analyze](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/vision?view=azure-cli-latest#az-cognitiveservices-vision-analyze)

### 11.2. Modelos de Visión Personalizados

```bash
# Crear un proyecto de Custom Vision
az cognitiveservices account create \
  --name <custom-vision-name> \
  --resource-group <resource-group-name> \
  --kind CustomVision.Training \
  --sku S0 \
  --location eastus \
  --yes
```

**Explicación**:

1. `--kind CustomVision.Training`: Crea un recurso para entrenar modelos de visión personalizados.

**Documentación**: [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)

## 12. Procesamiento de Lenguaje Natural (NLP)

### 12.1. Análisis de Texto

```bash
# Analizar sentimiento
az cognitiveservices language analyze-sentiment \
  --name <language-resource-name> \
  --resource-group <resource-group-name> \
  --text "El producto es excelente"

# Extraer entidades
az cognitiveservices language recognize-entities \
  --name <language-resource-name> \
  --resource-group <resource-group-name> \
  --text "Microsoft fue fundada por Bill Gates en 1975"
```

**Explicación**:

1. `az cognitiveservices language analyze-sentiment`: Analiza el sentimiento de un texto.
2. `az cognitiveservices language recognize-entities`: Extrae entidades nombradas del texto.

**Documentación**:

- [az cognitiveservices language analyze-sentiment](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/language?view=azure-cli-latest#az-cognitiveservices-language-analyze-sentiment)
- [az cognitiveservices language recognize-entities](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/language?view=azure-cli-latest#az-cognitiveservices-language-recognize-entities)

### 12.2. Procesamiento de Voz

```bash
# Configurar Azure Speech Service
az cognitiveservices account create \
  --name <speech-resource-name> \
  --resource-group <resource-group-name> \
  --kind SpeechServices \
  --sku S0 \
  --location eastus \
  --yes
```

**Explicación**:

1. `--kind SpeechServices`: Crea un recurso para servicios de voz (TTS y STT).

**Documentación**: [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)

### 12.3. Modelos de Lenguaje Personalizados

```bash
# Crear un recurso de LUIS
az cognitiveservices account create \
  --name <luis-resource-name> \
  --resource-group <resource-group-name> \
  --kind LUIS \
  --sku S0 \
  --location westus \
  --yes
```

**Explicación**:

1. `--kind LUIS`: Crea un recurso para Language Understanding.

**Documentación**: [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)

## 13. IA Responsable

### 13.1. Moderación de Contenido

```bash
# Configurar Azure Content Moderator
az cognitiveservices account create \
  --name <content-moderator-name> \
  --resource-group <resource-group-name> \
  --kind ContentModerator \
  --sku S0 \
  --location global \
  --yes

# Moderar texto
az cognitiveservices contentmoderator text-moderation \
  --name <content-moderator-name> \
  --resource-group <resource-group-name> \
  --text "Texto a moderar"
```

**Explicación**:

1. `az cognitiveservices contentmoderator text-moderation`: Modera contenido textual para detectar lenguaje inapropiado.

**Documentación**:

- [az cognitiveservices account create](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-create)
- [az cognitiveservices contentmoderator text-moderation](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/contentmoderator?view=azure-cli-latest#az-cognitiveservices-contentmoderator-text-moderation)

### 13.2. Configuración de IA Responsable

```bash
# Habilitar características de IA responsable en Azure OpenAI
az cognitiveservices account update \
  --name <openai-resource-name> \
  --resource-group <resource-group-name> \
  --content-filter "{\"filterType\": \"BlockList\", \"blockList\": [\"contenido-peligroso\"]}"
```

**Explicación**:

1. `az cognitiveservices account update`: Configura filtros de contenido para Azure OpenAI.

**Documentación**: [az cognitiveservices account update](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest#az-cognitiveservices-account-update)

## 14. Solución de Problemas

```bash
# Verificar estado de servicios
az resource list --resource-group <resource-group-name> --output table

# Verificar registros de actividad
az monitor activity-log list --resource-group <resource-group-name> --offset 90d
```

**Explicación**:

1. `az resource list`: Muestra el estado de los recursos.
2. `az monitor activity-log list`: Consulta registros de actividad para diagnosticar problemas.

**Documentación**:

- [az resource list](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-list)
- [az monitor activity-log list](https://learn.microsoft.com/en-us/cli/azure/monitor/activity-log?view=azure-cli-latest#az-monitor-activity-log-list)

## 15. Recursos Adicionales

1. [Documentación oficial de Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)
2. [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
3. [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
