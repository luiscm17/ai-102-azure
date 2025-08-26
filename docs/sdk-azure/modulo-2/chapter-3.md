# Capítulo 3: Uso Intermedio

En este capítulo, exploramos técnicas intermedias para interactuar con Azure OpenAI, enfocándonos en *chat completions* para conversaciones multi-turno, *tool calling* para ejecutar funciones externas, y los fundamentos de Retrieval-Augmented Generation (RAG) con un enfoque de retrieval simple. Usaremos el SDK `openai` (v1.101.0) configurado para Azure, con autenticación vía `azure-identity` (v1.24.0). Los ejemplos prácticos simulan escenarios reales, como un chatbot que mantiene contexto conversacional o un agente que usa herramientas externas, alineados con las capacidades de Azure AI Foundry. Todo se implementará mediante código, con logging para rastrear operaciones y depurar errores.

## Objetivos del Capítulo

- Implementar *chat completions* para conversaciones multi-turno.
- Usar *tool calling* para integrar funciones externas con Azure OpenAI.
- Introducir RAG con un ejemplo de retrieval simple en memoria.
- Monitorear y depurar con logging robusto.

## Chat Completions para Conversaciones Multi-Turno

**Explicación**:  
Las *chat completions* permiten mantener conversaciones multi-turno, donde el modelo recuerda el contexto de mensajes previos. Esto es ideal para chatbots o asistentes en Azure AI Foundry, que necesitan responder coherentemente en diálogos extendidos. Usaremos `client.chat.completions.create` con una lista de mensajes que incluye roles (`system`, `user`, `assistant`) para simular una conversación.

**Paso a Paso**:  

1. Configura el cliente Azure OpenAI.
2. Crea una conversación multi-turno con mensajes concatenados.
3. Analiza la respuesta y tokens usados.

**Código Práctico** (guarda como `chat_completion.py`):

```python
# chat_completion.py
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("chat_completion.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Conversación multi-turno

try:
    logger.info("Iniciando conversación multi-turno")
    messages = [
        {"role": "system", "content": "Eres un asistente de soporte técnico para Azure AI."},
        {"role": "user", "content": "¿Qué es Azure OpenAI?"},
        {"role": "assistant", "content": "Azure OpenAI es un servicio que ofrece modelos de IA generativa, como GPT, para aplicaciones empresariales."},
        {"role": "user", "content": "Dime más sobre sus usos en chatbots."}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    text = response.choices[0].message.content
    logger.info(f"Respuesta generada. Tokens usados: {response.usage.total_tokens}")
    print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en chat completion: {e}")
```

**Explicación**:  

- `messages`: Lista que incluye el historial de la conversación (`system`, `user`, `assistant`) para mantener contexto.
- `temperature`: 0.7 para respuestas equilibradas.
- `response.usage`: Muestra tokens consumidos, útil para monitorear costos.
- **Azure AI Foundry**: Este código simula un agente conversacional que responde basándose en el contexto previo.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Añade un tercer turno al `messages` (e.g., "user": "¿Cómo se integra con Azure Search?").
- Ajusta `max_tokens` a 100 y `temperature` a 0.5. Observa cómo cambia la respuesta.
- Revisa `chat_completion.log` para confirmar tokens usados.

## Tool Calling

**Explicación**:  
*Tool calling* permite al modelo invocar funciones externas (e.g., cálculos, consultas a APIs) basándose en el prompt. En Azure OpenAI, definimos herramientas (funciones) que el modelo puede "llamar" para resolver tareas. Esto es clave para agentes en Azure AI Foundry que necesitan interactuar con sistemas externos. Usaremos un ejemplo simple donde el modelo decide llamar una función para calcular el área de un círculo.

**Paso a Paso**:  

1. Define una herramienta (función) en el formato esperado por Azure OpenAI.
2. Configura una llamada con `tools` y `tool_choice`.
3. Procesa la respuesta para ejecutar la función.

**Código Práctico** (guarda como `tool_calling.py`):

```python
# tool_calling.py
from openai import AzureOpenAI
import os
import logging
import json
import math

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("tool_calling.log"), logging.StreamHandler()]
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
            "name": "calculate_circle_area",
            "description": "Calcula el área de un círculo dado su radio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "radius": {"type": "number", "description": "Radio del círculo"}
                },
                "required": ["radius"]
            }
        }
    }
]

# Función real

def calculate_circle_area(radius):
    return math.pi * radius ** 2

# Llamada con tool calling

try:
    logger.info("Enviando prompt con tool calling")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente que puede usar herramientas."},
            {"role": "user", "content": "Calcula el área de un círculo con radio 5."}
        ],
        tools=tools,
        tool_choice="auto",
        max_tokens=100
    )
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        logger.info(f"Tool call detectado: {tool_call.function.name}")
        arguments = json.loads(tool_call.function.arguments)
        result = calculate_circle_area(arguments["radius"])
        logger.info(f"Resultado: {result}")
        print(f"Área del círculo: {result:.2f}")
    else:
        logger.info("No se requirió tool call")
        print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    logger.error(f"Error en tool calling: {e}")
```

**Explicación**:  

