# Capítulo 7: Uso Intermedio

En este capítulo, desarrollamos agentes de IA con funcionalidades intermedias, integrando *tool calling* para ejecutar múltiples funciones externas, simulando interacciones multi-canal (texto y voz a través de MCP), y manejando contexto para conectar con fuentes de datos externas. Usaremos `openai` (v1.101.0) para la lógica principal, simulando aspectos de `azure-ai-generative` (v1.0.0b11) y `azure-mcp-server` (v0.1.0, preview) debido a su estado beta. Los ejemplos incluirán un agente que procesa comandos en lenguaje natural, usa herramientas para consultar datos (e.g., Azure resources), y simula interacciones de voz mediante texto estructurado. Todo se implementará con autenticación segura y logging para monitoreo, preparando el terreno para temas avanzados como RAG en agentes y herramientas personalizadas en el Capítulo 4.

## Objetivos del Capítulo

- Implementar un agente con múltiples herramientas usando *tool calling*.
- Simular interacciones multi-canal (texto y voz) con MCP.
- Gestionar contexto para conectar con fuentes de datos externas.
- Monitorear y depurar con logging robusto.

## Agente con Múltiples Herramientas (Tool Calling Avanzado)

**Explicación**:  
Un agente *agentic* puede usar múltiples herramientas para resolver tareas complejas, como consultar información, realizar cálculos o interactuar con servicios externos. Ampliaremos el *tool calling* del Capítulo 2 para incluir varias herramientas (e.g., obtener la fecha, calcular un promedio) y manejar decisiones dinámicas basadas en el contexto del usuario. Esto simula cómo un agente en Azure AI Foundry procesa comandos complejos.

**Paso a Paso**:  

1. Define múltiples herramientas con esquemas JSON.
2. Configura una conversación multi-turno con *tool calling*.
3. Procesa las respuestas y ejecuta las herramientas correspondientes.

**Código Práctico** (guarda como `multi_tool_agent.py`):

```python
# multi_tool_agent.py
from openai import AzureOpenAI
import os
import logging
import json
from datetime import datetime
import statistics

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("multi_tool_agent.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Define herramientas

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Obtiene la fecha actual en formato YYYY-MM-DD.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_average",
            "description": "Calcula el promedio de una lista de números.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Lista de números para promediar"
                    }
                },
                "required": ["numbers"]
            }
        }
    }
]

# Funciones reales

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def calculate_average(numbers):
    return statistics.mean(numbers)

# Conversación multi-turno con múltiples herramientas

try:
    logger.info("Iniciando agente con múltiples herramientas")
    messages = [
        {"role": "system", "content": "Eres un agente de IA que usa herramientas para responder."},
        {"role": "user", "content": "¿Qué es un agente de IA?"},
        {"role": "assistant", "content": "Un agente de IA combina modelos generativos y herramientas para tareas complejas."},
        {"role": "user", "content": "Dime la fecha actual y calcula el promedio de [10, 20, 30]."}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=200,
        temperature=0.7
    )
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            logger.info(f"Tool call detectado: {tool_call.function.name}")
            if tool_call.function.name == "get_current_date":
                result = get_current_date()
                messages.append({"role": "assistant", "content": f"Fecha actual: {result}"})
                print(f"Fecha actual: {result}")
            elif tool_call.function.name == "calculate_average":
                args = json.loads(tool_call.function.arguments)
                result = calculate_average(args["numbers"])
                messages.append({"role": "assistant", "content": f"Promedio: {result}"})
                print(f"Promedio: {result}")
            logger.info(f"Resultado de la herramienta: {result}")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `tools`: Define dos funciones: `get_current_date` y `calculate_average`.
- `tool_calls`: El modelo puede invocar múltiples herramientas en una sola respuesta.
- `messages`: Mantiene el contexto de la conversación multi-turno.
- **Azure AI Foundry**: Simula un agente que procesa comandos complejos combinando varias herramientas.

**Práctica**:  

- Ejecuta el script y revisa las respuestas. Cambia los números en el prompt a `[15, 25, 35, 45]`.
- Añade una nueva herramienta (e.g., `calculate_sum`) y actualiza el prompt para usarla.
- Revisa `multi_tool_agent.log` para confirmar las herramientas ejecutadas.

## Interacciones Multi-Canal (Texto y Voz Simulada)

**Explicación**:  
Los agentes *agentic* pueden interactuar a través de múltiples canales, como texto y voz, usando MCP para orquestar el contexto. Dado que `azure-mcp-server` está en preview, simularemos interacciones de voz convirtiendo comandos de texto en un formato que simula entrada de voz (e.g., texto estructurado con marcas de voz). El agente procesará estos comandos y mantendrá el contexto conversacional.

**Paso a Paso**:  

1. Define un formato para comandos de voz simulados (e.g., texto con prefijo "VOZ:").
2. Configura un agente que procesa texto y voz simulada.
3. Usa *tool calling* para responder a comandos.

**Código Práctico** (guarda como `multi_channel_agent.py`):

```python
# multi_channel_agent.py
from openai import AzureOpenAI
import os
import logging
import json
from datetime import datetime

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("multi_channel_agent.log"), logging.StreamHandler()]
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

# Procesar comando de voz simulado

def process_voice_command(text):
    if text.startswith("VOZ:"):
        return text.replace("VOZ:", "").strip()
    return text

# Conversación multi-canal

