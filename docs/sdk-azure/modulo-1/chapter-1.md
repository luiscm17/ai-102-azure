# Capítulo 1: Introducción a Modelos Generativos

En este **Capítulo 1**, exploraremos los fundamentos de los modelos generativos, como GPT y DALL-E, disponibles a través de Azure OpenAI. Nos enfocaremos exclusivamente en el uso del SDK de Python para interactuar con estos servicios, sin depender del portal de Azure o interfaces gráficas como Azure AI Foundry. Cubriremos conceptos esenciales, como prompts, tokens y Retrieval-Augmented Generation (RAG), que son fundamentales para entender cómo funcionan estas soluciones y cómo se integran en aplicaciones reales.

Usaremos el paquete `openai` (v1.101.0, configurado para Azure OpenAI) como SDK principal, junto con `azure-identity` (v1.24.0) para autenticación segura. Este capítulo es introductorio, por lo que nos enfocaremos en la teoría y en una configuración inicial simple para interactuar con un modelo generativo, preparando el terreno para capítulos posteriores donde profundizaremos en implementaciones avanzadas como RAG y fine-tuning.

## Objetivos del Capítulo

- Comprender los conceptos clave de modelos generativos (prompts, tokens, embeddings).
- Introducir Retrieval-Augmented Generation (RAG) como técnica para mejorar respuestas.
- Configurar el entorno para interactuar con Azure OpenAI vía SDK.
- Realizar una llamada básica a un modelo generativo para generar texto.

## Conceptos Fundamentales de Modelos Generativos

**Explicación**:  
Los modelos generativos, como los ofrecidos por Azure OpenAI (e.g., GPT-4, DALL-E), son modelos de inteligencia artificial capaces de generar contenido como texto, imágenes o incluso código, basándose en datos de entrenamiento masivos. En Azure AI-102, nos enfocamos principalmente en modelos de texto como GPT, que generan respuestas naturales a partir de prompts (instrucciones de entrada). Estos modelos son clave para aplicaciones como chatbots, generación de contenido o análisis avanzado.

- **Prompts**: Instrucciones en lenguaje natural que das al modelo (e.g., "Escribe un poema sobre la luna"). El diseño del prompt afecta la calidad de la respuesta.
- **Tokens**: Unidades de texto (palabras, caracteres o fragmentos) que el modelo procesa. Por ejemplo, "Hola mundo" puede ser ~2-3 tokens. Azure OpenAI tiene límites de tokens por solicitud (e.g., 4096 para algunos modelos).
- **Embeddings**: Representaciones numéricas de texto que capturan su significado, usadas para tareas como búsqueda semántica.
- **Retrieval-Augmented Generation (RAG)**: Técnica que combina generación de texto con búsqueda de información externa (e.g., documentos en Azure Search) para respuestas más precisas y contextuales. RAG es clave en AI-102 para aplicaciones avanzadas, como chatbots que consultan bases de conocimiento.

Azure OpenAI se diferencia de OpenAI estándar porque se despliega en la infraestructura de Azure, con endpoints específicos y autenticación vía Azure AD o claves API. Usaremos el SDK `openai` configurado para Azure, lo que permite integrarlo con otros servicios Azure AI (e.g., Cognitive Services) y simular funcionalidades de Azure AI Foundry (como agents generativos) sin UI.

**Práctica**:  
Piensa en un caso de uso real (e.g., un asistente de soporte que responde preguntas usando RAG). Escribe un prompt simple para probar más adelante.

## Configuración del Entorno para Azure OpenAI

**Explicación**:  
Para interactuar con Azure OpenAI, necesitas un recurso desplegado (como hicimos en el Módulo 0 con Text Analytics, pero ahora para OpenAI). Usaremos `openai` para enviar solicitudes al modelo, autenticándonos con `azure-identity` o una clave API. Este paso configura el entorno para una llamada básica, que validará nuestra conexión al servicio.

**Paso a Paso**:  

1. Asegúrate de tener un recurso Azure OpenAI desplegado (si no, lo creamos vía SDK).
2. Instala el paquete `openai`.
3. Configura credenciales y endpoint para conectar al modelo.

**Código Práctico** (guarda como `setup_openai.py`):  
Primero, instala el paquete:

```bash
pip install openai==1.101.0 azure-identity==1.24.0
```

Crea un recurso Azure OpenAI (si no lo tienes del Capítulo 2, Módulo 0):

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os

# Configura credenciales
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "myopenai001"  # Nombre único
location = "eastus"
sku_name = "S0"

# Crea cliente
client = CognitiveServicesManagementClient(credential, subscription_id)

