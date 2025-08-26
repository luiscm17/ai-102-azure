# Capítulo 5: Introducción a Agentic AI

En este capítulo, introducimos los conceptos fundamentales de los agentes de IA (*agentic AI*), que son sistemas capaces de realizar tareas complejas mediante interacciones multi-turno, toma de decisiones autónomas y uso de herramientas externas. Exploraremos cómo los agentes mantienen contexto conversacional, integran herramientas (*tool integration*) y usan el protocolo MCP (Multi-Context Protocol) para gestionar múltiples fuentes de datos y conexiones externas. Usaremos el SDK `openai` (v1.101.0) para Azure OpenAI y `azure-ai-generative` (v1.0.0b11, beta) para configurar un agente básico, con autenticación segura vía `azure-identity` (v1.24.0). Este capítulo prepara el terreno para implementaciones avanzadas en los capítulos posteriores, como integración de RAG y herramientas personalizadas.

## Objetivos del Capítulo

- Comprender los conceptos de agentes de IA y sus características (multi-turno, tool integration).
- Introducir el protocolo MCP para gestión de contexto y conexiones externas.
- Configurar un agente básico con Azure OpenAI que usa *chat completions* y *tool calling*.
- Implementar logging para monitoreo y depuración.

## Conceptos Fundamentales

**Explicación**:  
Los agentes de IA son sistemas que combinan modelos generativos (e.g., GPT-4o, GPT-3.5-turbo) con capacidades de razonamiento, memoria contextual y acceso a herramientas externas para resolver tareas complejas. A diferencia de un simple chatbot, un agente puede planificar, recordar conversaciones previas y ejecutar acciones (e.g., consultar una API). Estas capacidades son esenciales para aplicaciones en Azure AI Foundry, como asistentes empresariales o automatización de procesos.

- **Agentes de IA**: Entidades que interactúan dinámicamente, toman decisiones basadas en contexto y ejecutan acciones. Ejemplo: Un agente que agenda reuniones consultando un calendario externo.
- **Interacciones Multi-Turno**: Conversaciones donde el agente mantiene el contexto de mensajes previos para respuestas coherentes.
- **Tool Integration**: Capacidad del agente para invocar funciones externas (e.g., cálculos, consultas a bases de datos) usando *tool calling*.
- **Multi-Context Protocol (MCP)**: Protocolo (en preview, gestionado por `azure-mcp-server` v0.1.0) que permite a los agentes coordinar múltiples fuentes de datos (e.g., Azure Search, APIs externas) y mantener contexto entre interacciones. MCP actúa como un orquestador para conectar el modelo con herramientas y datos externos.

**Ejemplo Conceptual**:  

- Sin agente: Prompt: "Agenda una reunión." Respuesta: "No tengo acceso a tu calendario."
- Con agente y MCP: Prompt: "Agenda una reunión para mañana." El agente usa MCP para consultar un calendario externo, confirmar disponibilidad y responder: "Reunión agendada para las 10 a.m."

**Práctica**: Escribe un prompt multi-turno para un agente que responde preguntas sobre Azure AI y luego sugiere una acción (e.g., "Busca documentación reciente").

## Configuración Básica de un Agente

**Explicación**:  
Configuraremos un agente básico usando Azure OpenAI con `openai` para mantener una conversación multi-turno y ejecutar una herramienta simple (e.g., obtener la fecha actual). Aunque `azure-ai-generative` (v1.0.0b11) y `azure-mcp-server` (v0.1.0) son paquetes en beta, usaremos `openai` para simular un agente, ya que MCP está en preview y su documentación es limitada al 25/08/2025.

**Paso a Paso**:  

1. Configura el cliente `openai` con autenticación segura.
2. Define una herramienta para una tarea simple.
3. Implementa una conversación multi-turno con *tool calling*.

**Código Práctico** (guarda como `basic_agent.py`):

```python
# basic_agent.py
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
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
credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-08-01-preview"
)

# Define herramienta

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Obtiene la fecha actual.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Función real

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# Conversación multi-turno con tool calling

try:
    logger.info("Iniciando conversación multi-turno con agente")
    messages = [
        {"role": "system", "content": "Eres un agente de IA que responde preguntas y usa herramientas."},
        {"role": "user", "content": "Dime qué es Azure AI."},
        {"role": "assistant", "content": "Azure AI es una plataforma de Microsoft para desarrollar soluciones de inteligencia artificial, como modelos generativos y agentes."},
        {"role": "user", "content": "Ahora dime la fecha actual."}
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
        result = get_current_date()
        logger.info(f"Resultado de la herramienta: {result}")
        messages.append({"role": "assistant", "content": f"La fecha actual es {result}."})
        print(f"Respuesta: La fecha actual es {result}.")
    else:
        text = response.choices[0].message.content
        logger.info(f"Respuesta generada: {text}")
        print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en agente: {e}")
```

