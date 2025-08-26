# Capítulo 2: Setup y Llamadas Básicas

En este capítulo, configuramos el entorno para interactuar con Azure OpenAI usando el SDK `openai` (v1.101.0) y realizamos llamadas básicas para generar texto (*completions*) y vectores semánticos (*embeddings*). Nos enfocamos en aplicaciones prácticas para la certificación AI-102, como chatbots o análisis semántico, simulando escenarios de Azure AI Foundry donde agentes generativos procesan datos. Todo se hará mediante código, usando autenticación segura con `azure-identity` (v1.24.0) y logging robusto para rastrear operaciones. Este capítulo extiende el ejemplo básico del Capítulo 1, introduciendo parámetros avanzados y manejo de errores.

## Objetivos del Capítulo

- Configurar el cliente `openai` para Azure OpenAI con autenticación segura.
- Realizar llamadas de *completions* para generar texto con parámetros personalizados.
- Generar *embeddings* para tareas semánticas.
- Implementar logging para monitoreo y depuración.

## Configuración del Cliente Azure OpenAI

**Explicación**:  
Para interactuar con Azure OpenAI, necesitamos un cliente configurado con el endpoint y credenciales de un recurso Azure OpenAI (creado en el Capítulo 1 o Módulo 0). Usaremos `AzureOpenAI` con una clave API para simplicidad, aunque también mostraremos cómo usar `DefaultAzureCredential` para autenticación Azure AD, ideal para entornos seguros como CI/CD o Azure AI Foundry. Este paso valida la conexión y prepara el entorno para llamadas posteriores.

**Paso a Paso**:  

1. Configura variables de entorno para el endpoint y la clave API.
2. Inicializa el cliente `AzureOpenAI` con opción para autenticación Azure AD.
3. Prueba la conexión con una llamada simple.

**Código Práctico** (guarda como `setup_openai_client.py`):

```python
# setup_openai_client.py
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("openai_setup.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura credenciales

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
api_version = "2024-08-01-preview"
model = "gpt-35-turbo"  # Verifica que esté desplegado

# Intenta autenticación con Azure AD, fallback a API key

try:
    credential = DefaultAzureCredential()
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=credential.get_token("<https://cognitiveservices.azure.com/.default>"),
        api_version=api_version
    )
    logger.info("Cliente configurado con Azure AD")
except Exception as e:
    logger.warning(f"Azure AD falló, usando API key: {e}")
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    logger.info("Cliente configurado con API key")

# Prueba de conexión

try:
    logger.info(f"Probando conexión con {model}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Confirma conexión a Azure OpenAI."}
        ],
        max_tokens=50
    )
    logger.info("Conexión exitosa")
    print(f"Respuesta: {response.choices[0].message.content}")
except Exception as e:
    logger.error(f"Error en prueba de conexión: {e}")
```

**Explicación**:  

- `AzureOpenAI`: Cliente para Azure OpenAI, configurado con `azure_endpoint` y `api_version`.
- `azure_ad_token_provider`: Usa `DefaultAzureCredential` para autenticación Azure AD, con fallback a `api_key` si falla.
- `max_tokens`: Limita la respuesta para optimizar costos.
- **Logging**: Registra cada paso en `openai_setup.log` y consola.

**Práctica**:  

- Configura `AZURE_OPENAI_ENDPOINT` y `AZURE_OPENAI_API_KEY` en variables de entorno (obtén desde el recurso creado en el Capítulo 1).
- Ejecuta el script y verifica la respuesta. Cambia el prompt a "Describe Azure AI en 20 palabras".
- Revisa `openai_setup.log`. Intenta forzar un error (e.g., endpoint inválido) y depura.

## Llamadas de Completions

**Explicación**:  
Las *completions* generan texto a partir de prompts, como respuestas de chat, resúmenes o contenido creativo. Usaremos `client.chat.completions.create` con parámetros avanzados (`temperature`, `top_p`, `max_tokens`) para controlar la creatividad y longitud. Esto simula cómo un agente en Azure AI Foundry generaría respuestas para usuarios.

**Paso a Paso**:  

1. Configura una llamada de *completion* con un prompt estructurado.
2. Ajusta parámetros para personalizar la respuesta.
3. Analiza el uso de tokens.

**Código Práctico** (guarda como `basic_completion.py`):

