# Capítulo 4: Temas Avanzados en Fundamentos

En este capítulo, profundizamos en conceptos avanzados para gestionar entornos Azure AI de manera programática usando el SDK de Python, enfocándonos en autenticación avanzada, Role-Based Access Control (RBAC) y soporte para entornos multi-tenant. Este capítulo es crucial para la certificación AI-102, ya que cubre habilidades para gestionar recursos de forma segura y escalable, sin depender del portal de Azure o Azure AI Foundry. Todo se realiza mediante código, con `azure-identity` (v1.24.0), `azure-core` (v1.35.0), y `azure-mgmt-authorization` (v3.0.0) para permisos, además de `azure-mgmt-cognitiveservices` (v13.7.0) para recursos. Construiremos sobre los capítulos anteriores (autenticación básica, creación de recursos, y configuración inicial) para manejar escenarios complejos como entornos empresariales o despliegues multi-región.

## Objetivos del Capítulo

- Implementar autenticación avanzada con `azure-identity` para entornos multi-tenant.
- Configurar RBAC para controlar accesos a recursos Azure AI.
- Gestionar recursos en múltiples tenants o suscripciones vía SDK.
- Monitorear y depurar configuraciones avanzadas con logging.

## Autenticación Avanzada con `azure-identity`

**Explicación**:  
En el Capítulo 2, usamos `DefaultAzureCredential` para autenticación básica, que intenta métodos como variables de entorno o Azure CLI. Ahora, exploraremos autenticación avanzada para escenarios multi-tenant (e.g., gestionar recursos en múltiples organizaciones) y entornos donde se requiere un control más granular. Usaremos `ClientSecretCredential` para autenticación explícita con un service principal, ideal para automatización en CI/CD o entornos empresariales. Esto simula cómo configurarías acceso para servicios de Azure AI Foundry (e.g., agents accediendo a recursos AI) sin UI.

**Paso a Paso**:  

1. Crea un service principal en Azure (puedes usar CLI una vez para obtener credenciales, luego todo es código).
2. Configura autenticación con `ClientSecretCredential`.
3. Valida acceso a recursos en un tenant específico.

**Código Práctico** (guarda como `advanced_auth.py`):

```python
from azure.identity import ClientSecretCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os

# Configura credenciales del service principal
tenant_id = os.environ.get("AZURE_TENANT_ID", "tu-tenant-id")
client_id = os.environ.get("AZURE_CLIENT_ID", "tu-client-id")
client_secret = os.environ.get("AZURE_CLIENT_SECRET", "tu-client-secret")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")

# Crea credencial
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

# Crea cliente para gestionar recursos
client = CognitiveServicesManagementClient(credential, subscription_id)

# Lista recursos para validar autenticación
try:
    print("Recursos Azure AI en el tenant:")
    for account in client.accounts.list():
        print(f"- Nombre: {account.name}, Tipo: {account.kind}, Ubicación: {account.location}")
except Exception as e:
    print(f"Error de autenticación: {e}")
```

**Explicación**:  

- `ClientSecretCredential`: Autentica explícitamente usando un service principal, ideal para scripts automatizados. Obtén `tenant_id`, `client_id`, y `client_secret` creando un service principal con:

  ```bash
  az ad sp create-for-rbac --name "MyApp" --role contributor --scopes /subscriptions/<tu-subscription-id>
  ```

  Esto genera las credenciales necesarias (guarda en variables de entorno).
- `client.accounts.list()`: Valida que el service principal tiene acceso a los recursos.

**Práctica**:  

- Configura las variables de entorno con las credenciales del service principal.
- Ejecuta el código y verifica que lista el recurso Text Analytics creado en el Capítulo 2.
- Modifica para listar recursos en una región específica (e.g., `eastus`).

## Configuración de Role-Based Access Control (RBAC)

**Explicación**:  
RBAC permite controlar quién (o qué) accede a tus recursos Azure AI. Por ejemplo, puedes asignar a un service principal permisos de "Contributor" para gestionar recursos, pero no eliminarlos. Esto es crítico para entornos seguros y alinea con AI-102, donde se evalúa la gestión de permisos. Usaremos `azure-mgmt-authorization` para asignar roles vía código.

**Paso a Paso**:  

1. Identifica el scope del recurso (e.g., un recurso Text Analytics).
2. Asigna un rol (e.g., "Cognitive Services Contributor") a un service principal.
3. Valida el acceso.

**Código Práctico** (guarda como `rbac_setup.py`):

```python
from azure.identity import ClientSecretCredential
from azure.mgmt.authorization import AuthorizationManagementClient
import os

# Configura credenciales
credential = ClientSecretCredential(
    tenant_id=os.environ.get("AZURE_TENANT_ID"),
    client_id=os.environ.get("AZURE_CLIENT_ID"),
    client_secret=os.environ.get("AZURE_CLIENT_SECRET")
)
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics001"

# Obtener scope del recurso
client = CognitiveServicesManagementClient(credential, subscription_id)
resource = client.accounts.get(resource_group, account_name)
scope = resource.id  # ID completo del recurso

# Asignar rol
auth_client = AuthorizationManagementClient(credential, subscription_id)
role_definition_id = f"/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/bef1b86e-c9f7-4e5a-8f90-7d21e0b0c6a3"  # Cognitive Services Contributor
principal_id = os.environ.get("AZURE_PRINCIPAL_ID")  # ID del service principal (obtén con az ad sp show)

try:
    assignment = auth_client.role_assignments.create(
        scope=scope,
        role_assignment_name="unique-role-assignment-id",  # Genera un GUID en producción
        parameters={
            "role_definition_id": role_definition_id,
            "principal_id": principal_id
        }
    )
    print(f"Rol asignado: {assignment.role_definition_id} al principal {principal_id}")
except Exception as e:
    print(f"Error al asignar rol: {e}")
```