try:
    logger.info("Iniciando agente multi-canal")
    messages = [
        {"role": "system", "content": "Eres un agente que maneja texto y comandos de voz simulados."},
        {"role": "user", "content": "Explica qué es un agente multi-canal."},
        {"role": "assistant", "content": "Un agente multi-canal procesa entradas de texto y voz, manteniendo contexto."},
        {"role": "user", "content": "VOZ: Dime la hora actual."}
    ]
    processed_command = process_voice_command(messages[-1]["content"])
    messages[-1]["content"] = processed_command
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
        messages.append({"role": "assistant", "content": f"Hora actual: {result} (vía voz simulada)"})
        print(f"Respuesta: Hora actual: {result} (vía voz simulada)")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `process_voice_command`: Simula la conversión de un comando de voz (prefijo "VOZ:") a texto.
- `tools`: Incluye una función para manejar comandos específicos.
- **Multi-canal**: El agente procesa tanto texto como comandos de voz simulados, manteniendo contexto.
- **MCP (simulación)**: La gestión de entradas multi-canal refleja cómo MCP orquestaría texto y voz.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Añade un nuevo comando de voz (e.g., "VOZ: ¿Qué día es hoy?").
- Crea una nueva herramienta para procesar comandos de voz (e.g., `get_current_day`).
- Revisa `multi_channel_agent.log`.

## Manejo de Contexto con MCP

**Explicación**:  
El Multi-Context Protocol (MCP) permite a los agentes gestionar contexto de múltiples fuentes (e.g., historial de conversación, datos externos). Dado que `azure-mcp-server` está en preview, simularemos la gestión de contexto almacenando el historial en memoria y conectando con una fuente de datos externa (e.g., Azure Cognitive Search para un RAG simple). Esto prepara para integraciones más avanzadas en el Capítulo 4.

**Paso a Paso**:  

1. Almacena el historial de conversación en memoria.
2. Integra una fuente de datos externa (simulada con una lista de documentos).
3. Usa *tool calling* para consultar datos y responder.

**Código Práctico** (guarda como `context_mcp_agent.py`):

```python
# context_mcp_agent.py
from openai import AzureOpenAI
import os
import logging
import json
import numpy as np

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("context_mcp_agent.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"
embedding_model = "text-embedding-ada-002"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Simulación de fuente de datos externa

documents = [
    {"id": "1", "content": "Azure AI Foundry soporta agentes generativos avanzados."},
    {"id": "2", "content": "MCP coordina múltiples fuentes de datos para agentes."}
]

# Define herramienta para búsqueda

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Busca documentos relevantes usando embeddings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta para buscar"}
                },
                "required": ["query"]
            }
        }
    }
]

# Función para generar embeddings

def get_embedding(text):
    response = client.embeddings.create(model=embedding_model, input=text)
    return response.data[0].embedding

# Función de búsqueda simulada

def search_documents(query):
    query_embedding = get_embedding(query)
    doc_embeddings = [get_embedding(doc["content"]) for doc in documents]
    similarities = [np.dot(query_embedding, doc_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)) for doc_emb in doc_embeddings]
    best_doc_idx = np.argmax(similarities)
    return documents[best_doc_idx]["content"]

# Conversación con manejo de contexto

try:
    logger.info("Iniciando agente con MCP simulado")
    messages = [
        {"role": "system", "content": "Eres un agente que usa MCP para gestionar contexto y fuentes externas."},
        {"role": "user", "content": "¿Qué es MCP?"},
        {"role": "assistant", "content": "MCP es un protocolo para coordinar contexto y datos externos en agentes de IA."},
        {"role": "user", "content": "Busca información sobre MCP en documentos."}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=200,
        temperature=0.7
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        logger.info(f"Tool call detectado: {tool_call.function.name}")
        args = json.loads(tool_call.function.arguments)
        result = search_documents(args["query"])
        logger.info(f"Resultado de la búsqueda: {result}")
        messages.append({"role": "assistant", "content": f"Información encontrada: {result}"})
        print(f"Respuesta: Información encontrada: {result}")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `documents`: Simula una fuente de datos externa (en memoria, como en RAG simple del Capítulo 3, Módulo 2).
- `search_documents`: Usa embeddings para buscar el documento más relevante, simulando MCP.
- **Contexto**: El historial de `messages` actúa como memoria contextual, como haría MCP.
- **Azure AI Foundry**: Este agente refleja cómo MCP orquestaría datos para respuestas precisas.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Cambia el `query` a "Información sobre Azure AI Foundry".
- Añade un nuevo documento a la lista (e.g., "Los agentes de IA usan herramientas externas").
- Revisa `context_mcp_agent.log`.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración asegura que el agente funcione correctamente. Errores comunes incluyen herramientas mal definidas, modelos no desplegados o problemas con embeddings.

**Paso a Paso**:  

1. Verifica que `gpt-35-turbo` y `text-embedding-ada-002` están desplegados.
2. Confirma las credenciales y el endpoint.
3. Usa logging para depurar.

**Código para Validar Modelos** (reutilizamos del Capítulo 2):

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

- Ejecuta el código para listar modelos. Asegúrate de que los modelos necesarios están desplegados.
- Simula un error (e.g., herramienta inválida) y revisa los logs.

## Notas Adicionales

- **Azure AI Foundry**: Los agentes multi-canal y con manejo de contexto son la base para asistentes avanzados.
- **Costos**: Monitorea `response.usage.total_tokens` para optimizar gastos.
- **MCP (beta)**: La simulación prepara para implementaciones reales en el Capítulo 4.

## Práctica Final

1. Ejecuta `multi_tool_agent.py` y prueba con diferentes números o herramientas.
2. Usa `multi_channel_agent.py` con un nuevo comando de voz simulado.
3. Ejecuta `context_mcp_agent.py` y añade un nuevo documento o `query`.
4. Usa `validate_deployments.py` para confirmar modelos desplegados.
5. Investiga en docs.microsoft.com sobre `azure-mcp-server` y sus capacidades para multi-canal.
