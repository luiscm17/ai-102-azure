# Guía de Referencia del SDK de Azure para Python - Parte 1 (AI-102)

Este manual está diseñado para preparar la certificación **AI-102: Designing and Implementing a Microsoft Azure AI Solution**, cubriendo el uso del **Azure SDK para Python** para crear, consumir y gestionar recursos de Azure relacionados con inteligencia artificial. La Parte 1 se enfoca en la configuración inicial, autenticación, gestión de recursos básicos y servicios clave de Azure AI (Language, Vision y OpenAI). Está alineado con el [syllabus del curso AI-102](https://learn.microsoft.com/es-es/training/courses/ai-102t00#course-syllabus) y utiliza las versiones más recientes de las bibliotecas del Azure SDK para Python (disponibles en [GitHub](https://github.com/Azure/azure-sdk-for-python) y documentadas en [Azure SDK Docs](https://azure.github.io/azure-sdk-for-python)). Cada sección incluye explicaciones didácticas, ejemplos de código actualizados y enlaces directos a la documentación oficial.

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Configuración Inicial](#2-configuración-inicial)
   1. [Instalación de Paquetes](#21-instalación-de-paquetes)
   2. [Autenticación](#22-autenticación)
   3. [Configuración de Variables de Entorno](#23-configuración-de-variables-de-entorno)
      1. [Desarrollo Local](#231-desarrollo-local)
      2. [Producción](#232-producción)
3. [Gestión de Recursos](#3-gestión-de-recursos)
   1. [Grupos de Recursos](#31-grupos-de-recursos)
   2. [Recursos Genéricos](#32-recursos-genéricos)
4. [Azure AI Services](#4-azure-ai-services)
   1. [Azure AI Language](#41-azure-ai-language)
      1. [Configuración del Cliente](#411-configuración-del-cliente)
      2. [Análisis de Sentimientos](#412-análisis-de-sentimientos)
      3. [Extracción de Entidades](#413-extracción-de-entidades)
   2. [Azure AI Vision](#42-azure-ai-vision)
      1. [Configuración del Cliente](#421-configuración-del-cliente)
      2. [Análisis de Imágenes](#422-análisis-de-imágenes)
   3. [Azure OpenAI Service](#43-azure-openai-service)
      1. [Configuración del Cliente](#431-configuración-del-cliente)
      2. [Generación de Texto](#432-generación-de-texto)
      3. [Gestión de Despliegues](#433-gestión-de-despliegues)
5. [Azure AI Search](#5-azure-ai-search)
   1. [Configuración del Cliente](#51-configuración-del-cliente)
   2. [Creación de Índices](#52-creación-de-índices)
   3. [Indexación de Documentos](#53-indexación-de-documentos)
   4. [Consultas de Búsqueda](#54-consultas-de-búsqueda)
6. [Document Intelligence](#6-document-intelligence)
   1. [Configuración del Cliente](#61-configuración-del-cliente)
   2. [Análisis de Documentos (OCR)](#62-análisis-de-documentos-ocr)
7. [Azure Machine Learning](#7-azure-machine-learning)
   1. [Configuración de Workspace](#71-configuración-de-workspace)
   2. [Entrenamiento de Modelos](#72-entrenamiento-de-modelos)
   3. [Despliegue de Modelos](#73-despliegue-de-modelos)
8. [Retrieval-Augmented Generation (RAG)](#8-retrieval-augmented-generation-rag)
   1. [Configuración de Sistema RAG](#81-configuración-de-sistema-rag)
9. [Sistemas Multi-Agente](#9-sistemas-multi-agente)
   1. [Configuración de Agentes](#91-configuración-de-agentes)
10. [Bases de Datos](#10-bases-de-datos)
    1. [Azure Cosmos DB](#101-azure-cosmos-db)
    2. [Azure Database for PostgreSQL](#102-azure-database-for-postgresql)
11. [Redes y Seguridad](#11-redes-y-seguridad)
    1. [Redes Virtuales](#111-redes-virtuales)
    2. [Identidades Administradas](#112-identidades-administradas)
12. [IA Responsable](#12-ia-responsable)
    1. [Moderación de Contenido](#121-moderación-de-contenido)
    2. [Evaluación de Fairness](#122-evaluación-de-fairness)
13. [Solución de Problemas](#13-solución-de-problemas)
    1. [Manejo de Errores](#131-manejo-de-errores)
    2. [Logging y Monitoreo](#132-logging-y-monitoreo)
14. [Recursos Adicionales](#14-recursos-adicionales)

## 1. Introducción

El **Azure SDK para Python** proporciona bibliotecas de cliente para interactuar programáticamente con los servicios de Azure, permitiendo la creación, gestión y consumo de recursos de IA de manera eficiente. Este manual, enfocado en la certificación AI-102, cubre:

1. Configuración y autenticación para desarrollo local y producción.
2. Gestión de recursos (grupos de recursos, recursos genéricos).
3. Uso de Azure AI Services (Language, Vision, OpenAI) para implementar soluciones de visión computacional, procesamiento de lenguaje natural y generación de texto.

Los ejemplos utilizan Python 3.9 o superior, las versiones más recientes de las bibliotecas del Azure SDK (como `azure-ai-textanalytics`, `azure-ai-vision`, `azure-ai-inference`), y siguen las [Directrices de Diseño del Azure SDK](https://azure.github.io/azure-sdk/python/design.html). Para más detalles, consulta la [Documentación del Azure SDK para Python](https://azure.github.io/azure-sdk-for-python) y [Microsoft Learn: Python en Azure](https://learn.microsoft.com/en-us/azure/developer/python/get-started).

## 2. Configuración Inicial

### 2.1. Instalación de Paquetes

Instala las bibliotecas necesarias del Azure SDK para Python usando `pip`. Asegúrate de usar un entorno virtual (`venv`) para aislar dependencias.

```bash
# Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instalar bibliotecas principales
pip install azure-identity==1.18.0 azure-mgmt-resource==23.1.1
pip install azure-ai-textanalytics==5.3.0 azure-ai-vision-imageanalysis==1.0.1
pip install azure-ai-inference==1.0.0b4 azure-core==1.31.0
```

**Explicación**:

1. `azure-identity`: Maneja la autenticación con Azure (por ejemplo, `DefaultAzureCredential`).
2. `azure-mgmt-resource`: Permite gestionar recursos de Azure (grupos, suscripciones).
3. `azure-ai-textanalytics`: Soporta análisis de texto (sentimientos, entidades).
4. `azure-ai-vision-imageanalysis`: Proporciona capacidades de análisis de imágenes.
5. `azure-ai-inference`: Permite interactuar con modelos de Azure OpenAI.
6. `azure-core`: Incluye funcionalidades comunes (reintentos, logging, transporte).

**Documentación**:

- [azure-identity](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)
- [azure-mgmt-resource](https://learn.microsoft.com/en-us/python/api/overview/azure/resources-readme?view=azure-python)
- [azure-ai-textanalytics](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-textanalytics-readme?view=azure-python)
- [azure-ai-vision-imageanalysis](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-vision-imageanalysis-readme?view=azure-python)
- [azure-ai-inference](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme?view=azure-python)

### 2.2. Autenticación

El Azure SDK soporta múltiples métodos de autenticación, siendo `DefaultAzureCredential` el recomendado por su flexibilidad.

```python
from azure.identity import DefaultAzureCredential
import os

# Configurar credenciales
credential = DefaultAzureCredential()

# Configurar cliente de gestión de recursos
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
```

**Explicación**:

1. `DefaultAzureCredential`: Intenta autenticarse en este orden: variables de entorno, identidad administrada, Azure CLI (`az login`), Visual Studio Code, Azure PowerShell.
2. `AZURE_SUBSCRIPTION_ID`: ID de la suscripción de Azure, obtenida desde variables de entorno o configurada manualmente.

**Documentación**: [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python)

### 2.3. Configuración de Variables de Entorno

#### 2.3.1. Desarrollo Local

Crea un archivo `.env` para almacenar credenciales de forma segura.

```env
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
```

Carga las variables en tu aplicación:

```python
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Acceder a variables
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
ai_endpoint = os.getenv("AZURE_AI_ENDPOINT")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
```

**Explicación**:

1. `load_dotenv()`: Carga variables desde el archivo `.env`.
2. Asegúrate de agregar `.env` a `.gitignore` para evitar exponer credenciales.

#### 2.3.2. Producción

Usa **Azure Key Vault** para gestionar secretos en producción.

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Configurar cliente de Key Vault
key_vault_url = "https://your-keyvault.vault.azure.net/"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# Obtener secreto
ai_endpoint = secret_client.get_secret("AI-SERVICE-ENDPOINT").value
```

**Explicación**:

1. `SecretClient`: Accede a secretos almacenados en Azure Key Vault.
2. Usa identidades administradas para autenticación segura en producción.

**Documentación**:

- [azure-keyvault-secrets](https://learn.microsoft.com/en-us/python/api/overview/azure/keyvault-secrets-readme?view=azure-python)
- [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/overview)

## 3. Gestión de Recursos

### 3.1. Grupos de Recursos

Los grupos de recursos son contenedores lógicos para organizar recursos de Azure.

```python
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup

# Crear cliente de gestión de recursos
credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_client = ResourceManagementClient(credential, subscription_id)

# Crear grupo de recursos
def create_resource_group(group_name, location="eastus"):
    rg_params = ResourceGroup(location=location)
    result = resource_client.resource_groups.create_or_update(group_name, rg_params)
    print(f"Grupo de recursos creado: {result.name}")
    return result

# Listar grupos de recursos
def list_resource_groups():
    groups = resource_client.resource_groups.list()
    for group in groups:
        print(f"Nombre: {group.name}, Ubicación: {group.location}")

# Ejemplo de uso
create_resource_group("ai102-resource-group")
list_resource_groups()
```

**Explicación**:

1. `ResourceManagementClient`: Gestiona recursos y grupos de recursos.
2. `create_or_update`: Crea un grupo de recursos o actualiza uno existente.
3. `list`: Enumera todos los grupos de recursos en la suscripción.

**Documentación**: [azure-mgmt-resource](https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcegroups?view=azure-python)

### 3.2. Recursos Genéricos

Gestiona recursos individuales dentro de un grupo.

```python
# Listar recursos en un grupo
def list_resources(group_name):
    resources = resource_client.resources.list_by_resource_group(group_name)
    for resource in resources:
        print(f"Nombre: {resource.name}, Tipo: {resource.type}")

# Crear un recurso genérico
def create_generic_resource(group_name, resource_name, resource_type, location, properties=None):
    parameters = {"location": location, "properties": properties or {}}
    result = resource_client.resources.begin_create_or_update(
        resource_group_name=group_name,
        resource_provider_namespace=resource_type.split("/")[0],
        parent_resource_path="",
        resource_type=resource_type.split("/")[-1],
        resource_name=resource_name,
        parameters=parameters,
        api_version="2023-07-01"
    ).result()
    print(f"Recurso creado: {result.name}")
    return result

# Ejemplo de uso
list_resources("ai102-resource-group")
```

**Explicación**:

1. `list_by_resource_group`: Enumera recursos en un grupo específico.
2. `begin_create_or_update`: Crea o actualiza un recurso genérico, especificando el tipo y proveedor.

**Documentación**: [azure-mgmt-resource.resources](https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resources?view=azure-python)

## 4. Azure AI Services

### 4.1. Azure AI Language

Proporciona capacidades de análisis de texto, como detección de sentimientos y extracción de entidades.

#### 4.1.1. Configuración del Cliente

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

# Configurar cliente
def create_language_client(endpoint):
    credential = DefaultAzureCredential()
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

# Ejemplo de uso
endpoint = os.getenv("AZURE_AI_ENDPOINT")
language_client = create_language_client(endpoint)
```

**Explicación**:

1. `TextAnalyticsClient`: Cliente para interactuar con Azure AI Language.
2. Usa `DefaultAzureCredential` para autenticación segura.

**Documentación**: [TextAnalyticsClient](https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python)

#### 4.1.2. Análisis de Sentimientos

```python
# Analizar sentimiento
def analyze_sentiment(client, text):
    response = client.analyze_sentiment(documents=[text])[0]
    print(f"Sentimiento: {response.sentiment}")
    print(f"Puntuaciones: Positivo={response.confidence_scores.positive:.2f}, "
          f"Neutral={response.confidence_scores.neutral:.2f}, "
          f"Negativo={response.confidence_scores.negative:.2f}")
    return response

# Ejemplo de uso
text = "El producto es excelente y fácil de usar."
result = analyze_sentiment(language_client, text)
```

**Explicación**:

1. `analyze_sentiment`: Analiza el sentimiento de un texto, devolviendo positivo, neutral o negativo.
2. `confidence_scores`: Proporciona puntuaciones de confianza para cada categoría.

**Documentación**: [analyze_sentiment](https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python#azure-ai-textanalytics-textanalyticsclient-analyze-sentiment)

#### 4.1.3. Extracción de Entidades

```python
# Extraer entidades
def recognize_entities(client, text):
    response = client.recognize_entities(documents=[text])[0]
    for entity in response.entities:
        print(f"Entidad: {entity.text}, Categoría: {entity.category}, "
              f"Confianza: {entity.confidence_score:.2f}")
    return response

# Ejemplo de uso
text = "Microsoft fue fundado por Bill Gates en 1975."
result = recognize_entities(language_client, text)
```

**Explicación**:

1. `recognize_entities`: Identifica entidades nombradas (personas, organizaciones, fechas).
2. Devuelve el texto, categoría y confianza de cada entidad.

**Documentación**: [recognize_entities](https://learn.microsoft.com/en-us/python/api/azure-ai-textanalytics/azure.ai.textanalytics.textanalyticsclient?view=azure-python#azure-ai-textanalytics-textanalyticsclient-recognize-entities)

### 4.2. Azure AI Vision

Permite análisis de imágenes y OCR.

#### 4.2.1. Configuración del Cliente

```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.identity import DefaultAzureCredential

# Configurar cliente
def create_vision_client(endpoint):
    credential = DefaultAzureCredential()
    client = ImageAnalysisClient(endpoint=endpoint, credential=credential)
    return client

# Ejemplo de uso
endpoint = os.getenv("AZURE_AI_ENDPOINT")
vision_client = create_vision_client(endpoint)
```

**Explicación**:

1. `ImageAnalysisClient`: Cliente para análisis de imágenes.
2. Usa el mismo endpoint que otros servicios cognitivos si está configurado como multi-servicio.

**Documentación**: [ImageAnalysisClient](https://learn.microsoft.com/en-us/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.imageanalysisclient?view=azure-python)

#### 4.2.2. Análisis de Imágenes

```python
# Analizar imagen
def analyze_image(client, image_url):
    result = client.analyze(
        image_url=image_url,
        visual_features=["Caption", "Tags"]
    )
    print(f"Descripción: {result.caption.text} (Confianza: {result.caption.confidence:.2f})")
    print("Etiquetas:", [tag.name for tag in result.tags])
    return result

# Ejemplo de uso
image_url = "https://example.com/sample-image.jpg"
result = analyze_image(vision_client, image_url)
```

**Explicación**:

1. `analyze`: Analiza una imagen para obtener una descripción y etiquetas.
2. `visual_features`: Especifica las características a extraer (Caption, Tags, Objects, etc.).

**Documentación**: [analyze](https://learn.microsoft.com/en-us/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.imageanalysisclient?view=azure-python#azure-ai-vision-imageanalysis-imageanalysisclient-analyze)

### 4.3. Azure OpenAI Service

Proporciona acceso a modelos de lenguaje avanzados, como GPT-4o.

#### 4.3.1. Configuración del Cliente

```python
from azure.ai.inference import ChatCompletionClient
from azure.identity import DefaultAzureCredential

# Configurar cliente
def create_openai_client(endpoint):
    credential = DefaultAzureCredential()
    client = ChatCompletionClient(endpoint=endpoint, credential=credential)
    return client

# Ejemplo de uso
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_client = create_openai_client(openai_endpoint)
```

**Explicación**:

1. `ChatCompletionClient`: Cliente para interactuar con modelos de Azure OpenAI.
2. Requiere un endpoint específico para OpenAI (no el endpoint genérico de Cognitive Services).

**Documentación**: [ChatCompletionClient](https://learn.microsoft.com/en-us/python/api/azure-ai-inference/azure.ai.inference.chatcompletionclient?view=azure-python)

#### 4.3.2. Generación de Texto

```python
# Generar texto con un modelo
def generate_text(client, prompt, model="gpt-4o"):
    response = client.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"Respuesta: {response.choices[0].message.content}")
    return response

# Ejemplo de uso
prompt = "Escribe un poema sobre la inteligencia artificial."
result = generate_text(openai_client, prompt)
```

**Explicación**:

1. `complete`: Envía un prompt al modelo y devuelve una respuesta generada.
2. `messages`: Formato de chat con roles (`user`, `assistant`, `system`).

**Documentación**: [complete](https://learn.microsoft.com/en-us/python/api/azure-ai-inference/azure.ai.inference.chatcompletionclient?view=azure-python#azure-ai-inference-chatcompletionclient-complete)

#### 4.3.3. Gestión de Despliegues

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

# Crear cliente de gestión
def create_management_client():
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    return CognitiveServicesManagementClient(credential, subscription_id)

# Crear un despliegue de modelo
def create_openai_deployment(resource_group, account_name, deployment_name, model_name, model_version):
    client = create_management_client()
    deployment = client.deployments.begin_create_or_update(
        resource_group_name=resource_group,
        account_name=account_name,
        deployment_name=deployment_name,
        deployment={
            "properties": {
                "model": {
                    "name": model_name,
                    "version": model_version,
                    "format": "OpenAI"
                },
                "sku": {"name": "Standard", "capacity": 1}
            }
        }
    ).result()
    print(f"Despliegue creado: {deployment.name}")
    return deployment

# Ejemplo de uso
create_openai_deployment(
    resource_group="ai102-resource-group",
    account_name="my-openai-resource",
    deployment_name="gpt4o-deployment",
    model_name="gpt-4o",
    model_version="2024-05-13"
)
```

**Explicación**:

1. `CognitiveServicesManagementClient`: Gestiona recursos y despliegues de Azure OpenAI.
2. `begin_create_or_update`: Crea un despliegue para un modelo específico (por ejemplo, GPT-4o).

**Documentación**: [deployments.begin_create_or_update](https://learn.microsoft.com/en-us/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.operations.deploymentsoperations?view=azure-python#azure-mgmt-cognitiveservices-operations-deploymentsoperations-begin-create-or-update)

## 5. Azure AI Search

**Azure AI Search** permite implementar búsqueda semántica y vectorial, esencial para aplicaciones como RAG.

### 5.1. Configuración del Cliente

```python
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential
import os

# Configurar cliente
def create_search_client(endpoint, index_name):
    credential = DefaultAzureCredential()
    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
    return client

# Ejemplo de uso
endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "https://your-search-service.search.windows.net")
index_name = "my-index"
search_client = create_search_client(endpoint, index_name)
```

**Explicación**:

1. `SearchClient`: Cliente para realizar búsquedas en un índice de Azure AI Search.
2. `endpoint`: URL del servicio de búsqueda, obtenido de Azure Portal o variables de entorno.

**Documentación**: [SearchClient](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python)

### 5.2. Creación de Índices

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SearchField, SearchFieldDataType

# Crear índice
def create_search_index(client, index_name):
    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True, retrievable=True),
        SearchField(name="vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), searchable=True)
    ]
    index = SearchIndex(name=index_name, fields=fields)
    result = client.create_or_update_index(index)
    print(f"Índice creado: {result.name}")
    return result

# Ejemplo de uso
index_client = SearchIndexClient(endpoint=endpoint, credential=DefaultAzureCredential())
create_search_index(index_client, "my-index")
```

**Explicación**:

1. `SearchIndexClient`: Gestiona índices de búsqueda.
2. `SearchField`: Define campos del índice (clave, texto, vectores).
3. `create_or_update_index`: Crea o actualiza un índice.

**Documentación**: [SearchIndexClient](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python)

### 5.3. Indexación de Documentos

```python
# Indexar documentos
def index_documents(client, documents):
    result = client.upload_documents(documents=documents)
    print(f"Documentos indexados: {result[0].succeeded}")
    return result

# Ejemplo de uso
documents = [
    {"id": "1", "content": "Azure AI es poderoso", "vector": [0.1, 0.2, 0.3]},
    {"id": "2", "content": "Python impulsa la IA", "vector": [0.4, 0.5, 0.6]}
]
index_documents(search_client, documents)
```

**Explicación**:

1. `upload_documents`: Carga documentos en el índice.
2. Los documentos deben coincidir con el esquema del índice (campos `id`, `content`, `vector`).

**Documentación**: [upload_documents](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python#azure-search-documents-searchclient-upload-documents)

### 5.4. Consultas de Búsqueda

```python
# Realizar búsqueda
def search_documents(client, query):
    results = client.search(search_text=query)
    for result in results:
        print(f"ID: {result['id']}, Contenido: {result['content']}, Score: {result['@search.score']}")
    return results

# Ejemplo de uso
query = "Azure AI"
search_documents(search_client, query)
```

**Explicación**:

1. `search`: Ejecuta una consulta de búsqueda semántica o textual.
2. Devuelve documentos con puntajes de relevancia (`@search.score`).

**Documentación**: [search](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python#azure-search-documents-searchclient-search)

## 6. Document Intelligence

**Azure AI Document Intelligence** (anteriormente Form Recognizer) permite extraer texto, tablas y datos estructurados de documentos.

### 6.1. Configuración del Cliente

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.identity import DefaultAzureCredential

# Configurar cliente
def create_document_intelligence_client(endpoint):
    credential = DefaultAzureCredential()
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)
    return client

# Ejemplo de uso
endpoint = os.getenv("AZURE_AI_ENDPOINT")
di_client = create_document_intelligence_client(endpoint)
```

**Explicación**:

1. `DocumentIntelligenceClient`: Cliente para análisis de documentos.
2. Usa el endpoint de Azure AI Services.

**Documentación**: [DocumentIntelligenceClient](https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/azure.ai.documentintelligence.documentintelligenceclient?view=azure-python)

### 6.2. Análisis de Documentos (OCR)

```python
# Analizar documento
def analyze_document(client, document_url):
    poller = client.begin_analyze_document(model_id="prebuilt-document", document_url=document_url)
    result = poller.result()
    for page in result.pages:
        for line in page.lines:
            print(f"Texto: {line.content}")
    return result

# Ejemplo de uso
document_url = "https://example.com/sample.pdf"
result = analyze_document(di_client, document_url)
```

**Explicación**:

1. `begin_analyze_document`: Inicia el análisis de un documento (PDF, imagen).
2. `model_id="prebuilt-document"`: Usa un modelo preentrenado para OCR general.
3. `poller.result()`: Espera a que el análisis termine y devuelve los resultados.

**Documentación**: [begin_analyze_document](https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/azure.ai.documentintelligence.documentintelligenceclient?view=azure-python#azure-ai-documentintelligence-documentintelligenceclient-begin-analyze-document)

## 7. Azure Machine Learning

**Azure Machine Learning (AML)** permite entrenar, desplegar y gestionar modelos de IA.

### 7.1. Configuración de Workspace

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Configurar cliente
def create_ml_client(subscription_id, resource_group, workspace_name):
    credential = DefaultAzureCredential()
    client = MLClient(credential, subscription_id, resource_group, workspace_name)
    return client

# Ejemplo de uso
ml_client = create_ml_client(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group="ai102-resource-group",
    workspace_name="my-ml-workspace"
)
```

**Explicación**:

1. `MLClient`: Cliente para interactuar con Azure Machine Learning.
2. Requiere ID de suscripción, grupo de recursos y nombre del workspace.

**Documentación**: [MLClient](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python)

### 7.2. Entrenamiento de Modelos

```python
from azure.ai.ml.entities import Job, Command

# Configurar un trabajo de entrenamiento
def create_training_job(client, compute_name, script_path, environment_name):
    job = Command(
        code="./scripts",
        command=f"python {script_path}",
        environment=f"{environment_name}@latest",
        compute=compute_name
    )
    submitted_job = client.jobs.create_or_update(job)
    print(f"Trabajo enviado: {submitted_job.name}")
    return submitted_job

# Ejemplo de uso
training_job = create_training_job(
    client=ml_client,
    compute_name="cpu-cluster",
    script_path="train.py",
    environment_name="my-env"
)
```

**Explicación**:

1. `Command`: Define un trabajo de entrenamiento basado en un script Python.
2. `create_or_update`: Inicia el trabajo en el clúster especificado.

**Documentación**: [Command](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.command?view=azure-python)

### 7.3. Despliegue de Modelos

```python
from azure.ai.ml.entities import OnlineEndpoint, OnlineDeployment

# Crear endpoint en línea
def create_online_endpoint(client, endpoint_name):
    endpoint = OnlineEndpoint(name=endpoint_name, auth_mode="key")
    client.online_endpoints.begin_create_or_update(endpoint).result()
    print(f"Endpoint creado: {endpoint_name}")
    return endpoint

# Desplegar modelo
def create_model_deployment(client, endpoint_name, deployment_name, model_id):
    deployment = OnlineDeployment(
        name=deployment_name,
        endpoint_name=endpoint_name,
        model=model_id,
        instance_type="Standard_DS3_v2",
        instance_count=1
    )
    client.online_deployments.begin_create_or_update(deployment).result()
    print(f"Despliegue creado: {deployment_name}")
    return deployment

# Ejemplo de uso
endpoint_name = "my-endpoint"
create_online_endpoint(ml_client, endpoint_name)
create_model_deployment(ml_client, endpoint_name, "prod-deployment", "my-model:1")
```

**Explicación**:

1. `OnlineEndpoint`: Crea un endpoint para inferencia en tiempo real.
2. `OnlineDeployment`: Despliega un modelo en el endpoint.

**Documentación**:

- [OnlineEndpoint](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.onlineendpoint?view=azure-python)
- [OnlineDeployment](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.onlinedeployment?view=azure-python)

## 8. Retrieval-Augmented Generation (RAG)

**RAG** combina búsqueda semántica con generación de texto para respuestas contextualizadas.

### 8.1. Configuración de Sistema RAG

```python
from azure.ai.inference import ChatCompletionClient
from azure.search.documents import SearchClient

# Configurar sistema RAG
def rag_query(search_client, openai_client, query, model="gpt-4o"):
    # Búsqueda en Azure AI Search
    search_results = search_client.search(search_text=query)
    context = " ".join([result["content"] for result in search_results])

    # Generar respuesta con contexto
    prompt = f"Contexto: {context}\nPregunta: {query}\nRespuesta:"
    response = openai_client.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"Respuesta RAG: {response.choices[0].message.content}")
    return response

# Ejemplo de uso
rag_query(search_client, openai_client, "Beneficios de Azure AI")
```

**Explicación**:

1. `search`: Recupera documentos relevantes del índice.
2. `complete`: Usa el contexto recuperado para generar una respuesta con Azure OpenAI.

**Documentación**:

- [SearchClient.search](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python#azure-search-documents-searchclient-search)
- [ChatCompletionClient.complete](https://learn.microsoft.com/en-us/python/api/azure-ai-inference/azure.ai.inference.chatcompletionclient?view=azure-python#azure-ai-inference-chatcompletionclient-complete)

## 9. Sistemas Multi-Agente

Los sistemas multi-agente coordinan múltiples agentes de IA para tareas complejas.

### 9.1. Configuración de Agentes

```python
# Desplegar agentes especializados
def deploy_multi_agents(ml_client, endpoint_name, agents):
    for agent_name, model_id in agents.items():
        deployment = OnlineDeployment(
            name=agent_name,
            endpoint_name=endpoint_name,
            model=model_id,
            instance_type="Standard_DS3_v2",
            instance_count=1
        )
        ml_client.online_deployments.begin_create_or_update(deployment).result()
        print(f"Agente desplegado: {agent_name}")
    return endpoint_name

# Ejemplo de uso
agents = {
    "analyst": "analyst-model:1",
    "researcher": "researcher-model:1",
    "executor": "executor-model:1"
}
deploy_multi_agents(ml_client, "multi-agent-endpoint", agents)
```

**Explicación**:

1. `OnlineDeployment`: Despliega agentes especializados en un endpoint compartido.
2. Cada agente usa un modelo específico para tareas distintas.

**Documentación**: [OnlineDeployment](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.onlinedeployment?view=azure-python)

## 10. Bases de Datos

### 10.1. Azure Cosmos DB

Ideal para datos NoSQL escalables, compatible con RAG.

```python
from azure.cosmos import CosmosClient, PartitionKey

# Configurar cliente
def create_cosmos_client(endpoint, key):
    client = CosmosClient(endpoint, key)
    return client

# Crear base de datos y contenedor
def create_cosmos_container(client, database_name, container_name):
    database = client.create_database_if_not_exists(database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id")
    )
    print(f"Contenedor creado: {container.id}")
    return container

# Ejemplo de uso
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")
cosmos_client = create_cosmos_client(cosmos_endpoint, cosmos_key)
create_cosmos_container(cosmos_client, "my-database", "my-container")
```

**Explicación**:

1. `CosmosClient`: Cliente para interactuar con Azure Cosmos DB.
2. `create_container_if_not_exists`: Crea un contenedor con una clave de partición.

**Documentación**: [CosmosClient](https://learn.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos.cosmosclient?view=azure-python)

### 10.2. Azure Database for PostgreSQL

Soporta `pgvector` para embeddings de IA.

```python
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSqlManagementClient
import psycopg2

# Crear servidor PostgreSQL
def create_postgres_server(client, resource_group, server_name, admin_user, admin_password):
    server = client.servers.begin_create(
        resource_group_name=resource_group,
        server_name=server_name,
        parameters={
            "location": "eastus",
            "sku": {"name": "Standard_D2s_v3", "tier": "GeneralPurpose"},
            "administrator_login": admin_user,
            "administrator_login_password": admin_password,
            "version": "15"
        }
    ).result()
    print(f"Servidor creado: {server.name}")
    return server

# Habilitar extensión pgvector
def enable_pgvector(host, database, user, password):
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    cursor.close()
    conn.close()
    print("Extensión pgvector habilitada")

# Ejemplo de uso
postgres_client = PostgreSqlManagementClient(DefaultAzureCredential(), os.getenv("AZURE_SUBSCRIPTION_ID"))
create_postgres_server(postgres_client, "ai102-resource-group", "my-postgres", "adminuser", "securepassword")
```

**Explicación**:

1. `PostgreSqlManagementClient`: Gestiona servidores PostgreSQL.
2. `CREATE EXTENSION vector`: Habilita `pgvector` para almacenar embeddings.

**Documentación**: [PostgreSqlManagementClient](https://learn.microsoft.com/en-us/python/api/azure-mgmt-rdbms-postgresql-flexibleservers/azure.mgmt.rdbms.postgresql_flexibleservers.postgresqlmanagementclient?view=azure-python)

## 11. Redes y Seguridad

### 11.1. Redes Virtuales

```python
from azure.mgmt.network import NetworkManagementClient

# Crear red virtual
def create_vnet(client, resource_group, vnet_name):
    vnet = client.virtual_networks.begin_create_or_update(
        resource_group_name=resource_group,
        virtual_network_name=vnet_name,
        parameters={
            "location": "eastus",
            "address_space": {"address_prefixes": ["10.0.0.0/16"]},
            "subnets": [{"name": "default", "address_prefix": "10.0.0.0/24"}]
        }
    ).result()
    print(f"Red virtual creada: {vnet.name}")
    return vnet

# Ejemplo de uso
network_client = NetworkManagementClient(DefaultAzureCredential(), os.getenv("AZURE_SUBSCRIPTION_ID"))
create_vnet(network_client, "ai102-resource-group", "my-vnet")
```

**Explicación**:

1. `NetworkManagementClient`: Gestiona redes virtuales.
2. `begin_create_or_update`: Crea una red virtual con una subred.

**Documentación**: [NetworkManagementClient](https://learn.microsoft.com/en-us/python/api/azure-mgmt-network/azure.mgmt.network.networkmanagementclient?view=azure-python)

### 11.2. Identidades Administradas

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

# Asignar identidad administrada
def assign_managed_identity(client, resource_group, account_name):
    identity = client.accounts.update(
        resource_group_name=resource_group,
        account_name=account_name,
        properties={"identity": {"type": "SystemAssigned"}}
    )
    print(f"Identidad asignada a: {account_name}")
    return identity

# Ejemplo de uso
cog_client = CognitiveServicesManagementClient(DefaultAzureCredential(), os.getenv("AZURE_SUBSCRIPTION_ID"))
assign_managed_identity(cog_client, "ai102-resource-group", "my-openai-resource")
```

**Explicación**:

1. `update`: Asigna una identidad administrada al recurso.
2. `SystemAssigned`: Crea una identidad gestionada por Azure.

**Documentación**: [CognitiveServicesManagementClient](https://learn.microsoft.com/en-us/python/api/azure-mgmt-cognitiveservices/azure.mgmt.cognitiveservices.cognitiveservicesmanagementclient?view=azure-python)

## 12. IA Responsable

### 12.1. Moderación de Contenido

```python
from azure.ai.contentmoderator import ContentModeratorClient

# Configurar cliente
def create_content_moderator_client(endpoint):
    credential = DefaultAzureCredential()
    client = ContentModeratorClient(endpoint=endpoint, credential=credential)
    return client

# Moderar texto
def moderate_text(client, text):
    response = client.text_moderation.screen_text(
        text_content=text,
        text_type="text/plain",
        language="spa"
    )
    print(f"Moderación: {response.terms}")
    return response

# Ejemplo de uso
moderator_client = create_content_moderator_client(os.getenv("AZURE_AI_ENDPOINT"))
moderate_text(moderator_client, "Contenido a moderar")
```

**Explicación**:

1. `ContentModeratorClient`: Cliente para moderar contenido.
2. `screen_text`: Detecta contenido inapropiado en texto.

**Documentación**: [ContentModeratorClient](https://learn.microsoft.com/en-us/python/api/azure-ai-contentmoderator/azure.ai.contentmoderator.contentmoderatorclient?view=azure-python)

### 12.2. Evaluación de Fairness

```python
from fairlearn.metrics import MetricFrame
from sklearn.metrics import accuracy_score

# Evaluar fairness
def evaluate_fairness(model, X_test, y_test, sensitive_features):
    y_pred = model.predict(X_test)
    metrics = {"accuracy": accuracy_score}
    metric_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    print(f"Resultados por grupo: {metric_frame.by_group}")
    return metric_frame

# Ejemplo de uso (requiere datos preparados)
# evaluate_fairness(model, X_test, y_test, sensitive_features)
```

**Explicación**:

1. `MetricFrame`: Evalúa métricas de rendimiento por grupos sensibles.
2. `by_group`: Muestra resultados desglosados por características sensibles.

**Documentación**: [Fairlearn](https://fairlearn.org/)

## 13. Solución de Problemas

### 13.1. Manejo de Errores

```python
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
import time

# Operación con reintentos
def azure_operation_with_retry(operation, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return operation()
        except HttpResponseError as e:
            if e.status_code == 429:
                print(f"Rate limit alcanzado. Reintento {attempt + 1}/{max_retries}")
                time.sleep(delay * (attempt + 1))
            else:
                raise e
        except ResourceNotFoundError as e:
            print(f"Recurso no encontrado: {e}")
            raise e
    raise Exception(f"Falló después de {max_retries} intentos")

# Ejemplo de uso
def example_operation():
    return search_client.search("test")
azure_operation_with_retry(example_operation)
```

**Explicación**:

1. `azure_operation_with_retry`: Implementa reintentos para manejar errores transitorios.
2. Maneja `HttpResponseError` (por ejemplo, rate limits) y `ResourceNotFoundError`.

**Documentación**: [azure-core.exceptions](https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions?view=azure-python)

### 13.2. Logging y Monitoreo

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

# Configurar logging
def setup_logging(connection_string=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    if connection_string:
        configure_azure_monitor(connection_string=connection_string)
    return logging.getLogger(__name__)

# Ejemplo de uso
logger = setup_logging(os.getenv("AZURE_MONITOR_CONNECTION_STRING"))
logger.info("Aplicación iniciada")
```

**Explicación**:

1. `configure_azure_monitor`: Integra con Azure Monitor para telemetría.
2. `logging.getLogger`: Configura un logger personalizado.

**Documentación**: [configure_azure_monitor](https://learn.microsoft.com/en-us/python/api/azure-monitor-opentelemetry/azure.monitor.opentelemetry.configure_azure_monitor?view=azure-python)

## 14. Recursos Adicionales

1. [Documentación del Azure SDK para Python](https://azure.github.io/azure-sdk-for-python)
2. [Azure AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
3. [Azure SDK GitHub](https://github.com/Azure/azure-sdk-for-python)
4. [Microsoft Learn: Python en Azure](https://learn.microsoft.com/en-us/azure/developer/python/get-started)
5. [Fairlearn](https://fairlearn.org/) para evaluación de fairness.
