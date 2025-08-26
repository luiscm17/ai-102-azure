# Capítulo 1: Introducción a Modelos Generativos

En este capítulo, introducimos los fundamentos de los modelos generativos, un pilar clave para la certificación AI-102. Nos enfocamos en conceptos esenciales como GPT, DALL-E, prompts, y Retrieval-Augmented Generation (RAG), todos aplicados a través de Azure OpenAI usando el SDK de Python `openai` (v1.101.0). Este capítulo establece las bases teóricas y prácticas para trabajar con soluciones generativas, como chatbots o generadores de contenido, sin depender de interfaces gráficas como el portal de Azure o Azure AI Foundry. Todo se hará mediante código, con autenticación segura vía `azure-identity` (v1.24.0). También proporcionaremos un ejemplo básico de interacción con Azure OpenAI para ilustrar los conceptos.

## Objetivos del Capítulo

- Comprender los fundamentos de modelos generativos (GPT, DALL-E).
- Aprender a diseñar prompts efectivos.
- Introducir Retrieval-Augmented Generation (RAG) como técnica clave.
- Realizar una interacción básica con Azure OpenAI vía SDK.

## Conceptos Fundamentales

**Explicación**:  
Los modelos generativos son sistemas de inteligencia artificial capaces de crear contenido nuevo, como texto (GPT) o imágenes (DALL-E), basados en patrones aprendidos de datos masivos. En Azure AI-102, nos centramos en Azure OpenAI, que ofrece modelos como GPT-3.5-turbo, GPT-4, y DALL-E, optimizados para entornos empresariales con autenticación Azure AD y escalabilidad.

- **GPT (Generative Pre-trained Transformer)**: Modelos de lenguaje para tareas de texto, como generación de respuestas, resúmenes o traducción. Ejemplo: GPT-3.5-turbo genera texto conversacional.
- **DALL-E**: Modelo para generar imágenes a partir de prompts de texto. Útil para aplicaciones creativas (aunque en AI-102 nos enfocamos más en texto).
- **Prompts**: Instrucciones en lenguaje natural que guían al modelo. Un buen prompt es claro y específico (e.g., "Escribe un resumen de 50 palabras sobre IA").
- **Tokens**: Unidades de texto procesadas por el modelo (palabras, signos, etc.). Los modelos tienen límites (e.g., 4096 tokens para GPT-3.5-turbo).
- **Retrieval-Augmented Generation (RAG)**: Técnica que combina búsqueda de información externa (e.g., en Azure Search) con generación de texto para respuestas más precisas. Ejemplo: Un chatbot consulta documentos antes de responder. RAG es clave para aplicaciones avanzadas en AI-102 y lo exploraremos en detalle en el Capítulo 4.

**Ejemplo Conceptual**:  

- Sin RAG: Prompt: "Explica la relatividad." Respuesta: Basada solo en el conocimiento del modelo, puede ser genérica.
- Con RAG: Prompt: "Explica la relatividad usando [documento de Einstein]." Respuesta: Más precisa, basada en el documento.

**Práctica**: Escribe un prompt para generar un correo formal invitando a un evento. Luego, reescríbelo como si usara RAG (e.g., "Usa [agenda del evento] para escribir un correo formal").

## Configuración Básica de Azure OpenAI

**Explicación**:  
Para interactuar con Azure OpenAI, necesitamos un recurso desplegado (como en el Módulo 0, Capítulo 2). Configuraremos el cliente `openai` para Azure, usando una clave API para simplicidad (aunque en producción preferimos `azure-identity`). Esto simula cómo un agente en Azure AI Foundry usaría modelos generativos.

**Paso a Paso**:  

1. Asegúrate de tener un recurso Azure OpenAI (puedes crearlo con el código del Módulo 0).
2. Instala `openai` y `azure-identity`.
3. Configura el cliente con el endpoint y clave.

**Código Práctico** (instalación en terminal):

```bash
pip install openai==1.101.0 azure-identity==1.24.0
```

**Código para Crear Recurso (si no lo tienes)**:

```python
# crear_openai_resource.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("openai_resource.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "tu-subscription-id")
resource_group = "my-resource-group"
account_name = "myopenai002"  # Nombre único
location = "eastus"
sku_name = "S0"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Crea recurso OpenAI

try:
    logger.info(f"Creando recurso {account_name}")
    parameters = {
        "kind": "OpenAI",
        "sku": {"name": sku_name},
        "location": location,
        "properties": {}
    }
    poller = client.accounts.begin_create(resource_group, account_name, parameters)
    result = poller.result()
    logger.info(f"Recurso creado: {result.name}, Tipo: {result.kind}")

    # Obtén endpoint y clave
    endpoint = result.properties.endpoint
    keys = client.accounts.list_keys(resource_group, account_name)
    api_key = keys.key1
    logger.info(f"Endpoint: {endpoint}, Clave: {api_key[:4]}...")
except Exception as e:
    logger.error(f"Error al crear recurso: {e}")
```

**Explicación**:  

- `kind: "OpenAI"`: Crea un recurso para Azure OpenAI.
- `endpoint` y `api_key`: Necesarios para interactuar con el modelo. Guárdalos en variables de entorno.
- **Logging**: Registra el proceso en `openai_resource.log`.

**Práctica**:  

- Ejecuta el código con un `account_name` único. Verifica el recurso en el portal (solo para validar, luego usa solo código).
- Guarda `endpoint` y `api_key` en variables de entorno:

  ```bash
  export AZURE_OPENAI_ENDPOINT="https://myopenai002.openai.azure.com/"
  export AZURE_OPENAI_API_KEY="tu-api-key"
  ```

## Llamada Básica a Modelo Generativo

