# Capítulo 2: Setup del Entorno

El setup del entorno es el primer paso práctico para trabajar con Azure AI. Normalmente, crearías recursos (como un servicio de Cognitive Services o Azure OpenAI) a través del portal de Azure, pero con el SDK de Python, puedes hacerlo desde un script, lo que permite integrarlo en pipelines, automatizar despliegues y mantener consistencia en entornos. Usaremos `azure-identity` (v1.24.0) para autenticación segura y `azure-mgmt-cognitiveservices` (v13.7.0) para crear recursos, como un servicio de Text Analytics o Vision. Esto alinea con AI-102, que evalúa tu capacidad para gestionar recursos programáticamente.

Imagina que eres un ingeniero AI que necesita desplegar un servicio de análisis de texto en múltiples regiones sin tocar el portal. Aquí aprenderás a autenticarte (usando métodos seguros como Azure AD o managed identities) y a crear un recurso AI desde cero. Este capítulo va de lo básico (instalación y auth) a lo práctico (crear un recurso), preparando el terreno para módulos posteriores como generative AI o vision.

## Didáctica Paso a Paso

1. **Configuración del Entorno Python**: Asegúrate de tener Python 3.8+ y un entorno virtual. Instala los paquetes necesarios.
2. **Autenticación con `azure-identity`**: Usa `DefaultAzureCredential` para autenticarte sin exponer claves, soportando múltiples métodos (environment vars, CLI, managed identity).
3. **Creación de Recursos**: Usa `azure-mgmt-cognitiveservices` para provisionar un recurso AI (e.g., Text Analytics).
4. **Validación y Debugging**: Verifica el recurso creado y maneja errores comunes en código.

## Código Práctico

A continuación, un ejemplo completo que cubre instalación, autenticación y creación de un recurso Azure AI. Dividimos el proceso en partes para que sea claro.

### Paso 1: Configuración e Instalación

Instala las librerías necesarias:

```bash
pip install azure-identity==1.24.0 azure-mgmt-cognitiveservices==13.7.0 azure-core==1.35.0
```

Crea un entorno virtual si no lo tienes:

```bash
python -m venv myenv
source myenv/bin/activate  # En Windows: myenv\Scripts\activate
```

### Paso 2: Autenticación con `azure-identity`

`DefaultAzureCredential` prueba métodos de autenticación en orden (environment vars, managed identity, CLI, etc.). Configura variables de entorno para pruebas locales (puedes obtenerlas desde el portal una vez, luego todo es código).

**Configura variables de entorno** (en terminal o script):

```bash
export AZURE_SUBSCRIPTION_ID="tu-subscription-id"
export AZURE_TENANT_ID="tu-tenant-id"  # Opcional, para Azure AD
export AZURE_CLIENT_ID="tu-client-id"   # Opcional, para service principal
export AZURE_CLIENT_SECRET="tu-client-secret"  # Opcional
```

Si usas Azure CLI localmente, haz `az login` una vez para pruebas.

**Código de Autenticación** (guarda como `auth_setup.py`):

```bash
export AZURE_SUBSCRIPTION_ID="tu-subscription-id"
export AZURE_TENANT_ID="tu-tenant-id"  # Opcional, para Azure AD
export AZURE_CLIENT_ID="tu-client-id"   # Opcional, para service principal
export AZURE_CLIENT_SECRET="tu-client-secret"  # Opcional
```

Si usas Azure CLI localmente, haz `az login` una vez para pruebas.

**Código de Autenticación** (guarda como `auth_setup.py`):

```python
from azure.identity import DefaultAzureCredential
import os

# Configura credenciales
try:
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    print("Autenticación exitosa con DefaultAzureCredential")
except Exception as e:
    print(f"Error de autenticación: {e}")
    exit(1)

# Prueba simple: Lista suscripciones para verificar auth
from azure.mgmt.resource import SubscriptionClient
client = SubscriptionClient(credential)
for sub in client.subscriptions.list():
    print(f"Suscripción encontrada: {sub.display_name} (ID: {sub.subscription_id})")
```

**Explicación**:

