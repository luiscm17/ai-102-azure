# Capítulo 3: Instalación y Configuración Inicial

En este capítulo, nos enfocaremos en completar la configuración inicial del entorno de desarrollo para trabajar con el SDK de Python para Azure AI, asegurándonos de que todo esté listo para interactuar con servicios como Cognitive Services, Azure OpenAI o Azure AI Foundry de manera programática. Este paso es esencial para la certificación AI-102, ya que establece las bases para gestionar recursos sin depender del portal de Azure. Vamos a instalar las librerías necesarias, configurar herramientas como Jupyter Notebooks para prototipado y realizar una configuración inicial robusta, todo mediante código Python. Usaremos versiones estables al 25 de agosto de 2025 (verificados en PyPI/docs): `azure-identity` (v1.24.0), `azure-core` (v1.35.0) y `azure-mgmt-cognitiveservices` (v13.7.0), además de otras herramientas útiles.

El objetivo es que tengas un entorno funcional donde puedas ejecutar scripts, probar servicios AI y depurar errores, todo desde código. Este capítulo equilibra teoría y práctica, con ejemplos claros y pasos para validar la configuración.

## Objetivos del Capítulo

- Instalar las librerías base del SDK de Azure y herramientas adicionales.
- Configurar Jupyter Notebooks para prototipado interactivo.
- Realizar una configuración inicial para conectar con servicios Azure AI.
- Validar la instalación y solucionar problemas comunes.

## Instalación de Librerías Base

**Explicación**:  
El SDK de Azure para Python es modular, con paquetes específicos para cada servicio (e.g., `azure-ai-textanalytics` para NLP). Sin embargo, todos dependen de `azure-core` para operaciones HTTP y `azure-identity` para autenticación. Instalaremos estos paquetes base y uno adicional para gestionar recursos (`azure-mgmt-cognitiveservices`). También instalaremos `jupyter` para prototipado, ya que es ideal para pruebas interactivas y visualización de resultados.

**Paso a Paso**:  

1. Asegúrate de tener Python 3.8+ y un entorno virtual activo (creado en el Capítulo 2: `python -m venv myenv` y `source myenv/bin/activate` o `myenv\Scripts\activate` en Windows).
2. Instala las librerías necesarias con pip.

**Código Práctico** (ejecuta en terminal):

```bash
pip install azure-identity==1.24.0 azure-core==1.35.0 azure-mgmt-cognitiveservices==13.7.0 jupyter==1.1.1
```

- `jupyter==1.1.1`: Versión estable para Notebooks. Si prefieres otra IDE (e.g., VS Code), puedes omitirlo, pero lo usaremos para ejemplos.

**Validación**: Verifica la instalación:

```bash
pip list | grep azure
pip list | grep jupyter
```

Deberías ver las versiones instaladas (e.g., `azure-identity 1.24.0`).

**Práctica**: Si usas Windows, macOS o Linux, confirma que el comando `jupyter notebook` inicia un servidor local (<http://localhost:8888>). No lo ejecutes aún, lo configuraremos más adelante.

## Configuración de Jupyter Notebooks

**Explicación**:  
Jupyter Notebooks es ideal para prototipado porque permite ejecutar código en celdas, visualizar outputs (e.g., resultados de un servicio AI) y documentar pasos. Configuraremos un Notebook para interactuar con Azure AI, usando el recurso Text Analytics creado en el Capítulo 2. Esto simula cómo probarías servicios de Azure AI Foundry (e.g., para agents o modelos) sin UI.

**Paso a Paso**:  

1. Inicia Jupyter Notebook.
2. Crea un nuevo Notebook y configura autenticación básica.
3. Escribe un script simple para listar recursos, reutilizando el código del Capítulo 2.

**Código Práctico** (guarda como `setup_notebook.ipynb` en Jupyter):

1. Inicia Jupyter:

    ```bash
    jupyter notebook
    ```

    Abre el navegador en <http://localhost:8888>, crea un nuevo Notebook.

2. En una celda, pega y ejecuta:

    ```python
    # Celda 1: Importar librerías y autenticar
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
    import os
    
    # Configura credenciales
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
    if not subscription_id:
        raise ValueError("Define AZURE_SUBSCRIPTION_ID en variables de entorno")
    
    # Crear cliente
    client = CognitiveServicesManagementClient(credential, subscription_id)
    
    # Celda 2: Listar recursos
    print("Recursos Azure AI disponibles:")
    for account in client.accounts.list():
        print(f"- Nombre: {account.name}, Tipo: {account.kind}, Ubicación: {account.location}")
    ```

**Explicación**:  

- `DefaultAzureCredential`: Reutiliza la autenticación del Capítulo 2. Asegúrate de tener `AZURE_SUBSCRIPTION_ID` configurada.
- `client.accounts.list()`: Lista todos los recursos Cognitive Services, como el Text Analytics creado antes.
- Jupyter permite ejecutar celdas individualmente, ideal para probar y depurar.

**Práctica**:  

- Ejecuta el Notebook. Si ves el recurso Text Analytics del Capítulo 2 (e.g., `mytextanalytics001`), la configuración funciona.
- Agrega una celda para filtrar recursos por `location == 'eastus'`. Usa: `if account.location == 'eastus': print(...)`.

## Configuración Inicial para Servicios Azure AI

**Explicación**:  
Con las librerías instaladas y Jupyter listo, configuramos el entorno para interactuar con un servicio específico (Text Analytics como ejemplo). Esto implica obtener la clave API y el endpoint del recurso creado en el Capítulo 2, que usaremos en módulos posteriores (e.g., NLP, generative AI). Todo se hace vía SDK, simulando cómo configurarías recursos para Azure AI Foundry (como agents o modelos) sin UI.

**Paso a Paso**:  

1. Obtén el endpoint y la clave del recurso Text Analytics.
2. Configura un script para probar la conexión al servicio.
3. Guarda credenciales de forma segura (evitando hardcoding).

**Código Práctico** (agrega a `setup_notebook.ipynb` o crea `initial_config.py`):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.ai.textanalytics import TextAnalyticsClient
import os

# Configura credenciales y parámetros
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "mytextanalytics001"

# Obtener endpoint y clave
client = CognitiveServicesManagementClient(credential, subscription_id)
account = client.accounts.get(resource_group, account_name)
endpoint = account.properties.endpoint
keys = client.accounts.list_keys(resource_group, account_name)
api_key = keys.key1

print(f"Endpoint: {endpoint}, Clave: {api_key[:4]}... (truncada por seguridad)")

# Probar conexión al servicio Text Analytics
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=api_key)
try:
    response = text_analytics_client.recognize_entities(documents=["Test document"])
    print("Conexión exitosa. Entidades detectadas:", response[0].entities)