**Explicación**:  
Haremos una llamada simple a un modelo de Azure OpenAI (e.g., GPT-3.5-turbo) para ilustrar cómo funcionan los prompts y las respuestas. Esto introduce cómo interactúan los modelos generativos con inputs de texto, preparando el terreno para RAG y tool calling en capítulos posteriores.

**Paso a Paso**:  

1. Configura el cliente `openai` con endpoint y clave.
2. Envía un prompt para generar texto.
3. Analiza la respuesta y tokens usados.

**Código Práctico** (guarda como `basic_generative_call.py`):

```python
# basic_generative_call.py
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("generative_call.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"  # Verifica que esté desplegado
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-08-01-preview"
)

# Llamada al modelo

try:
    logger.info("Enviando prompt al modelo")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente creativo y conciso."},
            {"role": "user", "content": "Escribe un haiku sobre la inteligencia artificial."}
        ],
        max_tokens=50,
        temperature=0.7
    )
    text = response.choices[0].message.content
    logger.info(f"Respuesta generada. Tokens usados: {response.usage.total_tokens}")
    print(f"Haiku: {text}")
except Exception as e:
    logger.error(f"Error en la llamada: {e}")
```

**Explicación**:  

- `AzureOpenAI`: Cliente configurado para Azure OpenAI, usando endpoint y API version específicos.
- `messages`: Formato de chat con roles `system` (instrucciones generales) y `user` (prompt).
- `max_tokens` y `temperature`: Controlan la longitud y creatividad de la respuesta.
- **RAG (contexto)**: Este ejemplo es sin RAG; en el Capítulo 4, añadiremos búsqueda externa.

**Práctica**:  

- Ejecuta el código y revisa el haiku generado. Cambia el prompt a "Escribe un resumen de 30 palabras sobre Azure OpenAI".
- Ajusta `temperature` a 0.3 y `max_tokens` a 30. Observa cómo cambia la respuesta.
- Revisa `generative_call.log` para confirmar tokens usados.

## Overview de Retrieval-Augmented Generation (RAG)

**Explicación**:  
RAG combina la generación de texto con la búsqueda de información externa (e.g., documentos en Azure Search) para mejorar la precisión y relevancia de las respuestas. Es una técnica clave en AI-102 para aplicaciones como chatbots empresariales o agentes en Azure AI Foundry. Aunque implementaremos RAG completo en el Capítulo 4, aquí conceptualizamos su flujo:

1. **Retrieval**: Busca documentos relevantes usando embeddings o palabras clave.
2. **Augmentation**: Añade el contexto recuperado al prompt.
3. **Generation**: El modelo genera una respuesta basada en el contexto.

**Ejemplo Conceptual**:  

- Prompt sin RAG: "Explica qué es Azure OpenAI."  
  Respuesta: General, basada solo en el modelo.
- Prompt con RAG: "Explica Azure OpenAI usando [documentación oficial de Microsoft]."  
  Respuesta: Más precisa, basada en el documento.

**Código Conceptual** (sin ejecutar, para ilustrar RAG):

```python
# Pseudo-código para RAG
context = search_documents("Azure OpenAI")  # Busca en Azure Search
prompt = f"Usa este contexto: {context}\nExplica Azure OpenAI."
response = client.chat.completions.create(model="gpt-35-turbo", messages=[{"role": "user", "content": prompt}])
```

**Práctica**:  

- Escribe un prompt que simule RAG (e.g., "Usa [texto sobre IA] para explicar la IA generativa").
- Investiga en docs.microsoft.com qué modelos de Azure OpenAI soportan embeddings para RAG (e.g., `text-embedding-ada-002`).

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración y la llamada asegura que el entorno está listo. Errores comunes incluyen modelos no desplegados, claves inválidas o límites de tokens excedidos.

**Paso a Paso**:  

1. Verifica que el recurso OpenAI está activo (usa `client.accounts.get` del Módulo 0).
2. Confirma que `gpt-35-turbo` está desplegado (puedes listar modelos con el SDK de gestión).
3. Usa logging para depurar.

**Código para Validar Modelos**:

```python
# validate_models.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("validate_models.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura credenciales

credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
resource_group = "my-resource-group"
account_name = "myopenai002"

# Crea cliente

client = CognitiveServicesManagementClient(credential, subscription_id)

# Lista modelos desplegados

try:
    deployments = client.deployments.list(resource_group, account_name)
    logger.info("Modelos desplegados:")
    for deployment in deployments:
        logger.info(f"- {deployment.name}")
except Exception as e:
    logger.error(f"Error al listar modelos: {e}")
```

**Práctica**:  

- Ejecuta el código para listar modelos. Asegúrate de que `gpt-35-turbo` está disponible.
- Simula un error (e.g., usa un endpoint inválido) y revisa `generative_call.log`.

## Notas Adicionales

- **Azure AI Foundry**: Los modelos generativos son la base para agentes en Foundry, que usan prompts para tareas como soporte al cliente.
- **Costos**: Monitorea `response.usage.total_tokens` para evitar gastos. Usa recursos de prueba con tiers bajos.
- **Seguridad**: Almacena claves en variables de entorno o Azure Key Vault (lo cubriremos en el Capítulo 4).

## Práctica Final

1. Ejecuta `create_openai_resource.py` para crear un recurso Azure OpenAI (si no lo tienes).
2. Usa `basic_generative_call.py` para generar un haiku. Modifica el prompt a algo creativo (e.g., "Escribe un eslogan para Azure AI").
3. Revisa `generative_call.log` para confirmar tokens usados.
4. Ejecuta `validate_models.py` para listar modelos desplegados.
5. Escribe un prompt que simule RAG (e.g., "Usa [documento ficticio] para responder...") y guárdalo para el Capítulo 4.