- `tools`: Define una función (`calculate_circle_area`) con su esquema JSON.
- `tool_choice="auto"`: Permite al modelo decidir si usa la herramienta.
- `tool_calls`: Si el modelo solicita una función, ejecutamos `calculate_circle_area` con los parámetros proporcionados.
- **Azure AI Foundry**: Simula un agente que usa herramientas externas (e.g., APIs) para responder.

**Práctica**:  

- Ejecuta el script y revisa el cálculo del área. Cambia el radio a 10 en el prompt.
- Añade una nueva herramienta (e.g., `calculate_square_area`) y modifícala para calcular el área de un cuadrado.
- Revisa `tool_calling.log` para confirmar la ejecución de la función.

## Introducción a RAG (Retrieval Simple)

**Explicación**:  
Retrieval-Augmented Generation (RAG) combina búsqueda de información externa con generación de texto para respuestas más precisas. En este capítulo, implementamos un RAG simple en memoria (sin `azure-search-documents`, que usaremos en el Capítulo 4). Simularemos una base de documentos, buscaremos el más relevante usando embeddings y lo incluiremos en el prompt.

**Paso a Paso**:  

1. Genera embeddings para una lista de documentos.
2. Compara el embedding del prompt con los documentos para encontrar el más relevante.
3. Usa el documento en una *chat completion*.

**Código Práctico** (guarda como `simple_rag.py`):

```python
# simple_rag.py
from openai import AzureOpenAI
import os
import logging
import numpy as np

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("simple_rag.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
embedding_model = "text-embedding-ada-002"
chat_model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Documentos simulados

documents = [
    "Azure OpenAI ofrece modelos generativos para texto e imágenes.",
    "RAG combina búsqueda y generación para respuestas precisas.",
    "Azure AI Foundry soporta agentes generativos avanzados."
]

# Generar embeddings para documentos

def get_embedding(text):
    response = client.embeddings.create(model=embedding_model, input=text)
    return response.data[0].embedding

try:
    logger.info("Generando embeddings para documentos")
    doc_embeddings = [get_embedding(doc) for doc in documents]

    # Prompt del usuario
    query = "Explica cómo funciona RAG."
    query_embedding = get_embedding(query)

    # Buscar documento más relevante (similitud coseno)
    similarities = [np.dot(query_embedding, doc_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)) for doc_emb in doc_embeddings]
    best_doc_idx = np.argmax(similarities)
    best_doc = documents[best_doc_idx]
    logger.info(f"Documento más relevante: {best_doc}")

    # Generar respuesta con RAG
    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "Eres un asistente que usa documentos para responder."},
            {"role": "user", "content": f"Usa este contexto: {best_doc}\n{query}"}
        ],
        max_tokens=150,
        temperature=0.7
    )
    text = response.choices[0].message.content
    logger.info(f"Respuesta generada. Tokens usados: {response.usage.total_tokens}")
    print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en RAG: {e}")
```

**Explicación**:  

- `get_embedding`: Genera embeddings para documentos y el prompt.
- **Similitud coseno**: Encuentra el documento más relevante comparando embeddings.
- **RAG**: Incluye el documento relevante en el prompt para una respuesta contextual.
- **Limitación**: Usa documentos en memoria; en el Capítulo 4 integraremos `azure-search-documents`.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Cambia el prompt a "Describe Azure AI Foundry".
- Añade un nuevo documento a la lista (e.g., "Los embeddings son vectores para búsqueda semántica").
- Revisa `simple_rag.log` para confirmar el documento seleccionado.

## Validación y Solución de Problemas

**Explicación**:  
Validar las configuraciones y llamadas asegura que el entorno está listo. Errores comunes incluyen modelos no desplegados, límites de tokens excedidos o problemas con embeddings.

**Paso a Paso**:  

1. Verifica que `gpt-35-turbo` y `text-embedding-ada-002` están desplegados.
2. Confirma el endpoint y clave en variables de entorno.
3. Usa logging para depurar.

**Código para Validar Modelos** (guarda como `validate_deployments.py`):

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

- Ejecuta el código para listar modelos. Asegúrate de que `gpt-35-turbo` y `text-embedding-ada-002` están disponibles.
- Simula un error (e.g., modelo no desplegado) y revisa `validate_deployments.log`.

## Notas Adicionales

- **Azure AI Foundry**: Chat completions y tool calling son fundamentales para agentes que mantienen conversaciones y usan herramientas externas.
- **Costos**: Monitorea `response.usage.total_tokens` para optimizar gastos. Usa tiers bajos para pruebas.
- **Seguridad**: Almacena claves en Azure Key Vault (lo cubriremos en el Capítulo 4).

## Práctica Final

1. Ejecuta `chat_completion.py` y añade un turno más a la conversación.
2. Usa `tool_calling.py` para calcular el área con un radio diferente. Añade una herramienta para otra operación (e.g., área de un cuadrado).
3. Ejecuta `simple_rag.py` y prueba con un nuevo prompt y documento adicional.
4. Usa `validate_deployments.py` para confirmar modelos desplegados.
5. Investiga en docs.microsoft.com otros parámetros de `tools` (e.g., `parallel_tool_calls`).
