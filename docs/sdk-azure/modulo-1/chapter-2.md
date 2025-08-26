# Capítulo 2: Gestión de Recursos

En este capítulo, nos enfocamos en la gestión programática de recursos de Azure AI usando el SDK de Python, específicamente con los paquetes `azure-mgmt-cognitiveservices` (v13.7.0) para servicios como Azure OpenAI o Text Analytics, y `azure-ai-ml` (v1.28.1) para Azure Machine Learning. Este capítulo es fundamental para la certificación AI-102, ya que cubre cómo crear, actualizar, escalar y eliminar recursos sin depender del portal de Azure o interfaces como Azure AI Foundry. Todo se hará mediante código, permitiendo automatización y escalabilidad en entornos reales, como los requeridos para agentes o soluciones generativas en Azure AI Foundry.

Construiremos sobre los fundamentos del Módulo 0, usando autenticación segura con `azure-identity` (v1.24.0) y extendiendo la creación de recursos vista en el Capítulo 2 del Módulo 0. Cubriremos el despliegue de recursos, actualización de propiedades (como el tier de precios), y gestión de Azure Machine Learning workspaces, con ejemplos prácticos y validación.

## Objetivos del Capítulo

- Crear y gestionar recursos de Cognitive Services usando `azure-mgmt-cognitiveservices`.
- Configurar y administrar workspaces de Azure Machine Learning con `azure-ai-ml`.
- Actualizar y escalar recursos vía SDK.
- Implementar logging para monitoreo y depuración.

## Creación de Recursos de Cognitive Services

**Explicación**:  
Azure Cognitive Services incluye servicios como Text Analytics, Computer Vision y Azure OpenAI. Usaremos `azure-mgmt-cognitiveservices` para desplegar estos recursos programáticamente. Por ejemplo, podemos crear un recurso de Azure OpenAI para soportar modelos generativos o un recurso de Text Analytics para NLP. Esto simula cómo configurarías recursos para Azure AI Foundry (e.g., para agents que usan modelos AI) sin UI.

**Paso a Paso**:  

1. Autenticar con `DefaultAzureCredential`.
2. Crear un recurso Cognitive Services (e.g., Text Analytics).
3. Validar la creación y obtener endpoint/clave.

