# Guía de Referencia del SDK de Azure AI para Python

## Tabla de Contenidos

- [1. Introducción](#1-introducción)
- [2. Configuración Inicial](#2-configuración-inicial)
  - [2.1 Instalación de Paquetes](#21-instalación-de-paquetes)
  - [2.2 Autenticación](#22-autenticación)
  - [2.3 Configuración de Variables de Entorno](#23-configuración-de-variables-de-entorno)
    - [Desarrollo Local](#desarrollo-local)
    - [Para Producción](#para-producción)
- [3. Gestión de Recursos](#3-gestión-de-recursos)
  - [3.1 Grupos de Recursos](#31-grupos-de-recursos)
  - [3.2 Workspaces de Azure ML](#32-workspaces-de-azure-ml)
  - [3.3 Endpoints y Despliegues](#33-endpoints-y-despliegues)
- [4. Azure AI Services](#4-azure-ai-services)
  - [4.1 Azure AI Foundry](#41-azure-ai-foundry)
  - [4.2 Azure Machine Learning](#42-azure-machine-learning)
    - [4.2.1 Configuración de Workspace y Compute](#421-configuración-de-workspace-y-compute)
    - [4.2.2 Experimentos y Seguimiento](#422-experimentos-y-seguimiento)
    - [4.2.3 Desplegar y Gestionar Modelos](#423-desplegar-y-gestionar-modelos)
  - [4.3 Natural Language Processing (NLP)](#43-natural-language-processing-nlp)
    - [Azure AI Language](#azure-ai-language)
    - [Azure OpenAI Service](#azure-openai-service)
  - [4.4 Computer Vision](#44-computer-vision)
    - [Azure AI Vision](#azure-ai-vision)
    - [Image Analysis](#image-analysis)
    - [Object Detection](#object-detection)
    - [Image Classification](#image-classification)
    - [Face Detection](#face-detection)
  - [4.5 Document Intelligence](#45-document-intelligence)
    - [4.5.1 Configuración del Cliente](#451-configuración-del-cliente)
    - [4.5.2 Document Analysis (OCR)](#452-document-analysis-ocr)
    - [4.5.3 Form Recognizer](#453-form-recognizer)
    - [4.5.4 Layout Analysis](#454-layout-analysis)
  - [4.6 Azure AI Search](#46-azure-ai-search)
    - [4.6.1 Configuración del Cliente](#461-configuración-del-cliente)
    - [4.6.2 Index Creation](#462-index-creation)
    - [4.6.3 Document Indexing](#463-document-indexing)
    - [4.6.4 Search Queries](#464-search-queries)
    - [4.6.5 Hybrid Search (Text and Vector)](#465-hybrid-search-text-and-vector)
    - [4.6.6 Mejores Prácticas](#466-mejores-prácticas)
    - [4.6.7 Solución de Problemas Comunes](#467-solución-de-problemas-comunes)
- [5. Automatización y Scripts](#5-automatización-y-scripts)
  - [5.1 Script de Provisionamiento Completo](#51-script-de-provisionamiento-completo)
  - [5.2 Sistemas Multi-Agente](#52-sistemas-multi-agente)
- [6. Redes y Seguridad](#6-redes-y-seguridad)
  - [6.1 Configuración de Red Virtual](#61-configuración-de-red-virtual)
  - [6.2 Identidades Administradas](#62-identidades-administradas)
- [7. Bases de Datos](#7-bases-de-datos)
  - [7.1 Azure Cosmos DB](#71-azure-cosmos-db)
  - [7.2 Azure SQL Database](#72-azure-sql-database)
- [8. RAG (Retrieval Augmented Generation)](#8-rag-retrieval-augmented-generation)
  - [8.1 Configuración de Sistema RAG](#81-configuración-de-sistema-rag)
- [9. Escenarios Avanzados](#9-escenarios-avanzados)
  - [9.1 Entrenamiento Distribuido](#91-entrenamiento-distribuido)
  - [9.2 Inferencia de Baja Latencia](#92-inferencia-de-baja-latencia)
  - [9.3 Implementación Híbrida Nube-Borde](#93-implementación-híbrida-nube-borde)
- [10. IA Responsable](#10-ia-responsable)
  - [10.1 Evaluación de Modelos para Fairness](#101-evaluación-de-modelos-para-fairness)
  - [10.2 Interpretabilidad de Modelos](#102-interpretabilidad-de-modelos)
- [11. Solución de Problemas](#11-solución-de-problemas)
  - [11.1 Manejo de Errores Comunes](#111-manejo-de-errores-comunes)
  - [11.2 Logging y Monitoreo](#112-logging-y-monitoreo)
- [12. Recursos Adicionales](#12-recursos-adicionales)
  - [12.1 Patrones de Diseño para aplicaciones de IA](#121-patrones-de-diseño-para-aplicaciones-de-ia)
  - [12.2 Consideraciones de Costos](#122-consideraciones-de-costos)
  - [12.3 Migración desde servicios existentes](#123-migración-desde-servicios-existentes)
  - [12.4 Enlaces de Documentación Oficial](#124-enlaces-de-documentación-oficial)

## 1. Introducción

El SDK de Python para Azure proporciona una forma programática de interactuar con los servicios de Azure, permitiendo la automatización completa de la gestión de recursos, ideal para preparar la certificación AI-102.

## 2. Configuración Inicial

### 2.1 Instalación de Paquetes

```bash
# Instalar el SDK de Azure AI completo
pip install azure-ai

# Paquetes principales para IA
pip install azure-ai-ml azure-ai-formrecognizer azure-ai-textanalytics
pip install azure-ai-vision azure-ai-translation
pip install azure-ai-language-conversations azure-search-documents

# Para desarrollo de IA generativa
pip install azure-ai-generative

# Para bases de datos
pip install pyodbc azure-cosmos
```

### 2.2 Autenticación

Azure AI Services soporta múltiples métodos de autenticación, cada uno con sus propios casos de uso:

- **DefaultAzureCredential**: El método recomendado que intenta múltiples fuentes de credenciales en este orden:
  1. Variables de entorno (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
  2. Identidad administrada asignada por el sistema
  3. Visual Studio Code
  4. Azure CLI
  5. Azure PowerShell

- **Claves de API**: Útiles para pruebas rápidas pero menos seguras para producción.
- **Entidades de servicio**: Ideales para escenarios de automatización.
- **Managed Identities**: La opción más segura para aplicaciones en la nube.

Nunca codifique credenciales directamente en el código fuente. En su lugar:

- Use Azure Key Vault para almacenar secretos
- Utilice variables de entorno para desarrollo local
- Aproveche las identidades administradas en entornos de producción

```python
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.core.credentials import AzureKeyCredential
import os

# Autenticación recomendada (Azure AD) - Soporta múltiples métodos de autenticación
# Intenta autenticarse en este orden:
# 1. Variables de entorno
# 2. Azure CLI (az login)
# 3. Managed Identity
# 4. Visual Studio Code
# 5. Visual Studio
# 6. Azure PowerShell
credential = DefaultAzureCredential()

# Para desarrollo local, puedes usar:
# credential = InteractiveBrowserCredential()  # Abre el navegador para autenticación

# Configurar cliente de recursos
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")  # O tu ID de suscripción directamente
resource_client = ResourceManagementClient(credential, subscription_id)

# Configuración para Azure AI Services
endpoint = os.getenv("AZURE_AI_ENDPOINT")
client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
```

### 2.3 Configuración de Variables de Entorno

#### Desarrollo Local

1. Crea un archivo `.env` en la raíz de tu proyecto:

    ```env
    # Azure Subscription
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    AZURE_TENANT_ID=your-tenant-id
    AZURE_CLIENT_ID=your-client-id
    AZURE_CLIENT_SECRET=your-client-secret
    
    # Azure AI Services
    AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
    ```

2. Agrega `.env` a tu `.gitignore`:

    ```gitignore
    # Archivos de entorno
    .env
    ```

3. Carga las variables en tu aplicación:

    ```python
    from dotenv import load_dotenv
    
    # Cargar variables de entorno desde .env
    load_dotenv()
    ```

#### Para Producción

En entornos de producción, usa identidades administradas o Azure Key Vault:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
    
def get_secret(secret_name):
    key_vault_url = "https://your-keyvault.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    return client.get_secret(secret_name).value
    
# Usar el secreto
ai_endpoint = get_secret("AI-SERVICE-ENDPOINT")
```

## 3. Gestión de Recursos

```python
# Listar todos los recursos en un grupo
def list_resources(resource_client, group_name):
    resources = resource_client.resources.list_by_resource_group(group_name)
    for resource in resources:
        print(f"Nombre: {resource.name}, Tipo: {resource.type}")

# Crear un recurso genérico
def create_generic_resource(resource_client, group_name, resource_name,
                          resource_type, location, parameters):
    resource = resource_client.resources.begin_create_or_update(
        resource_group_name=group_name,
        resource_provider_namespace=resource_type.split('/')[0],
        parent_resource_path="",
        resource_type=resource_type.split('/')[1],
        resource_name=resource_name,
        parameters=parameters
    ).result()
    return resource
```

### 3.1 Grupos de Recursos

```python
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup

# Crear grupo de recursos
def create_resource_group(resource_client, group_name, location):
    rg_params = {'location': location}
    resource_group = resource_client.resource_groups.create_or_update(
        group_name, rg_params
    )
    print(f"Grupo de recursos creado: {resource_group.name}")
    return resource_group

# Listar grupos de recursos
def list_resource_groups(resource_client):
    resource_groups = resource_client.resource_groups.list()
    for rg in resource_groups:
    print(f"Nombre: {rg.name}, Ubicación: {rg.location}")

# Eliminar grupo de recursos
def delete_resource_group(resource_client, group_name):
    delete_async_operation = resource_client.resource_groups.begin_delete(group_name)
    delete_async_operation.wait()
    print(f"Grupo de recursos {group_name} eliminado")
```

### 3.2 Workspaces de Azure ML

El workspace es el recurso de nivel superior que contiene todos los artefactos de Azure Machine Learning. Proporciona:

- Almacenamiento de modelos, conjuntos de datos y experimentos
- Seguridad y control de acceso basado en roles (RBAC)
- Monitoreo y registro de métricas
- Integración con otros servicios de Azure

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace, IdentityConfiguration


# Crear un workspace de Azure ML (versión 2025+)
def create_ml_workspace(ml_client, workspace_name, location, group_name, subscription_id):
    workspace = Workspace(
        name=workspace_name,
        location=location,
        identity=IdentityConfiguration(type="SystemAssigned"),
        friendly_name="Mi Workspace AI",
        description="Workspace para certificación AI-102",
        key_vault=f"/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/Microsoft.KeyVault/vaults/ml-keyvault",
        application_insights=f"/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/microsoft.insights/components/ml-appinsights",
        container_registry=f"/subscriptions/{subscription_id}/resourceGroups/{group_name}/providers/Microsoft.ContainerRegistry/registries/ml-registry"
    )
    # Usar el método recomendado: begin_create
    ws = ml_client.workspaces.begin_create(workspace=workspace).result()
    print(f"Workspace creado: {ws.name}")
    return ws

# Listar workspaces
def list_ml_workspaces(ml_client, group_name):
    workspaces = ml_client.workspaces.list_by_resource_group(group_name)
    for ws in workspaces:
        print(f"Workspace: {ws.name}, Estado: {ws.provisioning_state}")
```

### 3.3 Endpoints y Despliegues

Los experimentos permiten organizar y comparar ejecuciones de entrenamiento. Cada ejecución registra:

- Parámetros de entrada
- Métricas de rendimiento
- Archivos de salida
- Instantánea del código
- Imágenes de contenedor

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import OnlineEndpoint, OnlineDeployment, Model

# Crear un endpoint online
def create_online_endpoint(ml_client, endpoint_name):
    endpoint = OnlineEndpoint(
        name=endpoint_name,
        description="Endpoint para modelo de IA",
        auth_mode="key"
    )

    created_endpoint = ml_client.online_endpoints.begin_create_or_update(
        endpoint
    ).result()
    return created_endpoint

# Desplegar modelo en endpoint
def deploy_model(ml_client, endpoint_name, deployment_name, model_path):
    # Registrar modelo primero
    model = Model(
        path=model_path,
        name="mi-modelo-ia",
        description="Modelo para certificación AI-102"
    )
    registered_model = ml_client.models.create_or_update(model)

    # Crear deployment
    deployment = OnlineDeployment(
        name=deployment_name,
        endpoint_name=endpoint_name,
        model=registered_model.id,
        instance_type="Standard_DS3_v2",
        instance_count=1
    )

    created_deployment = ml_client.online_deployments.begin_create_or_update(
        deployment
    ).result()
    return created_deployment
```

## 4. Azure AI Services

### 4.1 Azure AI Foundry

#### 4.1.1 Consumo de modelos de terceros en Azure AI Foundry

**Flujo actualizado: desde la creación del grupo de recursos hasta el consumo de modelos (SDK 2025+)**

1. **Crea un grupo de recursos en Azure:**

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    import os

    credential = DefaultAzureCredential()
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    resource_client = ResourceManagementClient(credential, subscription_id)
    group_name = "rg-foundry-demo"
    location = "eastus"  # O la región que prefieras
    resource_client.resource_groups.create_or_update(group_name, {"location": location})
    print(f"Grupo de recursos '{group_name}' creado.")
    ```

2. **Crea un proyecto de Azure AI Foundry (tipo 'project') usando MLClient:**

    > **Nota:** Desde 2025, la gestión de proyectos Foundry se realiza con el SDK de Azure Machine Learning (`azure-ai-ml`). No uses clases como `FoundryManagementClient`.

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=group_name
    )

    # Crea el proyecto Foundry (tipo 'project')
    project_name = "foundry-proj-demo"
    project = ml_client.workspaces.begin_create(
        {
            "name": project_name,
            "location": location,
            "kind": "project"
        }
    ).result()
    print(f"Proyecto Foundry '{project_name}' creado.")
    ```

    > Puedes consultar el endpoint del proyecto en el portal de Azure o con:
    >
    > ```python
    > project = ml_client.workspaces.get(project_name)
    > print(project.workspace_id)  # O project.endpoint según versión
    > ```

3. **Obtén el endpoint del proyecto Foundry:**

    El endpoint se encuentra en el portal de Azure, sección "Overview" del proyecto Foundry, o usando el SDK como arriba.

4. **Consume modelos del catálogo Foundry usando el SDK de Foundry:**

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.foundry import FoundryClient

    credential = DefaultAzureCredential()
    foundry_endpoint = "https://<tu-endpoint-foundry>"  # Copia el endpoint del portal
    foundry_client = FoundryClient(credential=credential, endpoint=foundry_endpoint)

    # Listar modelos disponibles
    models = foundry_client.models.list()
    for model in models:
        print(f"Modelo: {model.name}, Proveedor: {model.provider}, Versión: {model.version}")

    # Consumir un modelo específico
    response = foundry_client.completions.create(
        model="gemini-1.5-pro",
        prompt="¿Cuál es el animal más rápido del mundo?"
    )
    print(response.choices[0].text)
    ```

**Resumen actualizado:**

- Usa `MLClient` para crear y gestionar proyectos Foundry.
- El endpoint del proyecto se obtiene desde el portal o con el SDK.
- El consumo de modelos se realiza con el SDK de Foundry y el endpoint del proyecto.
- No uses `FoundryManagementClient` ni `FoundryClient` para gestión de recursos.

**Referencias oficiales:**

- [Create a project for Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects#create-a-hub-based-project)
- [Azure AI Foundry SDK client libraries (Python)](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview)

> **Nota:** El SDK y la API de Foundry evolucionan rápidamente. Consulta siempre la documentación oficial para ejemplos actualizados y lista de modelos soportados.

**Consideraciones importantes:**

- No necesitas crear recursos individuales para cada modelo de terceros; el consumo es directo desde el catálogo.
- Puede que algunos modelos requieran suscripción o permisos adicionales en el portal de Foundry.
- La facturación y límites de uso se gestionan desde Foundry, no desde el proveedor original.
- Consulta la documentación oficial de Foundry para detalles sobre autenticación, cuotas y soporte de modelos: <https://learn.microsoft.com/azure/ai-foundry/>

> **Nota:** El SDK y la API de Foundry evolucionan rápidamente. Consulta siempre la documentación oficial para ejemplos actualizados y lista de modelos soportados.

Azure AI Foundry es una plataforma integral de Microsoft diseñada para acelerar el desarrollo y despliegue de aplicaciones de inteligencia artificial. Este servicio unificado combina capacidades de IA generativa, aprendizaje automático y análisis de datos en un solo entorno, permitiendo a los equipos de desarrollo crear soluciones de IA de manera más rápida y eficiente. Ofrece herramientas para la gestión del ciclo de vida completo de modelos de IA, incluyendo desarrollo, entrenamiento, evaluación y despliegue, con un fuerte énfasis en la seguridad y el cumplimiento normativo. Con integración nativa con otros servicios de Azure, facilita la creación de aplicaciones empresariales escalables que pueden aprovechar modelos de IA preentrenados o personalizados. [Documentación oficial de Azure AI Foundry](https://learn.microsoft.com/es-mx/azure/ai-foundry/overview)

### 4.2 Azure Machine Learning

Azure Machine Learning es un servicio en la nube que permite a los científicos de datos y desarrolladores entrenar, implementar, automatizar, administrar y rastrear modelos de aprendizaje automático. Ofrece un entorno completo para el desarrollo de IA con herramientas de colaboración, capacidades de aprendizaje automático automatizado y capacidades de aprendizaje profundo. [Documentación oficial de Azure Machine Learning](https://learn.microsoft.com/es-mx/azure/machine-learning/overview-what-is-azure-ml)

#### 4.2.1 Configuración de Workspace y Compute

El workspace de Azure Machine Learning es el recurso fundamental para el servicio, proporcionando un lugar centralizado para trabajar con todos los artefactos que cree al usar Azure Machine Learning. El workspace mantiene un historial de todos los entrenamientos, incluyendo registros, métricas, salidas y una instantánea de sus scripts. [Documentación de Workspace](https://learn.microsoft.com/es-mx/azure/machine-learning/concept-workspace)

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute, Workspace
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError

# Mejor práctica 2025: especificar api_version explícitamente para evitar breaking changes
def connect_to_workspace(subscription_id, resource_group, workspace_name, api_version="2024-04-01-preview"):
    ml_client = MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name,
        api_version=api_version  # Especificar versión explícita
    )
    return ml_client

# Crear cluster de computación con manejo robusto de errores
def create_compute_cluster(ml_client, compute_name, vm_size="Standard_DS3_v2"):
    compute = AmlCompute(
        name=compute_name,
        size=vm_size,
        min_instances=0,
        max_instances=3,
        idle_time_before_scale_down=120
    )
    try:
        compute_cluster = ml_client.compute.begin_create_or_update(compute).result()
        return compute_cluster
    except HttpResponseError as e:
        print(f"Error al crear el cluster de cómputo: {e}")
        raise

# Enviar trabajo de entrenamiento con manejo de errores y mejores prácticas
def submit_training_job(ml_client, job_config_path):
    from azure.ai.ml import command, Input
    from azure.ai.ml.constants import AssetTypes
    try:
        job = command(
            code="./src",
            command="python train.py --data ${{inputs.data}}",
            inputs={"data": Input(type=AssetTypes.URI_FOLDER, path="azureml://datasets/mi-dataset/versions/1")},
            environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu",
            compute="cpu-cluster",
            display_name="entrenamiento-modelo-ia"
        )
        returned_job = ml_client.jobs.create_or_update(job)
        return returned_job
    except HttpResponseError as e:
        print(f"Error al enviar el trabajo de entrenamiento: {e}")
        raise

# Nota de mejores prácticas:
# - Siempre especifica api_version en producción.
# - Implementa manejo de errores para operaciones críticas.
# - Usa nombres descriptivos y consistentes para recursos.
```

#### 4.2.2 Experimentos y Seguimiento

Los experimentos en Azure Machine Learning son una forma de organizar y controlar las ejecuciones de entrenamiento de modelos. Cada vez que ejecuta un script de entrenamiento, se crea una ejecución que registra información como parámetros, métricas, archivos de salida y una instantánea del código. [Documentación de Experimentos](https://learn.microsoft.com/es-mx/azure/machine-learning/concept-azure-machine-learning-architecture#experiments)

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Experiment
from azure.core.exceptions import HttpResponseError

# Crear y ejecutar experimento con manejo de errores
def run_experiment(ml_client, experiment_name, script_path):
    from azure.ai.ml import command
    try:
        job = command(
            code=script_path,
            command="python main.py",
            environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu",
            compute="cpu-cluster",
            experiment_name=experiment_name
        )
        returned_job = ml_client.jobs.create_or_update(job)
        ml_client.jobs.stream(returned_job.name)
        metrics = ml_client.jobs.get_metrics(returned_job.name)
        return metrics
    except HttpResponseError as e:
        print(f"Error al ejecutar el experimento: {e}")
        return None

# Listar experimentos
def list_experiments(ml_client):
    experiments = ml_client.jobs.list()
    for exp in experiments:
        print(f"Experimento: {exp.display_name}, Estado: {exp.status}")
```

#### 4.2.3 Desplegar y Gestionar Modelos

Azure Machine Learning proporciona varias formas de implementar modelos como servicios web en la nube de Azure, en Azure Kubernetes Service (AKS), Azure Container Instances (ACI) o en dispositivos perimetrales. [Documentación de Implementación](https://learn.microsoft.com/es-mx/azure/machine-learning/concept-model-management-and-deployment)

```python
from azure.ai.ml.entities import Model, OnlineEndpoint, OnlineDeployment
from azure.ai.ml.constants import AssetTypes
from azure.core.exceptions import HttpResponseError

# Registrar un modelo con manejo de errores
def register_model(ml_client, model_path, model_name):
    try:
        model = Model(
            path=model_path,
            name=model_name,
            type=AssetTypes.CUSTOM_MODEL,
            description="Modelo para certificación AI-102"
        )
        registered_model = ml_client.models.create_or_update(model)
        return registered_model
    except HttpResponseError as e:
        print(f"Error al registrar el modelo: {e}")
        raise

# Crear deployment de modelo con manejo de errores
def create_model_deployment(ml_client, endpoint_name, deployment_name, model_id):
    try:
        deployment = OnlineDeployment(
            name=deployment_name,
            endpoint_name=endpoint_name,
            model=model_id,
            instance_type="Standard_DS3_v2",
            instance_count=1,
            environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu"
        )
        created_deployment = ml_client.online_deployments.begin_create_or_update(
            deployment
        ).result()
        return created_deployment
    except HttpResponseError as e:
        print(f"Error al crear el deployment: {e}")
        raise

# Monitorear uso del modelo con manejo de errores
def monitor_model_usage(ml_client, endpoint_name):
    try:
        endpoint = ml_client.online_endpoints.get(endpoint_name)
        usage = ml_client.online_endpoints.get_usage(endpoint_name)
        print(f"Endpoint: {endpoint.name}")
        print(f"Estado: {endpoint.provisioning_state}")
        print(f"Tráfico total: {usage.total_calls}")
        print(f"Latencia promedio: {usage.average_latency_ms}ms")
    except HttpResponseError as e:
        print(f"Error al monitorear el uso del modelo: {e}")

# Mejores prácticas:
# - Especifica api_version en MLClient para producción.
# - Implementa manejo de errores en todas las operaciones críticas.
# - Usa nombres y descripciones claras para modelos y endpoints.
```

### 4.3 Natural Language Processing (NLP)

#### Azure AI Language

Azure AI Language es un servicio de procesamiento de lenguaje natural que permite analizar y comprender texto no estructurado. Ofrece capacidades avanzadas como análisis de sentimiento, reconocimiento de entidades nombradas, extracción de frases clave y detección de idioma. Con su API REST y SDKs, los desarrolladores pueden integrar fácilmente estas capacidades en sus aplicaciones para extraer información valiosa de documentos, reseñas de clientes, soporte técnico y más. El servicio utiliza modelos de aprendizaje automático preentrenados que pueden personalizarse para dominios específicos, ofreciendo alta precisión con un mínimo esfuerzo de configuración. [Documentación oficial de Azure AI Language](https://learn.microsoft.com/es-mx/azure/cognitive-services/language-service/overview)

| Característica | Azure AI Language | Azure OpenAI |
|---------------|-------------------|--------------|
| Modelos | Pre-entrenados y personalizables | Modelos de lenguaje avanzados (GPT) |
| Casos de uso | Análisis de sentimiento, extracción de entidades | Generación de texto, resúmenes, chat |
| Personalización | Limitada a dominios específicos | Ajuste fino con datos personalizados |
| Latencia | Baja | Media-Alta |
| Costo | Basado en transacciones | Basado en tokens procesados |

- Utilice procesamiento por lotes para múltiples documentos
- Implemente manejo de errores para solicitudes fallidas
- Considere la tasa de límites (rate limits) en el diseño de su aplicación
- Use el modelo más pequeño que cumpla con sus requisitos para optimizar costos

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Configurar cliente de Text Analytics
def create_text_analytics_client(endpoint, key):
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

# Configurar cliente de Language Understanding (antes LUIS)
def create_conversation_analysis_client(endpoint, key):
    credential = AzureKeyCredential(key)
    client = ConversationAnalysisClient(endpoint=endpoint, credential=credential)
    return client

# Analizar intención del usuario
def analyze_intent(conversation_client, project_name, deployment_name, query):
    """
    Analiza la intención del usuario usando el servicio de Language Understanding
    
    Args:
        conversation_client: Cliente de Conversation Analysis
        project_name: Nombre del proyecto de Language Understanding
        deployment_name: Nombre del despliegue (ej: 'production')
        query: Texto del usuario a analizar
        
    Returns:
        dict: Resultados del análisis de intención
    """
    with conversation_client:
        result = conversation_client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "user",
                        "id": "1",
                        "modality": "text",
                        "text": query
                    }
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "stringIndexType": "TextElement_V8"
                }
            }
        )
    
    # Procesar resultados
    intent = result["result"]["prediction"]["topIntent"]
    confidence = result["result"]["prediction"]["intents"][intent]["confidenceScore"]
    entities = result["result"]["prediction"].get("entities", [])
    
    print(f"Intención detectada: {intent} (confianza: {confidence:.2f})")
    
    if entities:
        print("\nEntidades detectadas:")
        for entity in entities:
            print(f"- {entity['text']} ({entity['category']}) -> {entity.get('extraInformation', {}).get('value', 'Sin valor')}")
    
    return {
        "intent": intent,
        "confidence": confidence,
        "entities": entities
    }

# Crear un proyecto de Language Understanding
def create_conversation_project(conversation_client, project_name, project_description, language="es"):
    """
    Crea un nuevo proyecto de Language Understanding
    
    Args:
        conversation_client: Cliente de Conversation Analysis
        project_name: Nombre del proyecto
        project_description: Descripción del proyecto
        language: Idioma del proyecto (por defecto: 'es' para español)
        
    Returns:
        dict: Información del proyecto creado
    """
    project = {
        "projectKind": "Conversation",
        "settings": {
            "confidenceThreshold": 0.7
        },
        "projectName": project_name,
        "description": project_description,
        "language": language
    }
    
    with conversation_client:
        result = conversation_client.begin_create_project(
            project_name=project_name,
            project=project
        ).result()
    
    print(f"Proyecto '{project_name}' creado exitosamente")
    return result

# Entrenar un modelo
async def train_model(conversation_client, project_name):
    """
    Entrena un modelo de Language Understanding
    
    Args:
        conversation_client: Cliente de Conversation Analysis
        project_name: Nombre del proyecto a entrenar
    """
    with conversation_client:
        # Iniciar entrenamiento
        train_result = conversation_client.begin_train(
            project_name=project_name,
            configuration={
                "modelLabel": "v1.0",
                "trainingMode": "standard"
            }
        )
        
        # Esperar a que termine el entrenamiento
        train_result.wait()
        
        # Obtener el estado del entrenamiento
        status = train_result.status()
        
        if status == "succeeded":
            print("Entrenamiento completado exitosamente")
            
            # Desplegar el modelo entrenado
            deployment_result = conversation_client.begin_deploy_project(
                project_name=project_name,
                deployment_name="production",
                deployment_config={
                    "trainedModelLabel": "v1.0"
                }
            )
            deployment_result.wait()
            print("Modelo desplegado exitosamente en el entorno de producción")
        else:
            print(f"Error en el entrenamiento: {status}")
```

#### Azure OpenAI Service

Azure OpenAI Service proporciona acceso a modelos de lenguaje avanzados como GPT-4, permitiendo a las organizaciones crear aplicaciones de IA conversacional de nivel empresarial. Ofrece capacidades de generación de texto, resúmenes, traducción, análisis de código y más, todo ello con la seguridad y cumplimiento de Azure. Los desarrolladores pueden aprovechar estos modelos a través de API fáciles de usar, con opciones para ajuste fino que permiten personalizar el comportamiento del modelo para casos de uso específicos. El servicio incluye características de seguridad integradas y filtros de contenido para garantizar un uso responsable de la IA. [Documentación oficial de Azure OpenAI](https://learn.microsoft.com/es-mx/azure/ai-services/openai/overview)

```python

# OpenAI Python SDK 1.x+ (2025): Instanciación explícita y métodos actualizados
import openai
import os

def create_azure_openai_client(api_key=None, endpoint=None, api_version="2024-02-01"):
    """
    Crea un cliente de Azure OpenAI compatible con la versión 1.x+ del SDK de OpenAI.
    """
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    client = openai.OpenAI(api_key=api_key, base_url=endpoint, default_headers={"api-version": api_version})
    return client

def generate_text(openai_client, prompt, model="gpt-4", max_tokens=100, temperature=0.7):
    """
    Genera texto utilizando un modelo de lenguaje de OpenAI (SDK 1.x+)
    """
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al generar texto: {str(e)}")
        raise

def list_models(openai_client):
    """Lista los modelos de OpenAI disponibles en la suscripción (SDK 1.x+)"""
    try:
        models = openai_client.models.list()
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error al listar modelos: {str(e)}")
        return []

if __name__ == "__main__":
    client = create_azure_openai_client()
    response = generate_text(
        client,
        prompt="Explica la importancia de la seguridad en IA en 3 puntos",
        model="gpt-4"
    )
    print(response)
```

### 4.4 Computer Vision

#### Azure AI Vision

Azure AI Vision es un servicio de visión por computadora que permite extraer información procesable de imágenes y videos. Ofrece capacidades avanzadas de análisis visual, incluyendo reconocimiento de objetos, detección de rostros, análisis de imágenes y generación de descripciones automáticas. El servicio utiliza modelos de aprendizaje profundo preentrenados que pueden personalizarse para dominios específicos, permitiendo a los desarrolladores crear aplicaciones que pueden "ver" e interpretar contenido visual de manera similar a los humanos. [Documentación oficial de Azure AI Vision](https://learn.microsoft.com/es-mx/azure/ai-services/computer-vision/overview)

| Necesidad | Servicio Recomendado | Consideraciones |
|-----------|----------------------|-----------------|
| Análisis general de imágenes | Image Analysis | Proporciona etiquetas, descripciones y contenido explícito |
| Detección de objetos | Object Detection | Identifica objetos específicos con coordenadas |
| Análisis facial | Face Detection | Detecta rostros, emociones y atributos demográficos |
| Clasificación | Custom Vision | Entrenamiento personalizado para dominios específicos |

Optimización de Imágenes:

- Redimensione imágenes grandes antes del procesamiento
- Convierta a formato JPEG para reducir el tamaño
- Considere la compresión con pérdida para aplicaciones que no requieran máxima precisión

```python
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def create_vision_client(endpoint, key):
    """Initialize the Azure AI Vision client"""
    credential = AzureKeyCredential(key)
    return ImageAnalysisClient(endpoint=endpoint, credential=credential)
```

#### Image Analysis

El análisis de imágenes en Azure AI Vision permite extraer una amplia gama de características visuales de imágenes, incluyendo etiquetas descriptivas, objetos detectados, colores dominantes y contenido de texto (OCR). Esta funcionalidad es ideal para crear aplicaciones que necesitan entender el contenido de imágenes sin procesamiento manual. [Documentación de Análisis de Imágenes](https://learn.microsoft.com/es-mx/azure/ai-services/computer-vision/overview-image-analysis)

```python
def analyze_image(vision_client, image_url):
    """Analyze image content and extract features"""
    result = vision_client.analyze(
        image_url=image_url,
        visual_features=[
            VisualFeatures.TAGS,
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS
        ],
        language="es",
        gender_neutral_caption=True
    )
    
    if result.caption:
        print(f"Description: {result.caption.text} (confidence: {result.caption.confidence:.2f})")
    
    if result.tags:
        print("\nTags:")
        for tag in result.tags.list:
            print(f"- {tag.name} (confidence: {tag.confidence:.2f})")
    
    return result
```

#### Object Detection

La detección de objetos identifica y localiza múltiples objetos dentro de una imagen, proporcionando coordenadas de cuadros delimitadores para cada objeto detectado. Esta capacidad es esencial para aplicaciones como inventario automatizado, vehículos autónomos y sistemas de vigilancia. [Documentación de Detección de Objetos](https://learn.microsoft.com/es-mx/azure/ai-services/computer-vision/concept-object-detection)

```python
def detect_objects(vision_client, image_url):
    """Detect objects in an image"""
    result = vision_client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.OBJECTS],
        language="es"
    )
    
    if result.objects:
        print("\nDetected objects:")
        for obj in result.objects.list:
            print(f"- {obj.tags[0].name} (confidence: {obj.tags[0].confidence:.2f})")
            print(f"  Bounding box: {obj.bounding_box}")
    
    return result
```

#### Face Detection

La detección de caras identifica rostros humanos en imágenes, proporcionando información como edad, género, posición de la cabeza y expresiones faciales. Esta funcionalidad es fundamental para aplicaciones de reconocimiento facial, análisis de sentimientos y experiencias de usuario personalizadas. [Documentación de Detección de Caras](https://learn.microsoft.com/es-mx/azure/ai-services/computer-vision/overview-face)

```python
def detect_faces(vision_client, image_url):
    """Detect and analyze faces in an image"""
    result = vision_client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.PEOPLE],
        language="es"
    )
    
    if result.people:
        print(f"\nDetected {len(result.people)} faces:")
        for i, face in enumerate(result.people, 1):
            print(f"Face {i}:")
            print(f"- Bounding box: {face.bounding_box}")
            if hasattr(face, 'confidence'):
                print(f"- Detection confidence: {face.confidence:.2f}")
    
    return result
```

#### Image Classification

La clasificación de imágenes asigna categorías o etiquetas a imágenes completas basándose en su contenido. Azure AI Vision puede clasificar imágenes en miles de categorías predefinidas, lo que es útil para organizar y buscar en grandes colecciones de imágenes. [Documentación de Clasificación de Imágenes](https://learn.microsoft.com/es-mx/azure/ai-services/computer-vision/concept-image-classification)

```python
def classify_image(vision_client, image_url):
    """Classify image content using pre-trained models"""
    result = vision_client.analyze(
        image_url=image_url,
        visual_features=[VisualFeatures.TAGS],
        language="es"
    )
    
    if result.tags:
        print("\nImage classifications:")
        for tag in result.tags.list:
            print(f"- {tag.name} (confidence: {tag.confidence:.2f})")
    
    return result
```

#### Usage Example

```python
# Initialize client
endpoint = "YOUR_VISION_ENDPOINT"
key = "YOUR_VISION_KEY"
vision_client = create_vision_client(endpoint, key)

# Example usage
image_url = "https://example.com/image.jpg"

# Analyze image
print("Analyzing image...")
analyze_image(vision_client, image_url)

# Detect objects
print("\nDetecting objects...")
detect_objects(vision_client, image_url)

# Detect faces
print("\nDetecting faces...")
detect_faces(vision_client, image_url)

# Classify image
print("\nClassifying image...")
classify_image(vision_client, image_url)
```

> **Note**: Image generation capabilities are not part of Azure AI Vision. For image generation, consider using Azure OpenAI Service (DALL-E) or other specialized services.

### 4.5 Document Intelligence

Azure Document Intelligence (anteriormente Form Recognizer) es un servicio de IA que extrae automáticamente texto, pares clave-valor, tablas y estructuras de documentos mediante técnicas avanzadas de aprendizaje automático. Es ideal para automatizar el procesamiento de facturas, recibos, formularios y documentos comerciales. [Documentación oficial de Document Intelligence](https://learn.microsoft.com/es-mx/azure/applied-ai-services/document-intelligence/overview)

| Tipo de Documento | Modelo Recomendado | Características Clave |
|------------------|-------------------|----------------------|
| Facturas/Recibos | prebuilt-invoice | Extrae información estructurada |
| Documentos generales | prebuilt-layout | Mantiene estructura y relaciones espaciales |
| Formularios personalizados | Modelo personalizado | Entrenado con sus propios documentos |
| Documentos de identidad | prebuilt-idDocument | Extrae información de identificaciones |

#### 4.5.1 Configuración del Cliente

Para comenzar a usar Document Intelligence, primero debe crear un recurso en Azure Portal y obtener las credenciales necesarias. El servicio proporciona SDKs para varios lenguajes de programación, incluyendo Python, .NET y Java. [Documentación de inicio rápido](https://learn.microsoft.com/es-mx/azure/applied-ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?view=doc-intel-3.1.0&pivots=programming-language-python)

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os

def create_document_intelligence_client():
    """
    Crea un cliente para Azure Document Intelligence
    
    Returns:
        DocumentIntelligenceClient: Cliente configurado
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    if not endpoint or not key:
        raise ValueError("Las variables de entorno AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT y AZURE_DOCUMENT_INTELLIGENCE_KEY son requeridas")
    
    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
```

#### 4.5.2 Document Analysis (OCR)

El análisis de documentos extrae texto, tablas, estilos y estructura de documentos mediante tecnología OCR (Reconocimiento Óptico de Caracteres) avanzada. Soporta varios formatos de entrada como PDF, TIFF, JPG y PNG. [Documentación de Análisis de Documentos](https://learn.microsoft.com/es-mx/azure/applied-ai-services/document-intelligence/concept-layout?view=doc-intel-3.1.0)

```python
async def extract_text_async(document_client, document_url):
    """
    Extrae texto de un documento o imagen usando el modelo preentrenado de lectura
    
    Args:
        document_client: Cliente de Document Intelligence
        document_url: URL del documento o ruta local
        
    Returns:
        dict: Texto extraído y metadatos
    """
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError
    
    try:
        # Para archivos locales, primero subir a un blob storage o usar bytes
        if not document_url.startswith(('http://', 'https://')):
            with open(document_url, "rb") as f:
                poller = await document_client.begin_analyze_document(
                    "prebuilt-read",
                    f,
                    content_type="application/octet-stream"
                )
        else:
            poller = await document_client.begin_analyze_document_from_url(
                "prebuilt-read",
                document_url
            )
        
        result = await poller.result()
        
        # Procesar resultados
        extracted_data = {
            'content': '',
            'pages': [],
            'languages': set(),
            'tables': []
        }
        
        for page in result.pages:
            page_data = {
                'page_number': page.page_number,
                'angle': page.angle if hasattr(page, 'angle') else None,
                'width': page.width,
                'height': page.height,
                'unit': page.unit,
                'lines': []
            }
            
            for line in page.lines:
                line_data = {
                    'text': line.content,
                    'bounding_box': [{'x': p.x, 'y': p.y} for p in line.polygon] if hasattr(line, 'polygon') else [],
                    'confidence': line.confidence,
                    'words': [
                        {
                            'text': word.content,
                            'confidence': word.confidence,
                            'bounding_box': [{'x': p.x, 'y': p.y} for p in word.polygon] if hasattr(word, 'polygon') else []
                        }
                        for word in getattr(line, 'words', [])
                    ]
                }
                page_data['lines'].append(line_data)
                extracted_data['content'] += line.content + '\n'
            extracted_data['pages'].append(page_data)
        
        # Procesar tablas si existen
        if hasattr(result, 'tables'):
            for table in result.tables:
                table_data = {
                    'row_count': table.row_count,
                    'column_count': table.column_count,
                    'cells': []
                }
                
                for cell in table.cells:
                    cell_data = {
                        'text': cell.content,
                        'row_index': cell.row_index,
                        'column_index': cell.column_index,
                        'is_header': cell.kind == "columnHeader" or cell.kind == "rowHeader",
                        'bounding_box': [{'x': p.x, 'y': p.y} for p in cell.polygon] if hasattr(cell, 'polygon') else []
                    }
                    table_data['cells'].append(cell_data)
                
                extracted_data['tables'].append(table_data)
        
        # Obtener idiomas detectados
        if hasattr(result, 'languages') and result.languages:
            extracted_data['languages'] = list({lang.locale for lang in result.languages})
        
        return extracted_data
        
    except HttpResponseError as e:
        print(f"Error en el servicio Document Intelligence: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Detalles del error: {e.response.text}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar el documento: {e}")
        return None
```

#### 4.5.3 Form Recognizer

El reconocimiento de formularios extrae pares clave-valor y datos de tablas de documentos estructurados como formularios, facturas y recibos. Utiliza modelos preentrenados para documentos comunes o puede entrenarse con ejemplos personalizados. [Documentación de Reconocimiento de Formularios](https://learn.microsoft.com/es-mx/azure/applied-ai-services/document-intelligence/concept-custom?view=doc-intel-3.1.0)

```python
async def analyze_custom_document(document_client, model_id, document_url):
    """
    Analiza un documento usando un modelo personalizado de Document Intelligence
    
    Args:
        document_client: Cliente de Document Intelligence
        model_id: ID del modelo personalizado
        document_url: URL del documento o ruta local
        
    Returns:
        dict: Resultados del análisis
    """
    try:
        if not document_url.startswith(('http://', 'https://')):
            with open(document_url, "rb") as f:
                poller = await document_client.begin_analyze_document(
                    model_id,
                    f,
                    content_type="application/octet-stream"
                )
        else:
            poller = await document_client.begin_analyze_document_from_url(
                model_id,
                document_url
            )
        
        result = await poller.result()
        
        # Procesar resultados
        analysis_result = {
            'doc_type': result.doc_type,
            'fields': {},
            'confidence': result.confidence
        }
        
        if hasattr(result, 'documents') and result.documents:
            for doc in result.documents:
                for name, field in doc.fields.items():
                    analysis_result['fields'][name] = {
                        'value': field.value,
                        'confidence': field.confidence,
                        'bounding_box': [{'x': p.x, 'y': p.y} for p in field.bounding_regions[0].polygon] 
                                      if hasattr(field, 'bounding_regions') and field.bounding_regions else []
                    }
        
        return analysis_result
        
    except Exception as e:
        print(f"Error al analizar el documento: {e}")
        return None
```

#### 4.5.4 Layout Analysis

El análisis de diseño extrae información sobre la estructura visual de un documento, incluyendo texto, tablas, marcas de selección y estilos de texto. Es útil para documentos con diseños complejos o personalizados. [Documentación de Análisis de Diseño](https://learn.microsoft.com/es-mx/azure/applied-ai-services/document-intelligence/concept-layout?view=doc-intel-3.1.0)

```python
async def analyze_layout(document_client, document_url):
    """
    Analiza el diseño y estructura de un documento
    
    Args:
        document_client: Cliente de Document Intelligence
        document_url: URL del documento o ruta local
        
    Returns:
        dict: Estructura del documento analizado
    """
    try:
        if not document_url.startswith(('http://', 'https://')):
            with open(document_url, "rb") as f:
                poller = await document_client.begin_analyze_document(
                    "prebuilt-layout",
                    f,
                    content_type="application/octet-stream"
                )
        else:
            poller = await document_client.begin_analyze_document_from_url(
                "prebuilt-layout",
                document_url
            )
        
        result = await poller.result()
        
        layout_data = {
            'pages': [],
            'tables': [],
            'selection_marks': []
        }
        
        # Procesar páginas
        for page in result.pages:
            page_data = {
                'page_number': page.page_number,
                'width': page.width,
                'height': page.height,
                'unit': page.unit,
                'text_angles': [angle for angle in page.angles] if hasattr(page, 'angles') else [],
                'lines': []
            }
            
            if hasattr(page, 'lines'):
                for line in page.lines:
                    page_data['lines'].append({
                        'text': line.content,
                        'bounding_box': [{'x': p.x, 'y': p.y} for p in line.polygon],
                        'words': [
                            {
                                'text': word.text,
                                'confidence': word.confidence,
                                'bounding_box': [{'x': p.x, 'y': p.y} for p in word.polygon]
                            }
                            for word in line.words
                        ] if hasattr(line, 'words') else []
                    })
            
            layout_data['pages'].append(page_data)
        
        # Procesar tablas
        if hasattr(result, 'tables'):
            for table in result.tables:
                table_data = {
                    'row_count': table.row_count,
                    'column_count': table.column_count,
                    'cells': []
                }
                
                for cell in table.cells:
                    cell_data = {
                        'text': cell.content,
                        'row_index': cell.row_index,
                        'column_index': cell.column_index,
                        'is_header': cell.kind == "columnHeader" or cell.kind == "rowHeader",
                        'bounding_box': [{'x': p.x, 'y': p.y} for p in cell.polygon]
                    }
                    table_data['cells'].append(cell_data)
                
                layout_data['tables'].append(table_data)
        
        # Procesar marcas de selección (checkboxes, radio buttons)
        if hasattr(result, 'selection_marks'):
            for mark in result.selection_marks:
                layout_data['selection_marks'].append({
                    'state': mark.state,
                    'confidence': mark.confidence,
                    'bounding_box': [{'x': p.x, 'y': p.y} for p in mark.polygon]
                })
        
        return layout_data
        
    except Exception as e:
        print(f"Error al analizar el diseño del documento: {e}")
        return None
```

#### 4.5.5 Entrenamiento de Modelos Personalizados

```python
async def train_custom_model(document_client, training_data_url, model_name, use_labels=False):
    """
    Entrena un modelo personalizado de Document Intelligence
    
    Args:
        document_client: Cliente de Document Intelligence
        training_data_url: URL del contenedor de Azure Blob Storage con los datos de entrenamiento
        model_name: Nombre para el modelo
        use_labels: Si se usan etiquetas para el entrenamiento supervisado
        
    Returns:
        str: ID del modelo entrenado
    """
    from azure.ai.documentintelligence.models import (
        BuildDocumentModelRequest,
        AzureBlobContentSource,
        DocumentBuildMode
    )
    
    try:
        build_mode = DocumentBuildMode.TEMPLATE if not use_labels else DocumentBuildMode.NEURAL
        
        request = BuildDocumentModelRequest(
            model_id=model_name,
            build_mode=build_mode,
            azure_blob_source=AzureBlobContentSource(
                container_url=training_data_url
            )
        )
        
        poller = await document_client.begin_build_document_model(request)
        model = await poller.result()
        
        return {
            'model_id': model.model_id,
            'description': model.description,
            'created_date': model.created_date_time,
            'expiration_date': model.expiration_date_time,
            'doc_types': list(model.doc_types.keys()) if hasattr(model, 'doc_types') else []
        }
        
    except Exception as e:
        print(f"Error al entrenar el modelo personalizado: {e}")
        return None
```

#### 4.5.6 Mejores Prácticas

1. **Manejo de Errores**: Siempre implementa manejo de errores para casos como:
   - Tiempos de espera agotados
   - Límites de tasa excedidos
   - Documentos no soportados

2. **Optimización de Rendimiento**:
   - Usa procesamiento por lotes para múltiples documentos
   - Implementa reintentos con retroceso exponencial
   - Considera el uso de Async/Await para operaciones de larga duración

3. **Seguridad**:
   - Nunca codificar claves en el código
   - Usa identidades administradas cuando sea posible
   - Limita los permisos al mínimo necesario

4. **Monitoreo**:
   - Registra métricas de uso y rendimiento
   - Configura alertas para errores y límites de cuota
   - Implementa seguimiento distribuido para diagnósticos

5. **Optimización de Costos**:
   - Usa el modelo más adecuado para cada caso de uso
   - Considera el uso de procesamiento por lotes para reducir costos
   - Monitorea el uso para ajustar la capacidad según sea necesario

#### 4.5.7 Solución de Problemas Comunes

1. **Error de autenticación**:
   - Verifica que las claves y puntos de conexión sean correctos
   - Asegúrate de que el servicio esté desplegado en la región correcta

2. **Documentos no soportados**:
   - Verifica los formatos de archivo soportados
   - Asegúrate de que los documentos no estén dañados
   - Considera convertir documentos a un formato estándar antes del procesamiento

3. **Baja precisión**:
   - Asegúrate de que los documentos estén bien escaneados y sean legibles
   - Considera usar modelos personalizados para casos de uso específicos
   - Revisa la documentación para obtener consejos sobre la preparación de documentos

4. **Límites de tasa**:
   - Implementa reintentos con retroceso exponencial
   - Considera distribuir la carga a lo largo del tiempo
   - Solicita un aumento de cuota si es necesario

5. **Tiempos de espera**:
   - Aumenta los tiempos de espera para documentos grandes
   - Considera usar operaciones asíncronas para documentos grandes
   - Divide documentos grandes en partes más pequeñas si es posible

### 4.6 Azure AI Search

Azure AI Search (anteriormente Azure Cognitive Search) es un servicio de búsqueda en la nube que proporciona capacidades avanzadas de búsqueda sobre contenido estructurado y no estructurado. Este servicio permite crear experiencias de búsqueda enriquecidas con características como búsqueda semántica, búsqueda vectorial, filtrado facetado, autocompletado y sugerencias. Es ideal para aplicaciones que necesitan implementar funcionalidades de búsqueda empresarial, catálogos de productos, búsqueda de documentos y más. [Documentación oficial de Azure AI Search](https://learn.microsoft.com/es-mx/azure/search/search-what-is-azure-search)

#### 4.6.1 Configuración del Cliente

La configuración del cliente de Azure AI Search es sencilla y se integra con la identidad de Azure AD para una autenticación segura. El servicio proporciona SDKs para varios lenguajes de programación, incluyendo .NET, Python, Java y JavaScript. [Documentación de configuración del cliente](https://learn.microsoft.com/es-mx/azure/search/search-howto-dotnet-sdk)

```python
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, 
    SearchField, 
    SearchFieldDataType,
    SimpleField, 
    SearchableField, 
    VectorSearch, 
    HnswParameters,
    HnswAlgorithmConfiguration,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
    SemanticSearch,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField
)
import os

def create_search_index_client(endpoint=None, api_version="2023-11-01", use_azure_ad=True):
    """
    Crea un cliente de índice de búsqueda de Azure AI Search.
    
    Args:
        endpoint: URL del punto de conexión del servicio de búsqueda
        api_version: Versión de la API a utilizar (por defecto: 2023-11-01)
        use_azure_ad: Si es True, usa autenticación con Azure AD (recomendado)
        
    Returns:
        SearchIndexClient: Cliente configurado para administrar índices
    """
    endpoint = endpoint or os.getenv("AZURE_SEARCH_ENDPOINT")
    
    if use_azure_ad:
        # Usar DefaultAzureCredential para autenticación con Azure AD
        credential = DefaultAzureCredential()
        return SearchIndexClient(
            endpoint=endpoint,
            credential=credential,
            api_version=api_version
        )
    else:
        # Usar clave de API (solo para desarrollo/pruebas)
        credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        return SearchIndexClient(
            endpoint=endpoint,
            credential=credential,
            api_version=api_version
        )

def create_search_client(index_name, endpoint=None, api_version="2023-11-01", use_azure_ad=True):
    """
    Crea un cliente de búsqueda para consultar un índice existente.
    
    Args:
        index_name: Nombre del índice a consultar
        endpoint: URL del punto de conexión del servicio de búsqueda
        api_version: Versión de la API a utilizar (por defecto: 2023-11-01)
        use_azure_ad: Si es True, usa autenticación con Azure AD (recomendado)
        
    Returns:
        SearchClient: Cliente configurado para consultar el índice
    """
    endpoint = endpoint or os.getenv("AZURE_SEARCH_ENDPOINT")
    
    if use_azure_ad:
        credential = DefaultAzureCredential()
    else:
        credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        
    return SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=credential,
        api_version=api_version
    )
```

#### 4.6.2 Index Creation

La creación de índices en Azure AI Search permite definir la estructura de los documentos que se indexarán, incluyendo campos, tipos de datos, analizadores y perfiles de puntuación. Los índices pueden incluir campos de texto, numéricos, geográficos y vectores para búsquedas semánticas y vectoriales. [Documentación de creación de índices](https://learn.microsoft.com/es-mx/azure/search/search-what-is-an-index)

```python
def create_search_index(client, index_name, vector_search_dimensions=None):
    """
    Crea un nuevo índice de búsqueda con soporte para búsqueda vectorial y semántica.
    
    Args:
        client: Cliente de índice de búsqueda
        index_name: Nombre del índice a crear
        vector_search_dimensions: Dimensiones para búsqueda vectorial (opcional)
        
    Returns:
        SearchIndex: El índice creado
    """
    # Definir campos básicos
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, 
                  key=True, filterable=True, sortable=True),
                  
        SearchableField(name="title", type=SearchFieldDataType.String,
                      analyzer_name="es.microsoft",
                      searchable=True, filterable=True, sortable=True, facetable=True),
                      
        SearchableField(name="content", type=SearchFieldDataType.String,
                      analyzer_name="es.microsoft",
                      searchable=True),
                      
        SearchableField(name="category", type=SearchFieldDataType.String,
                      searchable=True, filterable=True, facetable=True, sortable=True),
                      
        SimpleField(name="publish_date", type=SearchFieldDataType.DateTimeOffset,
                  filterable=True, sortable=True, facetable=True),
                  
        SimpleField(name="rating", type=SearchFieldDataType.Int32,
                  filterable=True, sortable=True, facetable=True)
    ]
    
    # Configuración de búsqueda vectorial si se especifican dimensiones
    vector_search = None
    if vector_search_dimensions:
        fields.append(
            SearchField(name="embedding", 
                      type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                      searchable=True, 
                      vector_search_dimensions=vector_search_dimensions,
                      vector_search_profile_name="my-vector-config")
        )
        
        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="my-hnsw",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(
                        m=4,
                        ef_construction=400,
                        ef_search=500,
                        metric=VectorSearchAlgorithmMetric.COSINE
                    )
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="my-vector-config",
                    algorithm_configuration_name="my-hnsw"
                )
            ]
        )
    
    # Configuración de búsqueda semántica
    # Usar semanticConfiguration (no searchFields) para semantic ranker (2025+)
    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
            keywords_fields=[SemanticField(field_name="category")]
        )
    )
    semantic_search = SemanticSearch(configurations=[semantic_config])
    
    # Crear el índice
    index = SearchIndex(
        name=index_name, 
        fields=fields, 
        vector_search=vector_search,
        semantic_search=semantic_search,
        scoring_profiles=[]
    )
    
    return client.create_index(index)
```

#### 4.6.3 Document Indexing

La indexación de documentos en Azure AI Search permite cargar y actualizar documentos en lotes, con soporte para operaciones de inserción, fusión, fusión o carga y eliminación. El servicio admite indexación tanto por inserción como por extracción, con conectores para orígenes de datos como Azure Blob Storage, Azure SQL Database y Azure Cosmos DB. [Documentación de indexación de documentos](https://learn.microsoft.com/es-mx/azure/search/search-what-is-data-import)

Estrategias de Indexación:

1. **Índices Particionados**
   - Divida índices grandes por región geográfica o categoría
   - Mejora el rendimiento de consultas frecuentes

2. **Perfiles de Puntuación**
   - Personalice cómo se clasifican los resultados
   - Aplique ponderaciones a campos específicos

3. **Sinónimos**
   - Defina listas de sinónimos para mejorar la recuperación
   - Útil para jerga específica del dominio

```python
def index_documents(search_client, documents, batch_size=1000):
    """
    Indexa documentos en lotes.
    
    Args:
        search_client: Cliente de búsqueda
        documents: Lista de documentos a indexar
        batch_size: Tamaño del lote para indexación
        
    Returns:
        dict: Resultados de la operación de indexación
    """
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError
    
    results = {
        'succeeded': 0,
        'failed': 0,
        'errors': []
    }
    
    # Procesar documentos en lotes
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        try:
            result = search_client.upload_documents(documents=batch)
            
            # Contar documentos exitosos y fallidos
            for doc_result in result:
                if doc_result.succeeded:
                    results['succeeded'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'key': doc_result.key,
                        'error': doc_result.error_message,
                        'status_code': doc_result.status_code
                    })
                    
        except HttpResponseError as e:
            results['failed'] += len(batch)
            results['errors'].append({
                'batch': i // batch_size,
                'error': str(e),
                'status_code': e.status_code if hasattr(e, 'status_code') else None
            })
    
    return results
```

#### 4.6.4 Search Queries

Las consultas en Azure AI Search admiten una amplia gama de capacidades, incluyendo búsqueda de texto completo, filtros, ordenación, paginación y perfiles de puntuación personalizados. Las consultas pueden incluir operadores booleanos, búsqueda aproximada, búsqueda con caracteres comodín y búsqueda de frases exactas. [Documentación de consultas de búsqueda](https://learn.microsoft.com/es-mx/azure/search/search-query-overview)

```python
def search_documents(search_client, search_text, vector=None, top=5, filter_expression=None):
    """
    Realiza una búsqueda en el índice.
    
    Args:
        search_client: Cliente de búsqueda
        search_text: Texto de búsqueda
        vector: Vector de embeddings para búsqueda vectorial (opcional)
        top: Número máximo de resultados a devolver
        filter_expression: Expresión de filtro OData (opcional)
        
    Returns:
        list: Resultados de la búsqueda
    """
    from azure.core.exceptions import HttpResponseError
    
    try:
        search_results = []
        
        # Configurar opciones de búsqueda
        search_kwargs = {
            'search_text': search_text,
            'top': top,
            'include_total_count': True,
            'query_language': 'es-es',
            'query_type': 'semantic',
            'semantic_configuration_name': 'my-semantic-config',
            'query_caption': 'extractive',
            'query_answer': 'extractive',
            'highlight_pre_tag': '<b>',
            'highlight_post_tag': '</b>',
            'filter': filter_expression
        }
        
        # Agregar búsqueda vectorial si se proporciona un vector
        if vector is not None:
            search_kwargs['vector_queries'] = [{
                'vector': vector,
                'fields': 'embedding',
                'k': top * 2  # Recuperar más resultados para filtrar después
            }]
        
        # Ejecutar la búsqueda
        results = search_client.search(**search_kwargs)
        
        # Procesar resultados
        for result in results:
            doc = {}
            
            # Copiar todos los campos del documento
            for key, value in result.items():
                if key != '@search.score' and key != '@search.reranker_score':
                    doc[key] = value
            
            # Agregar metadatos de puntuación
            doc['@search.score'] = result.get('@search.score')
            
            # Agregar resaltado de texto si está disponible
            if '@search.highlights' in result:
                doc['highlights'] = result['@search.highlights']
            
            # Agregar respuestas semánticas si están disponibles
            if hasattr(results, 'answers') and results.answers:
                doc['answers'] = [{
                    'text': answer.text,
                    'highlights': answer.highlights,
                    'score': answer.score
                } for answer in results.answers]
            
            search_results.append(doc)
        
        return {
            'results': search_results,
            'total_count': results.get_count(),
            'coverage': results.coverage if hasattr(results, 'coverage') else None
        }
        
    except HttpResponseError as e:
        print(f"Error en la búsqueda: {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Detalles del error: {e.response.text}")
        return {'results': [], 'error': str(e)}
```

#### 4.6.5 Hybrid Search (Text and Vector)

La búsqueda híbrida combina búsqueda de texto tradicional con búsqueda vectorial, permitiendo encontrar documentos similares basados tanto en significado semántico como en coincidencias de palabras clave. Esta característica es ideal para implementar funcionalidades como búsqueda por similitud semántica, recomendaciones y agrupación de documentos. [Documentación de búsqueda híbrida](https://learn.microsoft.com/es-mx/azure/search/vector-search-overview)

Combina:

- Búsqueda de texto tradicional (BM25)
- Búsqueda vectorial (embedding)
- Filtros y facetas

```python
def hybrid_search(search_client, query, query_embedding, top=5, filter_expression=None):
    """
    Realiza una búsqueda híbrida que combina texto y vectores.
    
    Args:
        search_client: Cliente de búsqueda
        query: Texto de consulta para búsqueda de texto completo
        query_embedding: Vector de embeddings para búsqueda vectorial
        top: Número máximo de resultados a devolver
        filter_expression: Expresión de filtro OData (opcional)
        
    Returns:
        list: Resultados de la búsqueda híbrida
    """
    try:
        # Primero, realizar una búsqueda de texto completo
        text_results = search_documents(
            search_client=search_client,
            search_text=query,
            top=top * 2,  # Recuperar más resultados para combinar
            filter_expression=filter_expression
        )
        
        # Luego, realizar una búsqueda vectorial
        vector_results = search_documents(
            search_client=search_client,
            search_text="",  # Solo búsqueda vectorial
            vector=query_embedding,
            top=top * 2,  # Recuperar más resultados para combinar
            filter_expression=filter_expression
        )
        
        # Combinar y ordenar resultados (Fusion Score = α * text_score + (1-α) * vector_score)
        combined_results = {}
        alpha = 0.5  # Peso para combinar puntuaciones (ajustar según sea necesario)
        
        # Procesar resultados de texto
        for doc in text_results.get('results', []):
            doc_id = doc.get('id')
            if doc_id:
                combined_results[doc_id] = {
                    'document': doc,
                    'text_score': doc.get('@search.score', 0),
                    'vector_score': 0,
                    'combined_score': doc.get('@search.score', 0) * alpha
                }
        
        # Procesar resultados vectoriales
        for doc in vector_results.get('results', []):
            doc_id = doc.get('id')
            vector_score = doc.get('@search.score', 0)
            
            if doc_id in combined_results:
                # Documento encontrado en ambas búsquedas
                combined_results[doc_id]['vector_score'] = vector_score
                combined_results[doc_id]['combined_score'] += vector_score * (1 - alpha)
            else:
                # Solo en resultados vectoriales
                combined_results[doc_id] = {
                    'document': doc,
                    'text_score': 0,
                    'vector_score': vector_score,
                    'combined_score': vector_score * (1 - alpha)
                }
        
        # Ordenar por puntuación combinada y devolver los mejores resultados
        sorted_results = sorted(
            combined_results.values(), 
            key=lambda x: x['combined_score'], 
            reverse=True
        )[:top]
        
        # Formatear resultados finales
        return [{
            **result['document'],
            '@search.score': result['combined_score'],
            '@search.text_score': result['text_score'],
            '@search.vector_score': result['vector_score']
        } for result in sorted_results]
        
    except Exception as e:
        print(f"Error en la búsqueda híbrida: {e}")
        return []
```

#### 4.6.6 Mejores Prácticas

1. **Diseño de Índices**:
   - Defina campos con los tipos de datos apropiados
   - Marque los campos como filtrables, ordenables o facetables según sea necesario
   - Use analizadores de idioma apropiados para campos de texto

2. **Rendimiento**:
   - Indexe en lotes de 1000 documentos o menos
   - Use filtros para reducir el conjunto de documentos antes de aplicar búsqueda de texto completo
   - Considere particionar índices grandes

3. **Seguridad**:
   - Use Azure AD para autenticación en entornos de producción
   - Implemente filtros de seguridad a nivel de fila cuando sea necesario
   - Use claves de API con permisos limitados para aplicaciones cliente

4. **Optimización de Consultas**:
   - Use perfiles de puntuación para personalizar el ranking
   - Aproveche las características semánticas para mejorar la relevancia
   - Considere el uso de sinónimos para mejorar la recuperación

#### 4.6.7 Solución de Problemas Comunes

1. **Errores de autenticación**:
   - Verifique que las credenciales de Azure AD sean correctas
   - Asegúrese de que la entidad de servicio tenga los permisos necesarios
   - Verifique que el punto de conexión del servicio sea correcto

2. **Problemas de rendimiento**:
   - Revise las métricas en Azure Portal para identificar cuellos de botella
   - Considere escalar vertical u horizontalmente según sea necesario
   - Optimice las consultas para reducir la carga del servicio

3. **Resultados de búsqueda inesperados**:
   - Verifique los analizadores de texto utilizados
   - Revise los perfiles de puntuación y las configuraciones semánticas
   - Considere ajustar los parámetros de búsqueda vectorial

4. **Problemas de indexación**:
   - Verifique que los documentos cumplan con el esquema del índice
   - Revise los registros para identificar documentos problemáticos
   - Considere implementar un proceso de reintento para errores transitorios

5. **Optimización de costos**:
   - Monitoree el uso de recursos y ajuste la capacidad según sea necesario
   - Considere usar niveles de servicio apropiados para sus cargas de trabajo
   - Implemente almacenamiento en caché para consultas frecuentes

## 5. Automatización y Scripts

### 5.1 Script de Provisionamiento Completo

Ejemplo de script para automatizar la creación de todos los recursos necesarios para un entorno de IA en Azure. Aprende más sobre automatización en la [documentación de Azure Automation](https://learn.microsoft.com/azure/automation/automation-intro).

```python
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.ai.ml import MLClient
import random

def provision_ai_environment(subscription_id, location="eastus"):
    credential = DefaultAzureCredential()

    # Crear cliente de recursos
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Nombre único para recursos
    random_suffix = random.randint(1000, 9999)
    resource_group_name = f"ai-lab-rg-{random_suffix}"
    workspace_name = f"ai-workspace-{random_suffix}"
    cognitive_service_name = f"ai-cognitive-{random_suffix}"

    try:
        # Crear grupo de recursos
        print(f"Creando grupo de recursos: {resource_group_name}")
        resource_group = resource_client.resource_groups.create_or_update(
            resource_group_name,
            {"location": location}
        )

        # Crear workspace de Azure ML
        print(f"Creando workspace de Azure ML: {workspace_name}")
        ml_client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group_name
        )
        
        workspace = create_ml_workspace(ml_client, resource_group_name, workspace_name, location)

        # Crear recurso de Cognitive Services
        print(f"Creando recurso de Cognitive Services: {cognitive_service_name}")
        cognitive_client = CognitiveServicesManagementClient(credential, subscription_id)
        cognitive_account = cognitive_client.accounts.begin_create(
            resource_group_name,
            cognitive_service_name,
            {
                "kind": "OpenAI",
                "sku": {"name": "S0"},
                "location": location,
                "properties": {"customSubDomainName": cognitive_service_name}
            }
        ).result()

        print("Provisionamiento completado exitosamente!")
        print(f"Grupo de recursos: {resource_group_name}")
        print(f"Workspace ML: {workspace_name}")
        print(f"Servicio Cognitive: {cognitive_service_name}")

        return {
            "resource_group": resource_group_name,
            "ml_workspace": workspace_name,
            "cognitive_service": cognitive_service_name
        }

    except Exception as e:
        print(f"Error en el provisionamiento: {str(e)}")
        # Limpiar recursos en caso de error
        resource_client.resource_groups.begin_delete(resource_group_name)
        raise e

# Ejecutar el script de provisionamiento
if __name__ == "__main__":
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("AZURE_SUBSCRIPTION_ID no está configurado")

    provision_ai_environment(subscription_id)
```

### 5.2 Sistemas Multi-Agente

#### Configuración de Sistema Multi-Agente

Describe cómo orquestar y coordinar múltiples agentes inteligentes usando frameworks como Semantic Kernel. Más información en la [documentación de Semantic Kernel](https://learn.microsoft.com/semantic-kernel/).

```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.planning import SequentialPlanner
import asyncio

# Configurar kernel de Semantic Kernel
def setup_semantic_kernel(openai_endpoint, openai_key, openai_deployment):
    kernel = Kernel()

    # Configurar servicio de chat
    kernel.add_chat_service(
        "gpt-4",
        AzureChatCompletion(
            openai_deployment,
            openai_endpoint,
            openai_key
        )
    )

    return kernel

# Definir agentes especializados
async def setup_multi_agent_system(kernel):
    # Importar habilidades para diferentes agentes
    analyst_skills = kernel.import_semantic_skill_from_directory(
        "skills", "analyst"
    )

    researcher_skills = kernel.import_semantic_skill_from_directory(
        "skills", "researcher"
    )

    executor_skills = kernel.import_semantic_skill_from_directory(
        "skills", "executor"
    )

    return {
        "analyst": analyst_skills,
        "researcher": researcher_skills,
        "executor": executor_skills
    }

# Orquestar tareas entre agentes
async def orchestrate_agents(agents, task_description):
    context = kernel.create_new_context()
    context["input"] = task_description

    # Analista procesa la tarea
    analysis = await agents["analyst"]["analyze"].invoke_async(context=context)
    context["analysis"] = analysis.result

    # Investigador busca información adicional
    research = await agents["researcher"]["research"].invoke_async(context=context)
    context["research"] = research.result

    # Ejecutor realiza la acción
    action = await agents["executor"]["execute"].invoke_async(context=context)

    return action.result

# Ejemplo de uso
async def main():
    kernel = setup_semantic_kernel(
        os.getenv("AZURE_OPENAI_ENDPOINT"),
        os.getenv("AZURE_OPENAI_API_KEY"),
        "gpt-4"
    )

    agents = await setup_multi_agent_system(kernel)

    result = await orchestrate_agents(
        agents,
        "Analizar las tendencias del mercado y proponer una estrategia de inversión"
    )

    print(f"Resultado: {result}")

# Ejecutar el sistema multi-agente
if __name__ == "__main__":
    asyncio.run(main())
```

#### Monitoreo de Agentes

Permite instrumentar, monitorear y trazar la ejecución de agentes y flujos de trabajo de IA en Azure. Consulta la [documentación de Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/overview).

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Configurar monitoreo distribuido
def setup_distributed_monitoring(connection_string):
    configure_azure_monitor(connection_string)
    tracer = trace.get_tracer(__name__)
    return tracer

# Trazar ejecución de agentes
def track_agent_execution(tracer, agent_name, task):
    with tracer.start_as_current_span(agent_name) as span:
        try:
            # Ejecutar la tarea del agente
            result = execute_agent_task(agent_name, task)
            span.set_status(trace.Status(trace.StatusCode.OK))
            span.set_attribute("result.success", True)
            return result
        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(e)
            span.set_attribute("result.success", False)
            raise e

# Consultar trazas
def query_traces(application_insights_client, operation_name):
    query = f"""
    traces
    | where operation_Name == "{operation_name}"
    | order by timestamp desc
    | take 10
    """

    results = application_insights_client.query(query)
    return results
```

## 6. Redes y Seguridad

### 6.1 Configuración de Red Virtual

Permite crear y administrar redes virtuales, subredes y endpoints privados para aislar y proteger recursos en Azure. Más información en la [documentación de redes virtuales](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview).

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetwork, Subnet, PrivateLinkServiceConnection

# Crear cliente de red con autenticación moderna
def create_network_client(subscription_id):
    """
    Crea un cliente de red con autenticación moderna.
    
    Args:
        subscription_id: ID de la suscripción de Azure
        
    Returns:
        NetworkManagementClient: Cliente configurado para administrar recursos de red
    """
    credential = DefaultAzureCredential()
    return NetworkManagementClient(credential, subscription_id)

# Crear red virtual
def create_virtual_network(network_client, resource_group_name, vnet_name, location):
    """
    Crea una red virtual con una subred predeterminada.
    
    Args:
        network_client: Cliente de red
        resource_group_name: Nombre del grupo de recursos
        vnet_name: Nombre de la red virtual
        location: Región de Azure
        
    Returns:
        VirtualNetwork: La red virtual creada
    """
    vnet_params = {
        'location': location,
        'address_space': {
            'address_prefixes': ['10.0.0.0/16']
        },
        'subnets': [{
            'name': 'default',
            'address_prefix': '10.0.0.0/24',
            'private_endpoint_network_policies': 'Disabled'
        }]
    }

    try:
        vnet_poller = network_client.virtual_networks.begin_create_or_update(
            resource_group_name=resource_group_name,
            virtual_network_name=vnet_name,
            parameters=vnet_params
        )
        return vnet_poller.result()
    except Exception as e:
        print(f"Error al crear la red virtual: {str(e)}")
        raise

# Configurar punto de conexión privado
def create_private_endpoint(network_client, resource_group_name, endpoint_name,
                          vnet_name, subnet_name, resource_id, location):
    """
    Crea un punto de conexión privado para un recurso de Azure.
    
    Args:
        network_client: Cliente de red
        resource_group_name: Nombre del grupo de recursos
        endpoint_name: Nombre del punto de conexión privado
        vnet_name: Nombre de la red virtual
        subnet_name: Nombre de la subred
        resource_id: ID del recurso de Azure al que se conectará el punto de conexión privado
        location: Región de Azure
        
    Returns:
        PrivateEndpoint: El punto de conexión privado creado
    """
    from azure.mgmt.network.models import PrivateEndpoint, PrivateLinkServiceConnection
    
    # Obtener el ID de la subred
    subnet = network_client.subnets.get(
        resource_group_name=resource_group_name,
        virtual_network_name=vnet_name,
        subnet_name=subnet_name
    )
    
    private_endpoint_params = {
        'location': location,
        'private_link_service_connections': [{
            'name': endpoint_name,
            'private_link_service_id': resource_id,
            'group_ids': ['sites']  # Depende del tipo de recurso
        }],
        'subnet': {
            'id': f'/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/virtualNetworks/{vnet_name}/subnets/{subnet_name}'
        }
    }

    try:
        endpoint_poller = network_client.private_endpoints.begin_create_or_update(
            resource_group_name=resource_group_name,
            private_endpoint_name=endpoint_name,
            parameters=private_endpoint_params
        )
        return endpoint_poller.result()
    except Exception as e:
        print(f"Error al crear el punto de conexión privado: {str(e)}")
        raise
```

### 6.2 Identidades Administradas

Las identidades administradas de Azure permiten a los recursos autenticarse automáticamente en otros servicios de Azure sin almacenar credenciales en el código. Consulta la [documentación de identidades administradas](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview).

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.msi import ManagedServiceIdentityClient
from azure.mgmt.msi.models import Identity
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.v2022_04_01.models import RoleAssignmentCreateParameters

# Crear cliente de identidad administrada
def create_msi_client(subscription_id):
    """
    Crea un cliente de identidad administrada con autenticación moderna.
    
    Args:
        subscription_id: ID de la suscripción de Azure
        
    Returns:
        ManagedServiceIdentityClient: Cliente configurado para administrar identidades
    """
    credential = DefaultAzureCredential()
    return ManagedServiceIdentityClient(credential, subscription_id)

# Crear identidad administrada
def create_managed_identity(msi_client, resource_group_name, identity_name, location):
    """
    Crea una identidad administrada asignada por el usuario.
    
    Args:
        msi_client: Cliente de identidad administrada
        resource_group_name: Nombre del grupo de recursos
        identity_name: Nombre de la identidad
        location: Región de Azure
        
    Returns:
        Identity: La identidad administrada creada
    """
    identity_params = {
        'location': location,
        'tags': {
            'purpose': 'ai-service-identity',
            'environment': 'production'
        }
    }

    try:
        identity = msi_client.user_assigned_identities.begin_create_or_update(
            resource_group_name=resource_group_name,
            resource_name=identity_name,
            parameters=identity_params
        ).result()
        print(f"Identidad administrada creada: {identity.principal_id}")
        return identity
    except Exception as e:
        print(f"Error al crear la identidad administrada: {str(e)}")
        raise

# Asignar roles a identidad
def assign_role_to_identity(subscription_id, scope, identity_principal_id, role_definition_id):
    """
    Asigna un rol de Azure a una identidad administrada.
    
    Args:
        subscription_id: ID de la suscripción de Azure
        scope: Ámbito de la asignación de rol (ej. suscripción, grupo de recursos o recurso)
        identity_principal_id: ID de la entidad de seguridad de la identidad
        role_definition_id: ID de la definición de rol (ej. 'Contributor')
        
    Returns:
        RoleAssignment: La asignación de rol creada
    """
    credential = DefaultAzureCredential()
    auth_client = AuthorizationManagementClient(credential, subscription_id)
    
    # Generar un nombre único para la asignación de rol
    import uuid
    role_assignment_name = str(uuid.uuid4())
    
    # Crear parámetros de asignación de rol
    role_assignment_params = {
        'role_definition_id': f"/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/{role_definition_id}",
        'principal_id': identity_principal_id,
        'principal_type': 'ServicePrincipal'
    }

    try:
        assignment = auth_client.role_assignments.create(
            scope, role_assignment_name, role_assignment_params
        )
        print(f"Rol asignado correctamente: {assignment.role_definition_id}")
        return assignment
    except Exception as e:
        print(f"Error al asignar el rol: {str(e)}")
        raise
```

### Actualizaciones de Seguridad

1. **Autenticación Moderna**:
   - Uso de `DefaultAzureCredential` para autenticación segura
   - Eliminación de credenciales codificadas

2. **Manejo de Errores**:
   - Manejo de excepciones mejorado
   - Mensajes de error descriptivos

3. **Documentación**:
   - Docstrings detallados para todas las funciones
   - Tipos de parámetros y valores de retorno documentados

4. **Buenas Prácticas**:
   - Uso de etiquetas para mejor organización
   - Configuración segura por defecto
   - Limpieza de recursos después de operaciones fallidas

### Configuración Requerida

Asegúrate de tener configuradas las siguientes variables de entorno:

```bash
# Para autenticación con Azure AD
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

### Notas de Migración

1. **De versiones anteriores**:
   - Las versiones anteriores usaban credenciales directas
   - La autenticación con claves de API ya no se recomienda

2. **Nuevas características**:
   - Soporte mejorado para RBAC
   - Integración con Azure AD para una mejor seguridad
   - Operaciones asíncronas para mejor rendimiento

3. **Requisitos del sistema**:
   - Python 3.7 o superior
   - Paquete `azure-identity` versión 1.10.0 o superior
   - Paquete `azure-mgmt-resource` versión 20.0.0 o superior

### Solución de Problemas Comunes

1. **Errores de autenticación**:
   - Verifica que las credenciales de Azure AD sean correctas
   - Asegúrate de que la entidad de servicio tenga los permisos necesarios

2. **Problemas de permisos**:
   - Verifica que la identidad tenga asignados los roles necesarios
   - Asegúrate de que el ámbito de la asignación de rol sea correcto

3. **Errores de red**:
   - Verifica la configuración de la red virtual
   - Asegúrate de que las reglas de NSG permitan el tráfico necesario

## 7. Bases de Datos

### 7.1 Azure Cosmos DB

Azure Cosmos DB es una base de datos NoSQL globalmente distribuida y escalable, ideal para almacenar y consultar grandes volúmenes de datos con baja latencia. Consulta la [documentación de Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/introduction).

```python
from azure.cosmos import CosmosClient, PartitionKey

# Conectar a Cosmos DB
def connect_to_cosmosdb(endpoint, key, database_name, container_name):
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

# Crear base de datos y contenedor
def create_cosmos_db_container(cosmos_client, database_name, container_name, partition_key):
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String,
                       analyzer_name="es.microsoft"),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String,
                   filterable=True, facetable=True)
    ]

    index = SearchIndex(name=container_name, fields=fields)
    search_index_client.create_index(index)

# Insertar documentos
def insert_documents(container, documents):
    for doc in documents:
        container.create_item(body=doc)
    print(f"Insertados {len(documents)} documentos")

# Consultar documentos
def query_documents(container, query):
    items = container.query_items(
        query=query,
        enable_cross_partition_query=True
    )
    return list(items)
```

### 7.2 Azure SQL Database

Azure SQL Database es un servicio de base de datos relacional totalmente administrado, compatible con SQL Server y optimizado para la nube. Más información en la [documentación de Azure SQL](https://learn.microsoft.com/azure/azure-sql/database/single-database-overview).

```python
import pyodbc
import pandas as pd

# Conectar a Azure SQL Database
def connect_to_sql_database(server, database, username, password):
    connection_string = f"""
        Driver={{ODBC Driver 17 for SQL Server}};
        Server={server}.database.windows.net;
        Database={database};
        Uid={username};
        Pwd={password};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
    """
    conn = pyodbc.connect(connection_string)
    return conn

# Ejecutar consultas
def execute_sql_query(connection, query, params=None):
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if query.strip().upper().startswith('SELECT'):
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    else:
        connection.commit()
        return cursor.rowcount

# Cargar datos desde DataFrame
def load_dataframe_to_sql(connection, dataframe, table_name):
    for index, row in dataframe.iterrows():
        columns = ', '.join(row.index)
        placeholders = ', '.join(['?'] * len(row))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        connection.cursor().execute(query, tuple(row))
    connection.commit()
```

#### 7.3 Patrones de Diseño

- **Patrón CQRS**: Separe las operaciones de lectura y escritura
- **Caché**: Implemente caché para consultas frecuentes
- **Paginación**: Use límites y tokens de continuación para grandes conjuntos de resultados

#### 7.4 Monitoreo

- Habilite registros de diagnóstico
- Establezca alertas para métricas clave
- Monitoree el uso de cuotas y límites

## 8. RAG (Retrieval Augmented Generation)

### 8.1 Configuración de Sistema RAG

Describe cómo configurar un sistema RAG (Retrieval Augmented Generation) en Azure, integrando búsqueda semántica y modelos generativos. Consulta la [guía de configuración RAG](https://learn.microsoft.com/azure/ai-services/openai/how-to/semantic-search-quickstart).

```python
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType,
    SimpleField, SearchableField
)
from azure.core.credentials import AzureKeyCredential

# Configurar índice RAG
def create_rag_index(search_index_client, index_name):
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String,
                       analyzer_name="es.microsoft"),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String,
                   filterable=True, facetable=True),
        SimpleField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                   searchable=True, vector_search_dimensions=1536,
                   vector_search_profile_name="my-vector-config")
    ]

    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="my-hnsw",
                kind="hnsw",
                parameters=HnswParameters(metric="cosine")
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="my-vector-config",
                algorithm_configuration_name="my-hnsw"
            )
        ]
    )

    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    search_index_client.create_index(index)

# Implementar búsqueda semántica
def semantic_search(search_client, query, vector=None):
    if vector:
        # Búsqueda vectorial
        results = search_client.search(
            search_text=query,
            vectors=[Vector(value=vector, k=3, fields="embedding")],
            select=["id", "title", "content", "category"]
        )
    else:
        # Búsqueda textual
        results = search_client.search(
            search_text=query,
            select=["id", "title", "content", "category"]
        )

    return [result for result in results]

# Sistema RAG completo
def rag_system(openai_client, search_client, query):
    # Generar embedding de la consulta
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    # Buscar documentos relevantes
    search_results = semantic_search(search_client, query, query_vector)

    # Construir contexto
    context = "\n\n".join([f"Documento {i+1}: {result['content']}"
                          for i, result in enumerate(search_results[:3])])

    # Generar respuesta
    prompt = f"""
    Basado en los siguientes documentos:
    {context}

    Responde a la pregunta: {query}
    """

    answer = generate_text(openai_client, prompt)
    return answer, search_results
```

### 8.3 Encriptación

- En tránsito: TLS 1.2+
- En reposo: Claves administradas por Microsoft o por el cliente

### 8.4 Cumplimiento

- Certificaciones: ISO 27001, SOC 1/2, HIPAA, GDPR
- Regiones: Elija regiones que cumplan con los requisitos de residencia de datos

## 9. Escenarios Avanzados

### 9.1 Entrenamiento Distribuido

Permite entrenar modelos de machine learning en múltiples nodos o GPUs para acelerar el proceso y manejar grandes volúmenes de datos. Más información en la [documentación de entrenamiento distribuido](https://learn.microsoft.com/azure/machine-learning/how-to-train-distributed).

```python
from azure.ai.ml import command
from azure.ai.ml.entities import DistributionConfiguration

# Configurar entrenamiento distribuido
def setup_distributed_training(ml_client, script_path, compute_target):
    distribution = DistributionConfiguration(
        type="PyTorch",
        process_count_per_instance=4
    )

    job = command(
        code=script_path,
        command="python train.py --distributed",
        environment="AzureML-PyTorch-1.9-ubuntu20.04-py38-cuda11-gpu",
        compute=compute_target,
        distribution=distribution,
        resources={
            "instance_count": 4,
            "properties": {
                "gpu_count": 4
            }
        }
    )

    return ml_client.jobs.create_or_update(job)

# Monitorear entrenamiento distribuido
def monitor_distributed_training(ml_client, job_id):
    job = ml_client.jobs.get(job_id)

    print(f"Estado del trabajo: {job.status}")
    print(f"Nodos de entrenamiento: {job.resources.instance_count}")

    # Obtener métricas por nodo
    metrics = ml_client.jobs.get_metrics(job_id)
    for node_metrics in metrics:
        print(f"Nodo {node_metrics['node_id']}:")
        print(f"  Pérdida: {node_metrics.get('loss', 'N/A')}")
        print(f"  Precisión: {node_metrics.get('accuracy', 'N/A')}")
```

### 9.2 Inferencia de Baja Latencia

Describe cómo optimizar el despliegue de modelos para obtener respuestas rápidas y eficientes en escenarios de producción. Consulta la [guía de inferencia optimizada](https://learn.microsoft.com/azure/machine-learning/how-to-deploy-inference).

```python
from azure.ai.ml.entities import OnlineEndpoint, OnlineDeployment, CodeConfiguration

# Configurar inferencia optimizada
def setup_optimized_inference(ml_client, model_id, endpoint_name):
    # Configurar endpoint para baja latencia
    endpoint = OnlineEndpoint(
        name=endpoint_name,
        description="Endpoint optimizado para baja latencia",
        auth_mode="key"
    )

    ml_client.online_endpoints.begin_create_or_update(endpoint)

    # Configurar deployment con optimizaciones
    deployment = OnlineDeployment(
        name="optimized-deployment",
        endpoint_name=endpoint_name,
        model=model_id,
        instance_type="Standard_NC6s_v3",  # Instancia con GPU
        instance_count=2,
        environment="AzureML-PyTorch-1.9-ubuntu20.04-py38-cuda11-gpu",
        code_configuration=CodeConfiguration(
            code="./inference-code",
            scoring_script="score.py"
        ),
        environment_variables={
            "OPTIMIZATION_LEVEL": "3",
            "INFERENCE_ACCELERATOR": "TensorRT"
        }
    )

    return ml_client.online_deployments.begin_create_or_update(deployment)
```

### 9.3 Implementación Híbrida Nube-Borde

Permite empaquetar e implementar modelos de IA tanto en la nube como en dispositivos edge, integrando IoT y Azure ML. Más información en la [documentación de Azure IoT Edge](https://learn.microsoft.com/azure/iot-edge/).

```python
from azure.mgmt.iotcentral import IotCentralClient
from azure.mgmt.iotcentral.models import App, AppSkuInfo

# Empaquetar modelo para edge
def package_model_for_edge(ml_client, model_id, output_path):
    from azure.ai.ml.entities import Package, TargetEnvironment

    # Crear paquete para contenedor de Docker
    package = Package(
        target_environment=TargetEnvironment(
            name="edge-environment",
            version="1.0",
            docker=TargetEnvironment.DockerConfiguration(
                base_image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04"
            )
        ),
        model=model_id,
        entry_script="score.py"
    )

    # Descargar paquete
    ml_client.packages.download(package, output_path)
    return output_path

# Implementar en IoT Edge
def deploy_to_iot_edge(iot_central_client, app_name, resource_group, package_path):
    # Crear aplicación de IoT Central
    app = App(
        location="global",
        sku=AppSkuInfo(name="ST2"),
        display_name=app_name,
        subdomain=app_name.lower()
    )

    app = iot_central_client.apps.create_or_update(resource_group, app_name, app)

    # Implementar modelo (simplificado - en producción usarías Azure IoT Hub SDK)
    print(f"Aplicación {app_name} creada. Implementa manualmente el paquete en dispositivos Edge.")
    return app
```

### 9.4 Azure Data Factory

- Orquestación de flujos de trabajo ETL
- Programación de pipelines de procesamiento

### 9.5 Azure Functions

- Procesamiento sin servidor
- Desencadenado por eventos (nuevos documentos, imágenes, etc.)

### Análisis de Texto Avanzado

Incluye técnicas avanzadas de análisis de texto como resumen automático, extracción de frases clave y análisis de opiniones usando Azure AI Language. Consulta la [guía de análisis de texto](https://learn.microsoft.com/azure/ai-services/language-service/overview).

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Análisis de documentos extensos
def analyze_large_documents(text_analytics_client, documents, chunk_size=10):
    results = []

    # Procesar en chunks para evitar límites de tamaño
    for i in range(0, len(documents), chunk_size):
        chunk = documents[i:i + chunk_size]

        # Análisis de sentimiento
        sentiment_response = text_analytics_client.analyze_sentiment(
            chunk, show_opinion_mining=True
        )

        # Extracción de frases clave
        key_phrases_response = text_analytics_client.extract_key_phrases(chunk)

        # Reconocimiento de entidades
        entities_response = text_analytics_client.recognize_entities(chunk)

        results.append({
            'sentiment': sentiment_response,
            'key_phrases': key_phrases_response,
            'entities': entities_response
        })

    return results

# Resumen automático de documentos
def summarize_document(text_analytics_client, document):
    poller = text_analytics_client.begin_extract_summary([document])
    summary_result = poller.result()

    if summary_result and not summary_result[0].is_error:
        summary = "\n".join([
            sentence.text for sentence in summary_result[0].sentences
        ])
        return summary
    return None

# Análisis de opiniones específicas
def analyze_targeted_opinions(text_analytics_client, documents, target_terms):
    all_opinions = []

    for doc in documents:
        # Buscar menciones de los términos objetivo
        entities_response = text_analytics_client.recognize_entities([doc])

        if not entities_response[0].is_error:
            for entity in entities_response[0].entities:
                if entity.text.lower() in [term.lower() for term in target_terms]:
                    # Analizar sentimiento alrededor de la entidad
                    sentiment_response = text_analytics_client.analyze_sentiment(
                        [doc], show_opinion_mining=True
                    )

                    if not sentiment_response[0].is_error:
                        for sentence in sentiment_response[0].sentences:
                            if any(entity.text.lower() in sentence.text.lower()
                                  for entity in entities_response[0].entities):
                                all_opinions.append({
                                    'target': entity.text,
                                    'sentence': sentence.text,
                                    'sentiment': sentence.sentiment,
                                    'scores': sentence.confidence_scores
                                })

    return all_opinions
```

## 10. IA Responsable

### 10.1 Evaluación de Modelos para Fairness

```python
from azureml.fairness import FairlearnDashboard
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Evaluar fairness del modelo
def evaluate_model_fairness(model, X_test, y_test, sensitive_features):
    # Realizar predicciones
    y_pred = model.predict(X_test)

    # Métricas de performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')

    # Analizar fairness con Fairlearn
    from fairlearn.metrics import MetricFrame, selection_rate
    from fairlearn.metrics import count, false_positive_rate, false_negative_rate

    metrics = {
        'accuracy': accuracy_score,
        'precision': precision_score,
        'recall': recall_score,
        'selection_rate': selection_rate,
        'false_positive_rate': false_positive_rate,
        'false_negative_rate': false_negative_rate
    }

    metric_frame = MetricFrame(
        metrics=metrics,
        y_true=y_test,
        y_pred={"model": y_pred},
        sensitive_features=sensitive_features
    )

    # Generar dashboard
    FairlearnDashboard(
        sensitive_features=sensitive_features,
        y_true=y_test.tolist(),
        y_pred={"model": y_pred.tolist()}
    )

    return metric_frame

# Mitigar sesgos en el modelo
def mitigate_model_bias(model, X_train, y_train, sensitive_features):
    from fairlearn.reductions import ExponentiatedGradient, GridSearch
    from fairlearn.reductions import DemographicParity, ErrorRate

    # Definir constraint de fairness
    constraint = DemographicParity()

    # Mitigar usando Exponentiated Gradient
    mitigator = ExponentiatedGradient(
        estimator=model,
        constraints=constraint,
        eps=0.01  # Tolerancia para la constraint
    )

    mitigator.fit(X_train, y_train, sensitive_features=sensitive_features)

    return mitigator
```

### 10.2 Interpretabilidad de Modelos

```python
from interpret_community import TabularExplainer
from interpret_community.widget import ExplanationDashboard

# Explicar predicciones del modelo
def explain_model_predictions(model, X_train, X_test, feature_names):
    # Crear explainer
    explainer = TabularExplainer(
        model,
        X_train,
        features=feature_names,
        classes=["Class 0", "Class 1"]  # Ajustar según el problema
    )

    # Generar explicaciones globales
    global_explanation = explainer.explain_global(X_train)

    # Generar explicaciones locales
    local_explanation = explainer.explain_local(X_test[:5])

    # Mostrar dashboard
    ExplanationDashboard(global_explanation, model, datasetX=X_train)

    return {
        'global': global_explanation,
        'local': local_explanation
    }

# Monitorear drift de datos
def monitor_data_drift(X_train, X_current, feature_names):
    from azureml.datadrift import DataDriftDetector

    # Configurar detector de drift
    detector = DataDriftDetector.create_from_datasets(
        'data-drift-detector',
        X_train,  # Línea base
        X_current,  # Datos actuales
        feature_names=feature_names
    )

    # Ejecutar detección
    drift_metrics = detector.run()

    # Analizar resultados
    if drift_metrics['data_drift']['drift_detected']:
        print(f"Drift detectado en características: {drift_metrics['data_drift']['drifted_features']}")

    return drift_metrics
```

## 11. Solución de Problemas

### 11.1 Manejo de Errores Comunes

```python
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
import time

# Función con reintentos para operaciones de Azure
def azure_operation_with_retry(operation, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return operation()
        except HttpResponseError as e:
            if e.status_code == 429:  # Too Many Requests
                print(f"Rate limit alcanzado. Reintento {attempt + 1}/{max_retries}")
                time.sleep(delay * (attempt + 1))
            elif e.status_code >= 500:  # Error del servidor
                print(f"Error del servidor. Reintento {attempt + 1}/{max_retries}")
                time.sleep(delay)
            else:
                raise e
        except ResourceNotFoundError as e:
            print(f"Recurso no encontrado: {e}")
            raise e
    raise Exception(f"Operación falló después de {max_retries} intentos")

# Verificar estado de recursos
def check_resource_health(resource_client, resource_id):
    try:
        resource = resource_client.resources.get_by_id(resource_id, "2023-01-01")
        return resource.properties.get('provisioningState', 'Unknown')
    except HttpResponseError as e:
        return f"Error: {e.message}"

# Diagnosticar problemas de autenticación
def diagnose_auth_issues():
    from azure.identity import CredentialUnavailableError

    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default")
        print("Autenticación exitosa")
        return True
    except CredentialUnavailableError as e:
        print(f"Credenciales no disponibles: {e}")
        print("Verifica que:")
        print("1. Azure CLI esté instalado y logueado (az login)")
        print("2. Las variables de entorno estén configuradas")
        print("3. La identidad administrada esté asignada (si se usa en Azure)")
        return False
    except Exception as e:
        print(f"Error de autenticación: {e}")
        return False
```

### 11.2 Logging y Monitoreo

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Configurar logging completo
def setup_azure_logging(connection_string=None):
    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configurar Azure Monitor si hay connection string
    if connection_string:
        configure_azure_monitor(connection_string)
        print("Azure Monitor configurado")

    return logging.getLogger(__name__)

# Decorador para trazar funciones
def trace_operation(func):
    tracer = trace.get_tracer(__name__)

    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__) as span:
            try:
                # Ejecutar la función
                result = func(*args, **kwargs)
                span.set_status(trace.Status(trace.StatusCode.OK))
                span.set_attribute("result.success", True)
                return result
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                span.set_attribute("result.success", False)
                raise e
    return wrapper

# Ejemplo de función con tracing
@trace_operation
def deploy_model_with_tracing(ml_client, model_id, endpoint_name):
    logger = logging.getLogger(__name__)
    logger.info(f"Iniciando despliegue del modelo {model_id}")

    # Lógica de despliegue
    endpoint = create_online_endpoint(ml_client, endpoint_name)
    deployment = create_model_deployment(ml_client, endpoint_name, "prod", model_id)

    logger.info(f"Despliegue completado: {deployment.name}")
    return deployment
```

### 11.3 Errores de Autenticación

- Verifique los permisos del principal de servicio
- Confirme que el token de acceso no haya expirado
- Valide las asignaciones de roles de Azure RBAC

### 11.4 Problemas de Rendimiento

- Revise los límites de servicio
- Considere particionar cargas de trabajo grandes
- Optimice consultas con proyecciones de campos

### 11.5 Errores de Cuota

- Monitoree el uso de la cuota
- Solicite aumentos de cuota con anticipación
- Considere distribuir cargas entre regiones

## 12. Recursos Adicionales

### 12.1 Patrones de Diseño para Aplicaciones de IA

#### 12.1.1 Arquitectura en Capas

- Capa de presentación
- Capa de API
- Capa de servicios de IA
- Capa de almacenamiento

#### 12.1.2 Patrón de Circuit Breaker

- Previene fallos en cascada
- Implementa reintentos con retroceso exponencial

### 12.2 Consideraciones de Costos

#### 12.2.1 Optimización de Costos

- Apague recursos de desarrollo cuando no estén en uso
- Utilice instancias reservadas para cargas de trabajo predecibles
- Monitoree el uso con Azure Cost Management

#### 12.2.2 Modelos de Precios

- Basado en transacciones (por solicitud)
- Basado en capacidad (reservado)
- Basado en consumo (pago por uso)

### 12.3 Migración desde Servicios Existentes

#### 12.3.1 De Cognitive Services a Azure AI Services

- Actualice los puntos de conexión y las versiones de API
- Revise los cambios en los formatos de respuesta
- Actualice las bibliotecas cliente

### 12.4 Enlaces de Documentación Oficial

- [Azure Python SDK Documentation](https://learn.microsoft.com/python/api/overview/azure/)
- [Azure AI Services Python Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-ml)
- [Azure Machine Learning Python SDK](https://learn.microsoft.com/azure/machine-learning/how-to-configure-environment)
- [Azure Cognitive Services Python SDK](https://learn.microsoft.com/azure/cognitive-services/)
