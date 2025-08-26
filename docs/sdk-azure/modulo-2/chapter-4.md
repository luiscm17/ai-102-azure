# Capítulo 4: Temas Avanzados

En este capítulo, exploramos técnicas avanzadas para Azure OpenAI, incluyendo *fine-tuning* para personalizar modelos, RAG completo integrando Azure Cognitive Search (`azure-search-documents` v11.5.3) para búsqueda de documentos, evaluación de respuestas generativas con `azure-ai-evaluation` (v1.10.0), y estrategias de seguridad para proteger datos sensibles. Usaremos el SDK `openai` (v1.101.0) y `azure-identity` (v1.24.0) para autenticación, con ejemplos prácticos que simulan escenarios de Azure AI Foundry, como agentes que combinan búsqueda y generación. Todo se implementará mediante código, con logging para rastrear operaciones y depurar errores.

## Objetivos del Capítulo

- Personalizar modelos con *fine-tuning* usando Azure OpenAI.
- Implementar RAG completo con Azure Cognitive Search para retrieval.
- Evaluar respuestas generativas con `azure-ai-evaluation`.
- Aplicar medidas de seguridad (e.g., Key Vault, moderación de contenido).

## Fine-Tuning de Modelos

**Explicación**:  
*Fine-tuning* permite personalizar un modelo de Azure OpenAI (e.g., GPT-3.5-turbo) con datos específicos para mejorar su rendimiento en tareas concretas, como generar respuestas en un estilo empresarial o clasificar texto. Usaremos el SDK `openai` para preparar datos, cargar un dataset, y entrenar un modelo. Nota: *Fine-tuning* en Azure OpenAI requiere un dataset en formato JSONL y puede incurrir en costos adicionales.

**Paso a Paso**:  

1. Prepara un dataset en formato JSONL.
2. Carga el dataset y configura *fine-tuning*.
3. Valida el modelo personalizado.

**Código Práctico** (guarda como `fine_tuning.py`):

```python
# fine_tuning.py
from openai import AzureOpenAI
import os
import logging
import json

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("fine_tuning.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Dataset de ejemplo (guarda como training_data.jsonl)

dataset = [
    {"messages": [
        {"role": "system", "content": "Eres un asistente empresarial formal."},
        {"role": "user", "content": "Redacta un correo invitando a un evento de IA."},
        {"role": "assistant", "content": "Asunto: Invitación al Evento de Inteligencia Artificial\nEstimado/a,\nLo invitamos cordialmente a nuestro evento de IA el 15/09/2025, donde exploraremos innovaciones en Azure AI. Confirme su asistencia a contact@empresa.com.\nSaludos,\nEquipo AI"}]}
]

# Guardar dataset

with open("training_data.jsonl", "w") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

# Subir dataset y comenzar fine-tuning

try:
    logger.info("Subiendo dataset para fine-tuning")
    file_response = client.files.create(file=open("training_data.jsonl", "rb"), purpose="fine-tune")
    file_id = file_response.id
    logger.info(f"Dataset subido: {file_id}")

    logger.info("Iniciando fine-tuning")
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-35-turbo"
    )
    job_id = fine_tune_response.id
    logger.info(f"Fine-tuning iniciado: {job_id}")

    # Verificar estado (esto puede tomar tiempo)
    status = client.fine_tuning.jobs.retrieve(job_id).status
    logger.info(f"Estado del fine-tuning: {status}")
except Exception as e:
    logger.error(f"Error en fine-tuning: {e}")
```

**Explicación**:  

- `training_data.jsonl`: Formato requerido con mensajes de ejemplo (`system`, `user`, `assistant`).
- `client.files.create`: Sube el dataset a Azure OpenAI.
- `client.fine_tuning.jobs.create`: Inicia el proceso de *fine-tuning*. Nota: Puede tomar horas y requiere monitoreo asíncrono.
- **Costos**: *Fine-tuning* incurre en cargos; usa datasets pequeños para pruebas.

**Práctica**:  

- Ejecuta el script con un dataset pequeño (2-3 ejemplos). Revisa `fine_tuning.log`.
- Añade más ejemplos al dataset (e.g., otro correo formal). Vuelve a ejecutar.
- Investiga en docs.microsoft.com parámetros adicionales de *fine-tuning* (e.g., `validation_file`).

## RAG Completo con Azure Cognitive Search

**Explicación**:  
Retrieval-Augmented Generation (RAG) mejora las respuestas generativas al integrar búsqueda de documentos relevantes usando Azure Cognitive Search (`azure-search-documents` v11.5.3). A diferencia del RAG simple del Capítulo 3 (en memoria), aquí indexaremos documentos en Azure Search, buscaremos los más relevantes con embeddings, y los usaremos en un prompt.

**Paso a Paso**:  

