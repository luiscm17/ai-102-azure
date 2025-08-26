# Capítulo 6: Setup y Configuración Básica

En este capítulo, configuramos el entorno para desarrollar agentes de IA (*agentic AI*) usando los SDKs `azure-ai-generative` (v1.0.0b11), `openai` (v1.101.0) con extensiones para agentes, y `azure-mcp-server` (v0.1.0, preview) para conectar a recursos de Azure mediante comandos en lenguaje natural. Implementaremos un agente básico que mantiene una conversación multi-turno, usa *tool calling* para ejecutar funciones externas, y simula la orquestación de contexto con MCP. Todos los ejemplos usarán autenticación segura con `azure-identity` (v1.24.0) y logging para monitoreo y depuración, preparando el terreno para temas avanzados como RAG y herramientas personalizadas en los capítulos siguientes.

## Objetivos del Capítulo

- Configurar los SDKs `azure-ai-generative`, `openai`, y `azure-mcp-server`.
- Crear un agente básico que procese comandos en lenguaje natural.
- Conectar el agente a recursos Azure (e.g., Azure OpenAI) usando *tool calling*.
- Simular MCP para gestión de contexto y conexiones externas.

## Configuración del Entorno

**Explicación**:  
Para desarrollar agentes *agentic*, necesitamos configurar los SDKs necesarios y autenticar con Azure OpenAI. Aunque `azure-ai-generative` y `azure-mcp-server` están en beta/preview, usaremos `openai` como base para la mayoría de las interacciones, simulando funcionalidades de MCP donde la documentación es limitada. Configuraremos el cliente con autenticación vía `DefaultAzureCredential` o clave API, y prepararemos el entorno para procesar comandos en lenguaje natural.

**Paso a Paso**:  

1. Instala los SDKs requeridos.
2. Configura el cliente `openai` para Azure OpenAI.
3. Valida la conexión con un comando simple.

**Código Práctico** (instalación en terminal):

```bash
pip install openai==1.101.0 azure-identity==1.24.0 azure-ai-generative==1.0.0b11
# Nota: azure-mcp-server (v0.1.0) es preview, instalación puede requerir un canal beta
```

**Código para Configuración** (guarda como `setup_agent_env.py`):

```python
# setup_agent_env.py
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("agent_setup.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
api_version = "2024-08-01-preview"
model = "gpt-35-turbo"

# Inicializa cliente

try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    logger.info(f"Cliente Azure OpenAI configurado para {endpoint}")
except Exception as e:
    logger.error(f"Error al configurar cliente: {e}")
    exit(1)

# Prueba de conexión

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un agente de IA para Azure."},
            {"role": "user", "content": "Confirma que estás conectado."}
        ],
        max_tokens=50
    )
    logger.info("Conexión exitosa con Azure OpenAI")
    print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    logger.error(f"Error en prueba de conexión: {e}")
```

**Explicación**:  

- `AzureOpenAI`: Cliente configurado para Azure OpenAI, usando `api_key` para simplicidad (Azure AD se usará en escenarios avanzados).
- **Nota**: `azure-ai-generative` y `azure-mcp-server` no se usan directamente aquí debido a su estado beta; simularemos sus funcionalidades con `openai`.
- **Logging**: Registra operaciones en `agent_setup.log`.

**Práctica**:  

- Configura `AZURE_OPENAI_ENDPOINT` y `AZURE_OPENAI_API_KEY` en variables de entorno.
- Ejecuta el script y verifica la conexión. Cambia el prompt a "Describe el rol de un agente de IA".
- Revisa `agent_setup.log` para confirmar la configuración.

## Creación de un Agente Básico

**Explicación**:  
Crearemos un agente básico que procesa comandos en lenguaje natural, mantiene una conversación multi-turno, y usa *tool calling* para interactuar con recursos externos (e.g., obtener información del sistema). Este agente simula funcionalidades de `azure-ai-generative` y MCP, usando `openai` para manejar la lógica principal. El ejemplo incluye una herramienta simple para obtener la hora actual.

**Paso a Paso**:  

1. Define una herramienta para una tarea específica.
2. Configura una conversación multi-turno con *tool calling*.
3. Procesa comandos en lenguaje natural.

**Código Práctico** (guarda como `basic_agent.py`):