- `DefaultAzureCredential`: Intenta autenticarte automáticamente. Si las variables de entorno están seteadas, usa un service principal; si no, prueba CLI o managed identity.
- `SubscriptionClient`: Valida que puedes acceder a tu suscripción. Si ves el nombre de tu suscripción, la auth funciona.

**Práctica**: Ejecuta el código y verifica el output. Si falla, revisa las variables de entorno o ejecuta `az login`. Asegúrate de reemplazar `tu-subscription-id`.

### Paso 3: Crear un Recurso Azure AI

Vamos a crear un recurso de Text Analytics (un servicio de Cognitive Services para NLP) vía SDK. Esto simula lo que harías para cualquier servicio AI (Vision, OpenAI, etc.).

**Código para Crear Recurso** (guarda como `create_resource.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os

# Configura credenciales y parámetros
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"  # Cambia o crea uno nuevo
account_name = "mytextanalytics001"   # Nombre único para el recurso
location = "eastus"                   # Región Azure
sku_name = "S0"                       # Tier de pricing (S0 es estándar)

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Crea o actualiza el recurso
try:
    parameters = {
        "kind": "TextAnalytics",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()  # Espera a que el recurso se cree
    print(f"Recurso creado: {result.name}, Tipo: {result.kind}, Ubicación: {result.location}")

    # Obtén las claves del recurso
    keys = client.accounts.list_keys(resource_group, account_name)
    print(f"Clave primaria: {keys.key1}")
except Exception as e:
    print(f"Error al crear recurso: {e}")
```

**Explicación**:

- **Resource Group**: Necesitas un grupo de recursos. Si no existe, créalo con `azure-mgmt-resource` (puedes extender el código para esto).
- **Parámetros**: `kind` especifica el tipo de servicio (e.g., "TextAnalytics", "ComputerVision"). `sku` define el tier (S0 es común para pruebas).
- `begin_create`: Operación asíncrona; `poller.result()` espera a que termine.
- `list_keys`: Obtiene claves API para usar el recurso en módulos posteriores (e.g., NLP).

**Práctica**: Ejecuta el código. Cambia `account_name` a algo único (Azure requiere nombres globalmente únicos). Verifica en el portal (solo para confirmar) que el recurso aparece en `resource_group`. Luego, modifica el código para crear un recurso de tipo "ComputerVision".

### Paso 4: Validación y Debugging

- **Validar**: Usa el código del Capítulo 1 (`client.accounts.list()`) para listar y confirmar que el recurso existe.
- **Errores Comunes**:
  - "Authentication failed": Revisa variables de entorno o `az login`.
  - "Resource group not found": Crea uno con `azure-mgmt-resource`.
  - "Name not unique": Cambia `account_name`.

**Código para Crear Resource Group (si necesitas)**:

```python
from azure.mgmt.resource import ResourceManagementClient

client = ResourceManagementClient(credential, subscription_id)
resource_group_params = {"location": location}
client.resource_groups.create_or_update(resource_group, resource_group_params)
print(f"Resource group {resource_group} creado.")
```

## Notas Adicionales

- **Seguridad**: Nunca guardes claves en el código. Usa `azure-identity` para auth y almacena keys en variables de entorno o Azure Key Vault (lo cubriremos en módulos avanzados).
- **Costos**: Usa la suscripción gratuita de Azure o monitorea costos con `azure-mgmt-costmanagement` para evitar sorpresas.
- **Azure AI Foundry**: Aunque Foundry suele ser un framework UI, aquí simulamos su funcionalidad (crear recursos para agents/models) vía SDK. Por ejemplo, el recurso Text Analytics podría usarse en un agent de Azure AI Foundry.

## Práctica Sugerida

1. Ejecuta `auth_setup.py` y verifica autenticación.
2. Ejecuta `create_resource.py` para crear un recurso Text Analytics.
3. Modifica para crear un recurso de tipo "OpenAI" (cambia `kind` a "OpenAI"). Investiga en docs.microsoft.com qué otros `kind` soporta `azure-mgmt-cognitiveservices`.