1. Configura un índice en Azure Cognitive Search.
2. Indexa documentos con embeddings generados por Azure OpenAI.
3. Realiza una búsqueda y usa el resultado en una *chat completion*.

**Código Práctico** (guarda como `full_rag.py`):

```python
# full_rag.py
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery
import os
import logging
import numpy as np

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("full_rag.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura clientes

credential = DefaultAzureCredential()
openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT", "<https://mysearch.search.windows.net>")
search_api_key = os.environ.get("AZURE_SEARCH_API_KEY", "tu-search-api-key")
index_name = "myindex"
openai_client = AzureOpenAI(azure_endpoint=openai_endpoint, api_key=openai_api_key, api_version="2024-08-01-preview")
search_client = SearchClient(search_endpoint, index_name, credential=DefaultAzureCredential())
index_client = SearchIndexClient(search_endpoint, credential=DefaultAzureCredential())

# Crear índice

from azure.search.documents.indexes.models import SearchIndex, SearchField, SearchFieldDataType, VectorSearch
try:
    logger.info("Creando índice en Azure Search")
    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content", type=SearchFieldDataType.String),
        SearchField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1536, vector_search_profile_name="my-vector-config")
    ]
    vector_search = VectorSearch(profiles=[{"name": "my-vector-config", "algorithm_configuration_name": "my-hnsw"}])
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    index_client.create_or_update_index(index)
    logger.info(f"Índice {index_name} creado")
except Exception as e:
    logger.error(f"Error al crear índice: {e}")

# Indexar documentos

documents = [
    {"id": "1", "content": "Azure OpenAI ofrece modelos generativos para texto e imágenes."},
    {"id": "2", "content": "RAG combina búsqueda y generación para respuestas precisas."}
]
try:
    logger.info("Generando embeddings e indexando documentos")
    for doc in documents:
        embedding = openai_client.embeddings.create(model="text-embedding-ada-002", input=doc["content"]).data[0].embedding
        doc["embedding"] = embedding
    search_client.upload_documents(documents)
    logger.info("Documentos indexados")
except Exception as e:
    logger.error(f"Error al indexar: {e}")

# RAG: Buscar y generar respuesta

try:
    logger.info("Ejecutando RAG")
    query = "Explica cómo funciona RAG."
    query_embedding = openai_client.embeddings.create(model="text-embedding-ada-002", input=query).data[0].embedding
    vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=1, fields="embedding")
    results = search_client.search(search_text=None, vector_queries=[vector_query])
    best_doc = next[results]("content")
    logger.info(f"Documento recuperado: {best_doc}")

    response = openai_client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "Usa el contexto proporcionado para responder."},
            {"role": "user", "content": f"Contexto: {best_doc}\n{query}"}
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

- `SearchIndex`: Crea un índice en Azure Cognitive Search con un campo para embeddings.
- `upload_documents`: Indexa documentos con embeddings generados por `text-embedding-ada-002`.
- `VectorizedQuery`: Busca el documento más relevante usando similitud de embeddings.
- **RAG**: Combina el documento recuperado con el prompt para una respuesta contextual.
- **Azure AI Foundry**: Simula un agente que usa búsqueda para responder preguntas empresariales.

**Práctica**:  

- Configura `AZURE_SEARCH_ENDPOINT` y `AZURE_SEARCH_API_KEY` (crea un servicio Azure Search si no lo tienes).
- Ejecuta el script y revisa la respuesta. Añade un nuevo documento a la lista.
- Cambia el `query` a "Describe Azure OpenAI". Revisa `full_rag.log`.

## Evaluación con `azure-ai-evaluation`

**Explicación**:  
`azure-ai-evaluation` (v1.10.0) permite evaluar la calidad de respuestas generativas en métricas como relevancia, coherencia o exactitud. Usaremos este SDK para evaluar una respuesta generada por el modelo, simulando un caso de auditoría para un agente en Azure AI Foundry.

**Paso a Paso**:  

1. Instala `azure-ai-evaluation`.
2. Evalúa una respuesta generada.
3. Analiza métricas.

**Código Práctico** (guarda como `evaluate_response.py`):

```python
# evaluate_response.py
from openai import AzureOpenAI
import os
import logging

# Nota: azure-ai-evaluation es un paquete beta, simulamos su funcionalidad

# pip install azure-ai-evaluation==1.10.0

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("evaluation.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura cliente

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Generar respuesta para evaluar

try:
    logger.info("Generando respuesta para evaluación")
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente técnico."},
            {"role": "user", "content": "Explica qué es RAG en 50 palabras."}
        ],
        max_tokens=100
    )
    generated_text = response.choices[0].message.content
    logger.info(f"Respuesta generada: {generated_text}")

    # Simulación de evaluación (azure-ai-evaluation no está completamente documentado)
    evaluation = {
        "relevance": 0.9,  # Supongamos métricas calculadas
        "coherence": 0.85,
        "fluency": 0.95
    }
    logger.info(f"Evaluación: {evaluation}")
    print(f"Evaluación: {evaluation}")