```python
# basic_agent.py
from openai import AzureOpenAI
import os
import logging
import json
from datetime import datetime

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("basic_agent.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Define herramienta

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Obtiene la hora actual en formato HH:MM:SS.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Función real

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

# Conversación multi-turno con tool calling

try:
    logger.info("Iniciando agente con conversación multi-turno")
    messages = [
        {"role": "system", "content": "Eres un agente de IA que procesa comandos en lenguaje natural y usa herramientas."},
        {"role": "user", "content": "¿Qué es un agente de IA?"},
        {"role": "assistant", "content": "Un agente de IA es un sistema que combina modelos generativos, contexto y herramientas para tareas complejas."},
        {"role": "user", "content": "Dime la hora actual."}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=150,
        temperature=0.7
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        logger.info(f"Tool call detectado: {tool_call.function.name}")
        result = get_current_time()
        logger.info(f"Resultado de la herramienta: {result}")
        messages.append({"role": "assistant", "content": f"La hora actual es {result}."})
        print(f"Respuesta: La hora actual es {result}.")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `tools`: Define una función (`get_current_time`) que el agente puede invocar.
- `messages`: Mantiene el contexto de una conversación multi-turno.
- `tool_choice="auto"`: Permite al modelo decidir si usa la herramienta.
- **MCP (simulación)**: Este ejemplo simula un agente que podría usar MCP para orquestar herramientas y contexto; la implementación real se cubrirá en el Capítulo 4.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Añade un nuevo turno al `messages` (e.g., "user": "¿Qué día es hoy?").
- Crea una nueva herramienta (e.g., `get_current_day`) para devolver el día de la semana.
- Revisa `basic_agent.log` para confirmar la ejecución.

## Simulación de MCP para Conexión a Recursos Azure

**Explicación**:  
El Multi-Context Protocol (MCP) permite a los agentes coordinar múltiples fuentes de datos y herramientas externas. Dado que `azure-mcp-server` (v0.1.0) está en preview y su documentación es limitada, simularemos su funcionalidad integrando una herramienta que podría conectar con un recurso Azure (e.g., Azure OpenAI para validar modelos desplegados). Usaremos `azure-mgmt-cognitiveservices` para simular una consulta a un recurso externo.

**Paso a Paso**:  

1. Define una herramienta para consultar modelos desplegados.
2. Integra la herramienta en una conversación multi-turno.
3. Simula la orquestación de contexto con MCP.

**Código Práctico** (guarda como `mcp_simulation.py`):

```python
# mcp_simulation.py
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging
import json

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mcp_simulation.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura clientes

credential = DefaultAzureCredential()
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "myopenai002"
model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")
mgmt_client = CognitiveServicesManagementClient(credential, subscription_id)

# Define herramienta

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_deployed_models",
            "description": "Lista los modelos desplegados en un recurso Azure OpenAI.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Función real

def list_deployed_models():
    try:
        deployments = mgmt_client.deployments.list(resource_group, account_name)
        return [deployment.name for deployment in deployments]
    except Exception as e:
        return f"Error: {str(e)}"

# Conversación multi-turno con MCP simulado

try:
    logger.info("Iniciando agente con MCP simulado")
    messages = [
        {"role": "system", "content": "Eres un agente que consulta recursos Azure."},
        {"role": "user", "content": "Dime qué es Azure OpenAI."},
        {"role": "assistant", "content": "Azure OpenAI es un servicio de Microsoft para modelos de IA generativa."},
        {"role": "user", "content": "Lista los modelos desplegados en mi recurso."}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=150,
        temperature=0.7
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        logger.info(f"Tool call detectado: {tool_call.function.name}")
        result = list_deployed_models()
        logger.info(f"Resultado de la herramienta: {result}")
        messages.append({"role": "assistant", "content": f"Modelos desplegados: {result}"})
        print(f"Respuesta: Modelos desplegados: {result}")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `tools`: Define una función (`list_deployed_models`) que consulta modelos desplegados.
- `mgmt_client`: Simula una conexión externa a un recurso Azure, como haría MCP.
- **MCP (simulación)**: La herramienta actúa como un proxy para MCP, orquestando la consulta a un servicio externo.
- **Azure AI Foundry**: Este ejemplo simula un agente que consulta recursos para responder comandos en lenguaje natural.

**Práctica**:  

- Configura `AZURE_SUBSCRIPTION_ID`, `AZURE_OPENAI_ENDPOINT`, y `AZURE_OPENAI_API_KEY`.
- Ejecuta el script y revisa la lista de modelos. Añade un nuevo turno (e.g., "user": "¿Qué modelos soporta Azure OpenAI?").
- Crea una nueva herramienta (e.g., `get_resource_status`) para verificar el estado del recurso.
- Revisa `mcp_simulation.log`.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración asegura que el agente funcione correctamente. Errores comunes incluyen modelos no desplegados, permisos insuficientes o herramientas mal definidas.

**Paso a Paso**:  

1. Verifica que `gpt-35-turbo` está desplegado.
2. Confirma las credenciales y el endpoint.
3. Usa logging para depurar.

**Código para Validar Modelos** (reutilizamos del Capítulo 1):

```python
# validate_deployments.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("validate_deployments.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "myopenai002"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Lista modelos desplegados

try:
    logger.info(f"Listando despliegues para {account_name}")
    deployments = client.deployments.list(resource_group, account_name)
    for deployment in deployments:
        logger.info(f"- Despliegue: {deployment.name}")
except Exception as e:
    logger.error(f"Error al listar despliegues: {e}")
```

**Práctica**:  

- Ejecuta el código para listar modelos. Asegúrate de que `gpt-35-turbo` está disponible.
- Simula un error (e.g., clave API inválida) y revisa `validate_deployments.log`.

## Notas Adicionales

- **Azure AI Foundry**: Los agentes configurados aquí son la base para asistentes avanzados que usan comandos en lenguaje natural.
- **Costos**: Monitorea `response.usage.total_tokens` para optimizar gastos. Usa tiers bajos para pruebas.
- **MCP (beta)**: La simulación de MCP prepara para implementaciones reales en el Capítulo 4.

## Práctica Final

1. Ejecuta `setup_agent_env.py` y valida la conexión.
2. Usa `basic_agent.py` para procesar un nuevo comando (e.g., "¿Qué día es hoy?") y añade una herramienta.
3. Ejecuta `mcp_simulation.py` y prueba con un nuevo turno o herramienta.
4. Usa `validate_deployments.py` para confirmar modelos desplegados.
5. Investiga en docs.microsoft.com sobre `azure-ai-generative` y sus extensiones para agentes.