```python
# basic_completion.py
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("completion.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "gpt-35-turbo"
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Llamada de completion

try:
    logger.info("Enviando prompt para completion")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente técnico."},
            {"role": "user", "content": "Explica en 100 palabras qué es Azure OpenAI y sus usos."}
        ],
        max_tokens=150,
        temperature=0.6,
        top_p=0.9
    )
    text = response.choices[0].message.content
    logger.info(f"Completion generada. Tokens usados: {response.usage.total_tokens}")
    print(f"Respuesta: {text}")
except Exception as e:
    logger.error(f"Error en completion: {e}")
```

**Explicación**:  

- `messages`: Estructura de chat con `system` (rol del modelo) y `user` (prompt).
- `temperature` (0.6): Equilibra creatividad y precisión.
- `top_p` (0.9): Controla la diversidad de palabras (probabilidad acumulativa).
- `response.usage`: Muestra tokens consumidos, clave para monitorear costos.

**Práctica**:  

- Ejecuta el script y revisa la explicación generada. Cambia el prompt a "Escribe un correo formal invitando a un evento de IA".
- Ajusta `temperature` a 0.9 y `max_tokens` a 100. Observa cómo cambia la respuesta.
- Revisa `completion.log` para confirmar tokens usados.

## Generación de Embeddings

**Explicación**:  
Los *embeddings* son vectores numéricos que representan el significado de un texto, ideales para búsqueda semántica, clasificación o RAG (que veremos en el Capítulo 4). Usaremos `client.embeddings.create` con un modelo como `text-embedding-ada-002` (si está desplegado) para generar vectores.

**Paso a Paso**:  

1. Configura el cliente para embeddings.
2. Genera un embedding para un texto.
3. Valida el vector resultante.

**Código Práctico** (guarda como `basic_embedding.py`):

```python
# basic_embedding.py
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("embedding.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
model = "text-embedding-ada-002"  # Verifica que esté desplegado
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Generar embedding

try:
    logger.info("Generando embedding")
    response = client.embeddings.create(
        model=model,
        input="Azure OpenAI impulsa soluciones generativas avanzadas."
    )
    embedding = response.data[0].embedding
    logger.info(f"Embedding generado. Longitud: {len(embedding)}")
    print(f"Primeros 5 valores: {embedding[:5]}")
except Exception as e:
    logger.error(f"Error en embedding: {e}")
```

**Explicación**:  

- `text-embedding-ada-002`: Modelo de embeddings (longitud ~1536, depende del modelo).
- `embedding`: Vector para comparar similitud semántica (e.g., en RAG).
- **Azure AI Foundry**: Los embeddings son clave para agentes que buscan información antes de generar respuestas.

**Práctica**:  

- Ejecuta el script y revisa el embedding. Cambia el texto a "La IA generativa transforma industrias".
- Genera embeddings para dos textos y calcula su similitud coseno con:

  ```python
  import numpy as np
  dot_product = np.dot(embedding1, embedding2)
  norm = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
  similarity = dot_product / norm
  ```

- Revisa `embedding.log` para confirmar la longitud del vector.

## Validación y Solución de Problemas

**Explicación**:  
Validar la configuración y las llamadas asegura que el entorno está listo para capítulos posteriores. Errores comunes incluyen modelos no desplegados, claves inválidas o límites de tokens excedidos.

**Paso a Paso**:  

1. Verifica que el recurso OpenAI está activo y los modelos están desplegados.
2. Confirma el endpoint y clave en variables de entorno.
3. Usa logging para rastrear errores.

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

- Ejecuta el código para listar modelos desplegados. Asegúrate de que `gpt-35-turbo` y `text-embedding-ada-002` están disponibles.
- Simula un error (e.g., modelo no desplegado) y revisa `validate_deployments.log`.

## Notas Adicionales

- **Azure AI Foundry**: Completions y embeddings son la base para agentes generativos en Foundry, que procesan texto o buscan datos semánticamente.
- **Costos**: Monitorea `response.usage.total_tokens` para optimizar gastos. Usa tiers bajos para pruebas.
- **Seguridad**: Almacena claves en Azure Key Vault (lo cubriremos en el Capítulo 4).

## Práctica Final

1. Ejecuta `setup_openai_client.py` y valida la conexión con un prompt simple.
2. Usa `basic_completion.py` para generar una explicación. Ajusta `temperature` y `top_p`.
3. Ejecuta `basic_embedding.py` y calcula la similitud coseno entre dos embeddings.
4. Usa `validate_deployments.py` para confirmar modelos desplegados.
5. Investiga en docs.microsoft.com otros parámetros de `chat.completions.create` (e.g., `n` para múltiples respuestas).