except Exception as e:
    print(f"Error al conectar: {e}")
```

**Explicación**:  

- `client.accounts.get`: Obtiene detalles del recurso, incluyendo el endpoint (e.g., `https://mytextanalytics001.cognitiveservices.azure.com/`).
- `list_keys`: Extrae la clave API para autenticar con el servicio.
- `TextAnalyticsClient`: Cliente para interactuar con Text Analytics. La prueba con `recognize_entities` valida que el servicio está accesible.
- **Seguridad**: La clave se imprime truncada. En producción, usa Azure Key Vault (lo cubriremos en módulos avanzados).

**Práctica**:  

- Ejecuta el código en Jupyter o como script. Si ves entidades (o un error diciendo que el documento está vacío), la conexión funciona.
- Modifica el código para usar `key2` en lugar de `key1`. Investiga en docs.microsoft.com cómo regenerar claves con `client.accounts.regenerate_key`.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración asegura que estás listo para módulos posteriores. Errores comunes incluyen versiones incompatibles, credenciales mal configuradas o recursos no disponibles.

**Paso a Paso**:  

1. Verifica versiones: `pip list | grep azure` debe mostrar las versiones correctas.
2. Confirma autenticación: Si `client.accounts.list()` falla, revisa `AZURE_SUBSCRIPTION_ID` o haz `az login`.
3. Prueba el servicio: El código de Text Analytics debe devolver un resultado o un error manejable.
4. Debugging: Usa `try-except` para capturar errores y logging para más detalles.

**Código para Logging Básico** (agrega a cualquier script):

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Tu código aquí, e.g., text_analytics_client.recognize_entities(...)
    logger.info("Operación exitosa")
except Exception as e:
    logger.error(f"Error: {e}")
```

**Práctica**:  

- Añade logging al código anterior y registra cada paso (e.g., "Conectando al cliente", "Recurso creado").
- Si encuentras un error, usa el mensaje para buscar en docs.microsoft.com o Stack Overflow.

## Notas Adicionales

- **Azure AI Foundry**: Aunque Foundry suele implicar UI, aquí usamos el SDK para replicar su funcionalidad (e.g., crear recursos para agents). Este código es compatible con pipelines que alimentarían Foundry.
- **Escalabilidad**: Guarda endpoints y claves en variables de entorno o un archivo `.env` con `python-dotenv` para entornos reales.
- **Costos**: Monitorea recursos creados para evitar cargos. Usa `client.accounts.delete` para eliminar si no los necesitas.

## Práctica Final

1. Crea un Notebook con las celdas del código anterior. Ejecuta y valida que el recurso Text Analytics está accesible.
2. Modifica el código para probar otro servicio (e.g., `ComputerVision` en lugar de `TextAnalytics`). Cambia `kind` en el Capítulo 2 y ajusta el cliente (usa `azure-ai-vision-imageanalysis`).
3. Investiga en PyPI qué otros paquetes Azure AI están disponibles (e.g., `azure-ai-documentintelligence`) y anótalos para módulos futuros.