**Explicación**:  

- `messages`: Mantiene el contexto de una conversación multi-turno.
- `tools`: Define una función simple (`get_current_date`) que el agente puede invocar.
- `tool_choice="auto"`: Permite al modelo decidir si usar la herramienta.
- **MCP (contexto)**: Este ejemplo no usa `azure-mcp-server` (en preview), pero simula un agente que coordina contexto y herramientas, similar a lo que MCP orquesta.

**Práctica**:  

- Ejecuta el script y revisa la respuesta. Añade un nuevo turno al `messages` (e.g., "user": "¿Qué hora es?").
- Crea una nueva herramienta (e.g., `get_current_time`) y modifícala para devolver la hora actual.
- Revisa `basic_agent.log` para confirmar la ejecución de la herramienta.

## Overview de Multi-Context Protocol (MCP)

**Explicación**:  
El Multi-Context Protocol (MCP), soportado por `azure-mcp-server` (v0.1.0, preview), es un protocolo para coordinar múltiples fuentes de datos y herramientas externas en agentes de IA. Permite a los agentes gestionar contexto (e.g., historial de conversación, datos de APIs) y conectar con servicios externos (e.g., Azure Search, bases de datos). Aunque MCP está en fase beta y su implementación completa se cubrirá en el Capítulo 4, aquí conceptualizamos su rol.

**Flujo de MCP**:  

1. **Context Management**: Almacena el historial de conversación y datos externos (e.g., en Redis o memoria).
2. **Tool Integration**: Conecta el modelo con APIs o servicios vía funciones definidas.
3. **External Connections**: Usa MCP para consultar datos de Azure Search, APIs REST, o bases de datos.

**Ejemplo Conceptual**:  

- Prompt: "Encuentra la disponibilidad de salas para mañana."  
- Con MCP: El agente usa MCP para consultar un calendario externo, mantiene el contexto y responde: "Sala A disponible a las 10 a.m."

**Código Conceptual** (sin ejecutar, para ilustrar MCP):

```python
# Pseudo-código para MCP
context = mcp_server.get_context(user_id="user123")  # Obtiene historial
external_data = mcp_server.query_external_api("calendar_api", {"date": "2025-08-26"})
prompt = f"Contexto: {context}\nDatos: {external_data}\nResponde al usuario."
response = client.chat.completions.create(model="gpt-35-turbo", messages=[{"role": "user", "content": prompt}])
```

**Práctica**:  

- Escribe un prompt multi-turno que simule el uso de MCP (e.g., "Consulta mi calendario y sugiere un horario").
- Investiga en docs.microsoft.com sobre `azure-mcp-server` y sus capacidades en preview.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración asegura que el agente funciona correctamente. Errores comunes incluyen modelos no desplegados, herramientas mal definidas o problemas de autenticación.

**Paso a Paso**:  

1. Verifica que `gpt-35-turbo` está desplegado.
2. Confirma el endpoint y clave en variables de entorno.
3. Usa logging para depurar.

**Código para Validar Modelos** (reutilizamos del Capítulo 4):

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
- Simula un error (e.g., herramienta mal definida) y revisa `basic_agent.log`.

## Notas Adicionales

- **Azure AI Foundry**: Los agentes *agentic* son la base para asistentes avanzados en Foundry, usando multi-turno y herramientas externas.
- **Costos**: Monitorea `response.usage.total_tokens` para optimizar gastos. Usa tiers bajos para pruebas.
- **Seguridad**: Almacena claves en Azure Key Vault (lo cubrimos en el Capítulo 4, Módulo 2).

## Práctica Final

1. Ejecuta `basic_agent.py` y añade un nuevo turno a la conversación.
2. Crea una nueva herramienta (e.g., `get_current_time`) y pruébala.
3. Escribe un prompt que simule el uso de MCP para consultar datos externos.
4. Usa `validate_deployments.py` para confirmar modelos desplegados.
5. Investiga en docs.microsoft.com sobre `azure-ai-generative` y sus funciones para agentes.