except Exception as e:
    logger.error(f"Error en evaluación: {e}")
```

**Explicación**:  

- **Nota**: `azure-ai-evaluation` es un paquete beta con documentación limitada al 25/08/2025. Simulamos su funcionalidad con métricas ficticias.
- `generated_text`: Respuesta generada para evaluar.
- **Uso**: En producción, usarías `azure-ai-evaluation` para métricas reales (e.g., relevancia basada en un dataset de referencia).

**Práctica**:  

- Ejecuta el script y revisa la respuesta simulada. Añade un nuevo prompt para evaluar.
- Investiga en docs.microsoft.com métricas soportadas por `azure-ai-evaluation`.
- Revisa `evaluation.log` para confirmar la evaluación.

## Seguridad en Generative AI

**Explicación**:  
La seguridad en IA generativa incluye proteger datos sensibles, moderar contenido y gestionar credenciales. Usaremos Azure Key Vault para almacenar claves y `azure-ai-contentsafety` (v1.0.0) para moderar respuestas. Esto es crucial para agentes en Azure AI Foundry que manejan datos sensibles.

**Paso a Paso**:  

1. Almacena la clave API en Azure Key Vault.
2. Modera una respuesta con `azure-ai-contentsafety`.
3. Valida la configuración.

**Código Práctico** (guarda como `secure_generative.py`):

```python
# secure_generative.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI
import os
import logging

# Configurar logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("secure_generative.log"), logging.StreamHandler()]
)
logger = logging.getLogger(**name**)

# Configura Key Vault

credential = DefaultAzureCredential()
vault_url = os.environ.get("AZURE_KEY_VAULT_URL", "<https://myvault.vault.azure.net/>")
secret_client = SecretClient(vault_url, credential)
try:
    api_key = secret_client.get_secret("openai-api-key").value
    logger.info("Clave API obtenida de Key Vault")
except Exception as e:
    logger.error(f"Error al obtener clave de Key Vault: {e}")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "tu-api-key")

# Configura cliente OpenAI

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "<https://myopenai002.openai.azure.com/>")
client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2024-08-01-preview")

# Generar y moderar respuesta

try:
    logger.info("Generando respuesta")
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente seguro."},
            {"role": "user", "content": "Genera un texto sobre tecnología."}
        ],
        max_tokens=100
    )
    text = response.choices[0].message.content
    logger.info(f"Respuesta generada: {text}")

    # Simulación de moderación (azure-ai-contentsafety)
    moderation_result = {"is_safe": True, "issues": []}  # Supongamos que pasa
    logger.info(f"Moderación: {moderation_result}")
    print(f"Respuesta: {text}\nModeración: {moderation_result}")
except Exception as e:
    logger.error(f"Error en generación o moderación: {e}")
```

**Explicación**:  

- `SecretClient`: Obtiene la clave API desde Azure Key Vault.
- **Moderación**: Simulamos `azure-ai-contentsafety` (requiere configuración real del servicio).
- **Seguridad**: Usar Key Vault evita hardcoding de claves.

**Práctica**:  

- Configura un Key Vault y almacena `openai-api-key`. Ejecuta el script.
- Añade un prompt con contenido potencialmente sensible y simula moderación.
- Revisa `secure_generative.log`.

## Validación y Solución de Problemas

**Explicación**:  
Validar las configuraciones asegura que el entorno está listo. Errores comunes incluyen permisos insuficientes, índices de búsqueda no creados o modelos no desplegados.

**Paso a Paso**:  

1. Verifica que los modelos (`gpt-35-turbo`, `text-embedding-ada-002`) están desplegados.
2. Confirma la configuración de Azure Search y Key Vault.
3. Usa logging para depurar.

**Código para Validar Modelos** (reutilizamos del Capítulo 3):

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
- Simula un error (e.g., índice no existente) y revisa los logs.

## Notas Adicionales

- **Azure AI Foundry**: RAG y *fine-tuning* son esenciales para agentes que necesitan respuestas precisas y personalizadas.
- **Costos**: Monitorea tokens y uso de Azure Search. Usa tiers bajos para pruebas.
- **Seguridad**: Implementa RBAC y moderación para cumplir con normativas (e.g., GDPR).

## Práctica Final

1. Ejecuta `fine_tuning.py` con un dataset pequeño. Revisa el estado en `fine_tuning.log`.
2. Usa `full_rag.py` para implementar RAG. Añade más documentos y prueba un nuevo `query`.
3. Ejecuta `evaluate_response.py` y simula evaluación de otra respuesta.
4. Usa `secure_generative.py` con Key Vault. Prueba moderación con un prompt sensible.
5. Valida modelos con `validate_deployments.py`.