# Crea recurso OpenAI
try:
    parameters = {
        "kind": "OpenAI",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    print(f"Recurso creado: {result.name}, Tipo: {result.kind}")

    # Obtén endpoint y clave
    endpoint = result.properties.endpoint
    keys = client.accounts.list_keys(resource_group, account_name)
    api_key = keys.key1
    print(f"Endpoint: {endpoint}, Clave: {api_key[:4]}...")
except Exception as e:
    print(f"Error: {e}")
```

**Explicación**:  

- `kind: "OpenAI"`: Especifica un recurso Azure OpenAI.
- `endpoint` y `api_key`: Necesarios para conectar al modelo. Guárdalos en variables de entorno para seguridad.

**Práctica**:  

- Ejecuta el código para crear el recurso (cambia `account_name` si ya existe).
- Verifica en el portal (solo para validar) que el recurso aparece. Luego, no uses el portal nuevamente.

## Llamada Básica a un Modelo Generativo

**Explicación**:  
Haremos una llamada simple a un modelo de Azure OpenAI (e.g., GPT-3.5-turbo o GPT-4, según disponibilidad en tu recurso) para generar texto. Esto introduce cómo estructurar prompts y manejar respuestas. Usaremos `openai` configurado para Azure, con autenticación vía clave API (o `azure-identity` en capítulos posteriores para escenarios avanzados).

**Paso a Paso**:  

1. Configura el cliente `openai` con el endpoint y clave del recurso.
2. Envía un prompt simple para generar texto.
3. Analiza la respuesta y maneja errores.

**Código Práctico** (guarda como `basic_openai_call.py`):

```python
from openai import AzureOpenAI
import os

# Configura cliente
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "https://myopenai001.openai.azure.com/")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"  # Cambia según el modelo desplegado en tu recurso

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-08-01-preview"  # Versión estable al 25/08/2025
)

# Llamada al modelo
try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Escribe un poema corto sobre la luna."}
        ],
        max_tokens=100,
        temperature=0.7
    )
    print("Respuesta del modelo:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
```

**Explicación**:  

- `AzureOpenAI`: Cliente configurado para Azure, no OpenAI estándar. Usa `azure_endpoint` y `api_version` específicos.
- `messages`: Formato de chat con roles (`system` para instrucciones, `user` para el prompt).
- `max_tokens`: Limita la longitud de la respuesta (evita costos innecesarios).
- `temperature`: Controla la creatividad (0.7 es equilibrado).
- **Seguridad**: Almacena `endpoint` y `api_key` en variables de entorno (`export AZURE_OPENAI_ENDPOINT=...`).

**Práctica**:  

- Configura las variables de entorno con el endpoint y clave del recurso creado.
- Ejecuta el código y verifica que genera un poema. Cambia el prompt a algo como "Explica qué es RAG en 50 palabras".
- Ajusta `max_tokens` a 50 y `temperature` a 0.3. Observa cómo cambia la respuesta.

## Introducción a Retrieval-Augmented Generation (RAG)

**Explicación**:  
RAG combina generación de texto con búsqueda de información externa (e.g., documentos en Azure Search) para mejorar la precisión y contexto de las respuestas. Por ejemplo, un chatbot puede buscar en una base de conocimiento antes de responder. En AI-102, RAG es relevante para aplicaciones generativas avanzadas. Aunque lo implementaremos en detalle en el Capítulo 4, aquí introducimos el concepto:

- **Retrieval**: Busca información relevante (e.g., vía `azure-search-documents`).
- **Augmentation**: Agrega el contexto recuperado al prompt.
- **Generation**: El modelo genera una respuesta basada en el contexto.

**Ejemplo Conceptual**:  
Prompt sin RAG: "Explica la teoría de la relatividad."  
Prompt con RAG: "Usa este documento [texto de Einstein] para explicar la relatividad."

**Práctica**:  
Escribe un prompt que combine un documento ficticio (e.g., "La luna es un satélite natural...") con una pregunta ("¿Por qué brilla la luna?"). Esto te prepara para el código de RAG en capítulos posteriores.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración y la llamada al modelo asegura que estás listo para escenarios más complejos. Errores comunes incluyen endpoints incorrectos, modelos no desplegados o límites de tokens excedidos.

**Paso a Paso**:  

1. Verifica que el recurso OpenAI está activo (usa `client.accounts.get` del Módulo 0).
2. Confirma que el modelo (e.g., `gpt-35-turbo`) está desplegado en tu recurso (puedes listar modelos con `client.deployments.list()` en el SDK de gestión).
3. Usa logging para rastrear errores.

**Código para Logging** (agrega a `basic_openai_call.py`):

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    logger.info(f"Conectando a {endpoint} con modelo {model}")
    response = client.chat.completions.create(...)
    logger.info("Respuesta recibida exitosamente")
    print(response.choices[0].message.content)
except Exception as e:
    logger.error(f"Error en la llamada: {e}")
```

**Práctica**:  

- Añade logging al código y registra cada paso (e.g., "Iniciando cliente", "Enviando prompt").
- Simula un error (e.g., usa un endpoint inválido) y revisa el log.

## Notas Adicionales

- **Azure AI Foundry**: Los modelos generativos son la base para agents en Foundry. Este código simula cómo un agent usaría Azure OpenAI para generar respuestas.
- **Costos**: Monitorea el uso de tokens en Azure OpenAI para evitar cargos. Usa `response.usage` para ver tokens consumidos.
- **Seguridad**: Nunca hardcodees `api_key`. Usa Azure Key Vault en producción (lo cubriremos en módulos avanzados).

## Práctica Final

1. Ejecuta `setup_openai.py` para crear un recurso Azure OpenAI (si no lo tienes).
2. Ejecuta `basic_openai_call.py` y genera un poema. Modifica el prompt a algo creativo (e.g., "Escribe un correo formal invitando a un evento").
3. Ajusta parámetros (`max_tokens`, `temperature`) y observa diferencias en las respuestas.
4. Escribe un prompt que simule RAG (e.g., "Basado en [texto ficticio], responde...") y guárdalo para el Capítulo 4.
5. Investiga en docs.microsoft.com qué modelos están disponibles en Azure OpenAI (e.g., GPT-4o) y verifica si están desplegados en tu recurso.