**Explicación**:  

- `scope`: Identificador único del recurso (obtenido con `resource.id`).
- `role_definition_id`: ID del rol "Cognitive Services Contributor". Encontrarás IDs en docs.microsoft.com o con `az role definition list`.
- `principal_id`: ID del service principal (obtén con `az ad sp show --id <client_id>`).
- **Nota**: Usa un GUID para `role_assignment_name` en producción (puedes usar `uuid.uuid4()`).

**Práctica**:  

- Ejecuta el código tras obtener `principal_id`. Verifica en el portal (solo para validar) que el rol aparece en el recurso.
- Modifica para asignar el rol "Reader" en lugar de "Contributor". Busca su `role_definition_id` en docs.

## Gestión de Entornos Multi-Tenant

**Explicación**:  
En entornos multi-tenant, un script puede gestionar recursos en múltiples organizaciones (tenants). Esto es útil para consultores o apps que operan en varias suscripciones. Configuraremos autenticación para cambiar entre tenants dinámicamente, simulando un escenario donde gestionas recursos para diferentes clientes de Azure AI Foundry.

**Paso a Paso**:  

1. Configura credenciales para múltiples tenants.
2. Cambia entre tenants en un script.
3. Lista recursos por tenant.

**Código Práctico** (guarda como `multi_tenant.py`):

```python
from azure.identity import ClientSecretCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os

# Lista de tenants y suscripciones
tenants = [
    {"tenant_id": os.environ.get("AZURE_TENANT_ID_1"), "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID_1")},
    {"tenant_id": os.environ.get("AZURE_TENANT_ID_2"), "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID_2")}
]
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")

# Itera por tenants
for tenant in tenants:
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant["tenant_id"],
            client_id=client_id,
            client_secret=client_secret
        )
        client = CognitiveServicesManagementClient(credential, tenant["subscription_id"])
        print(f"\nRecursos en tenant {tenant['tenant_id']}:")
        for account in client.accounts.list():
            print(f"- Nombre: {account.name}, Tipo: {account.kind}")
    except Exception as e:
        print(f"Error en tenant {tenant['tenant_id']}: {e}")
```

**Explicación**:  

- `tenants`: Lista de diccionarios con `tenant_id` y `subscription_id`. Configura variables de entorno para cada tenant.
- `ClientSecretCredential`: Crea una credencial por tenant, reutilizando `client_id` y `client_secret` si el service principal tiene acceso multi-tenant.
- **Nota**: Necesitas permisos en cada tenant (asigna roles como en la sección anterior).

**Práctica**:  

- Configura variables de entorno para al menos un tenant y suscripción. Si no tienes múltiples tenants, simula con una sola suscripción.
- Ejecuta y verifica que lista recursos. Agrega un tenant ficticio y observa el error (para practicar debugging).

## Monitoreo y Debugging con Logging

**Explicación**:  
En entornos avanzados, el logging es esencial para rastrear errores y monitorear operaciones. Configuraremos un sistema de logging robusto para capturar eventos de autenticación, RBAC y acceso multi-tenant.

**Código Práctico** (agrega a cualquier script, e.g., `multi_tenant.py`):

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ejemplo en el bucle de tenants
for tenant in tenants:
    try:
        credential = ClientSecretCredential(
            tenant_id=tenant["tenant_id"],
            client_id=client_id,
            client_secret=client_secret
        )
        logger.info(f"Autenticado en tenant {tenant['tenant_id']}")
        client = CognitiveServicesManagementClient(credential, tenant["subscription_id"])
        for account in client.accounts.list():
            logger.info(f"Recurso encontrado: {account.name}, Tipo: {account.kind}")
    except Exception as e:
        logger.error(f"Error en tenant {tenant['tenant_id']}: {e}")
```

**Explicación**:  

- `logging.basicConfig`: Configura formato con timestamp y nivel (INFO, ERROR).
- `logger.info`/`logger.error`: Registra eventos exitosos o fallos, útil para debugging en CI/CD o entornos multi-tenant.

**Práctica**:  

- Añade logging a `rbac_setup.py`. Registra cada paso (e.g., "Asignando rol", "Rol asignado").
- Simula un error (e.g., usa un `principal_id` inválido) y revisa el log para depurar.

## Notas Adicionales

- **Seguridad**: Almacena `client_secret` en Azure Key Vault para producción (lo cubriremos en módulos posteriores). Nunca lo dejes en código.
- **Azure AI Foundry**: RBAC y multi-tenant son clave para agents en Foundry, que necesitan permisos específicos para acceder a recursos AI.
- **Costos**: Monitorea roles y recursos creados con `azure-mgmt-costmanagement` para evitar cargos innecesarios.

## Práctica Final

1. Ejecuta `advanced_auth.py` con un service principal y verifica que lista recursos.
2. Usa `rbac_setup.py` para asignar un rol "Cognitive Services Contributor" a tu recurso Text Analytics.
3. Configura `multi_tenant.py` con al menos un tenant. Si tienes acceso a otro tenant, prueba con dos.
4. Añade logging a todos los scripts y revisa los logs para un error intencional (e.g., clave inválida).
5. Investiga en docs.microsoft.com otros roles disponibles (e.g., "Cognitive Services User") y prueba asignarlos.