**Código Práctico** (guarda como `create_cognitive_resource.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "mytextanalytics002"  # Nombre único
location = "eastus"
sku_name = "S0"  # Tier estándar

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Crea recurso
try:
    logger.info(f"Creando recurso {account_name} en {resource_group}")
    parameters = {
        "kind": "TextAnalytics",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso creado: {result.name}, Tipo: {result.kind}, Ubicación: {result.location}")

    # Obtener endpoint y clave
    endpoint = result.properties.endpoint
    keys = client.accounts.list_keys(resource_group, account_name)
    logger.info(f"Endpoint: {endpoint}, Clave: {keys.key1[:4]}...")
except Exception as e:
    logger.error(f"Error al crear recurso: {e}")
```

**Explicación**:  

- `begin_create`: Operación asíncrona para crear el recurso. `poller.result()` espera a que termine.
- `kind`: Especifica el tipo de servicio (e.g., "TextAnalytics", "OpenAI", "ComputerVision").
- `list_keys`: Obtiene claves API para interactuar con el recurso en módulos posteriores.
- **Seguridad**: La clave se trunca en el log. Usa variables de entorno o Azure Key Vault en producción.

**Práctica**:  

- Ejecuta el código con un `account_name` único. Verifica el recurso en el portal (solo para validar, luego evita UI).
- Cambia `kind` a "OpenAI" y crea un recurso para modelos generativos. Guarda el endpoint/clave para el Módulo 2.

## Gestión de Workspaces de Azure Machine Learning

**Explicación**:  
Azure Machine Learning (AML) permite entrenar, desplegar y gestionar modelos de machine learning. Usaremos `azure-ai-ml` para crear y configurar un workspace, que es el contenedor para experimentos, modelos y despliegues. Esto es clave para AI-102, ya que AML se usa para fine-tuning o integración con generative AI.

**Paso a Paso**:  

1. Crear un workspace AML.
2. Configurar propiedades básicas (e.g., almacenamiento, key vault).
3. Validar el workspace.

**Código Práctico** (guarda como `create_ml_workspace.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
workspace_name = "myamlworkspace001"  # Nombre único
location = "eastus"

# Crea cliente
client = MLClient(credential, subscription_id, resource_group, workspace_name=workspace_name)

# Crea workspace
try:
    workspace = Workspace(
        name=workspace_name,
        resource_group=resource_group,
        location=location,
        display_name="Mi Workspace ML",
        description="Workspace para AI-102"
    )
    logger.info(f"Creando workspace {workspace_name}")
    client.workspaces.begin_create(workspace)
    logger.info(f"Workspace {workspace_name} creado exitosamente")
except Exception as e:
    logger.error(f"Error al crear workspace: {e}")

# Lista workspaces para validar
try:
    for ws in client.workspaces.list():
        logger.info(f"Workspace encontrado: {ws.name}, Ubicación: {ws.location}")
except Exception as e:
    logger.error(f"Error al listar workspaces: {e}")
```

**Explicación**:  

- `MLClient`: Cliente para gestionar AML. Requiere `azure-ai-ml` (v1.28.1).
- `Workspace`: Define el workspace con propiedades como nombre y ubicación.
- `begin_create`: Crea el workspace asíncronamente. Incluye recursos asociados (almacenamiento, Key Vault) automáticamente.

**Práctica**:  

- Ejecuta el código con un `workspace_name` único. Verifica el workspace en el portal (solo para validar).
- Modifica para agregar un `description` diferente o cambiar `location` a otra región (e.g., "westus").

## Actualización y Escalado de Recursos

**Explicación**:  
Los recursos pueden actualizarse (e.g., cambiar el tier de precios) o escalarse (e.g., aumentar capacidad) vía SDK. Esto es útil para optimizar costos o rendimiento, como en escenarios de Azure AI Foundry donde un agent necesita más capacidad para procesar solicitudes.

**Paso a Paso**:  

1. Actualiza el tier de un recurso Cognitive Services (e.g., de S0 a S1).
2. Verifica la capacidad del recurso.

**Código Práctico** (guarda como `update_resource.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics002"

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Actualiza recurso
try:
    logger.info(f"Actualizando recurso {account_name} a tier S1")
    parameters = {
        "sku": {"name": "S1"},  # Cambia de S0 a S1
        "properties": {}
    }
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso actualizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"Error al actualizar: {e}")
```

**Explicación**:  

- `begin_update`: Cambia propiedades del recurso, como el tier de precios (`sku`).
- `S1`: Tier superior a `S0`, con más capacidad (verifica costos en docs.microsoft.com).
- **Nota**: No todos los servicios admiten todos los tiers; consulta la documentación para tu `kind`.

**Práctica**:  

- Ejecuta el código para cambiar el tier de `mytextanalytics002` a `S1`.
- Modifica para revertir a `S0`. Investiga otros tiers disponibles (e.g., `F0` para free tier, si aplica).

## Validación y Solución de Problemas

**Explicación**:  
Validar la creación y actualización de recursos asegura que están listos para módulos posteriores (e.g., NLP, generative AI). Errores comunes incluyen nombres no únicos, permisos insuficientes o regiones no soportadas.

**Paso a Paso**:  

1. Lista recursos para confirmar creación/actualización.
2. Usa logging para rastrear errores.
3. Revisa permisos si falla (ver Capítulo 4, Módulo 0 para RBAC).

**Código para Validación** (agrega a cualquier script):

```python
# Lista recursos Cognitive Services
try:
    for account in client.accounts.list():
        logger.info(f"Recurso: {account.name}, SKU: {account.sku.name}, Ubicación: {account.location}")
except Exception as e:
    logger.error(f"Error al listar: {e}")

# Lista workspaces AML
try:
    for ws in client.workspaces.list():
        logger.info(f"Workspace: {ws.name}, Ubicación: {ws.location}")
except Exception as e:
    logger.error(f"Error al listar: {e}")
```

**Práctica**:  

- Ejecuta el código de validación tras cada script. Confirma que `mytextanalytics002` y `myamlworkspace001` aparecen.
- Simula un error (e.g., usa un `resource_group` inválido) y revisa el log.

## Notas Adicionales

- **Azure AI Foundry**: La gestión de recursos vía SDK es la base para configurar agents o modelos generativos en Foundry, ya que estos requieren recursos como OpenAI o AML workspaces.
- **Seguridad**: Usa Azure Key Vault para claves (lo cubriremos en módulos avanzados). Evita hardcoding.
- **Costos**: Monitorea con `azure-mgmt-costmanagement` para evitar cargos por recursos no utilizados. Elimina recursos con `client.accounts.delete` si no los necesitas.

## Práctica Final

1. Ejecuta `create_cognitive_resource.py` para crear un recurso Text Analytics. Valida con el código de listado.
2. Ejecuta `create_ml_workspace.py` para crear un workspace AML. Confirma su creación.
3. Usa `update_resource.py` para cambiar el tier de `mytextanalytics002` a `S1` y verifica el cambio.
4. Modifica `create_cognitive_resource.py` para crear un recurso de tipo `ComputerVision`. Guarda endpoint/clave.
5. Investiga en docs.microsoft.com otros `kind` soportados por `azure-mgmt-cognitiveservices` (e.g., `Face`, `SpeechServices`).

```python
# create_cognitive_resource.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "mytextanalytics002"  # Nombre único
location = "eastus"
sku_name = "S0"  # Tier estándar

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Crea recurso

try:
    logger.info(f"Creando recurso {account_name} en {resource_group}")
    parameters = {
        "kind": "TextAnalytics",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso creado: {result.name}, Tipo: {result.kind}, Ubicación: {result.location}")

    # Obtener endpoint y clave
    endpoint = result.properties.endpoint
    keys = client.accounts.list_keys(resource_group, account_name)
    logger.info(f"Endpoint: {endpoint}, Clave: {keys.key1[:4]}...")
except Exception as e:
    logger.error(f"Error al crear recurso: {e}")
```

```python
# create_ml_workspace.py
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
workspace_name = "myamlworkspace001"  # Nombre único
location = "eastus"

# Crea cliente

client = MLClient(credential, subscription_id, resource_group, workspace_name=workspace_name)

# Crea workspace

try:
    workspace = Workspace(
        name=workspace_name,
        resource_group=resource_group,
        location=location,
        display_name="Mi Workspace ML",
        description="Workspace para AI-102"
    )
    logger.info(f"Creando workspace {workspace_name}")
    client.workspaces.begin_create(workspace)
    logger.info(f"Workspace {workspace_name} creado exitosamente")
except Exception as e:
    logger.error(f"Error al crear workspace: {e}")

# Lista workspaces para validar

try:
    for ws in client.workspaces.list():
        logger.info(f"Workspace encontrado: {ws.name}, Ubicación: {ws.location}")
except Exception as e:
    logger.error(f"Error al listar workspaces: {e}")
```

```python
# update_resource.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

# Configurar logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics002"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Actualiza recurso

try:
    logger.info(f"Actualizando recurso {account_name} a tier S1")
    parameters = {
        "sku": {"name": "S1"},  # Cambia de S0 a S1
        "properties": {}
    }
    poller = client.accounts.begin_update(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso actualizado: {result.name}, SKU: {result.sku.name}")
except Exception as e:
    logger.error(f"Error al actualizar: {e}")
```
