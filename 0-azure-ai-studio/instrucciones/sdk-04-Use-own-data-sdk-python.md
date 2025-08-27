---
lab:
    title: "Laboratorio: Aplicación RAG con tus propios datos usando solo SDK Python de Azure"
    description: "Aprende a construir una aplicación de chat RAG (Retrieval Augmented Generation) que fundamenta respuestas usando tus propios datos, empleando únicamente el SDK de Python de Azure."
---

# Laboratorio: Aplicación RAG con tus propios datos usando solo SDK Python de Azure

En este laboratorio, crearás una solución de Generación Aumentada por Recuperación (RAG) en Azure, usando únicamente el SDK de Python moderno (azure-ai-ml, azure-identity, openai, azure-search-documents). No se requieren pasos manuales en el portal.

> **Duración estimada:** 45 minutos

---

## Introducción

RAG es un patrón esencial para aplicaciones de IA generativa que requieren fundamentar respuestas con datos propios. Automatizar el ciclo completo (carga, indexación, consulta y chat) es clave para soluciones empresariales reproducibles.

---

## Paso 1: Preparar el entorno de desarrollo

1. Abre una terminal y navega a la carpeta de trabajo.
2. (Opcional) Crea y activa un entorno virtual:

    ```bash
    python3 -m venv labenv
    source labenv/bin/activate
    ```

3. Instala las dependencias necesarias:

    ```bash
    pip install azure-ai-ml azure-identity openai azure-search-documents python-dotenv
    ```

---

## Paso 2: Configurar autenticación y variables de entorno

1. Crea un archivo `.env` con las siguientes variables (reemplaza los valores):

    ```env
    AZURE_SUBSCRIPTION_ID=<tu-subscription-id>
    AZURE_RESOURCE_GROUP=<nombre-grupo-recursos>
    AZURE_WORKSPACE_NAME=<nombre-workspace>
    AZURE_OPENAI_ENDPOINT=<endpoint-openai>
    AZURE_OPENAI_KEY=<api-key-openai>
    AZURE_SEARCH_ENDPOINT=<endpoint-search>
    AZURE_SEARCH_KEY=<api-key-search>
    ```

2. Carga las variables en tus scripts usando `python-dotenv`:

    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # ...
    ```

---

## Paso 3: Cargar y preparar tus propios datos

1. Descarga el [archivo zip de folletos](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) y extrae la carpeta `brochures`.
2. Sube los archivos PDF a un contenedor de Azure Storage Blob usando el SDK:

    ```python
    from azure.storage.blob import BlobServiceClient
    import os
    from dotenv import load_dotenv

    load_dotenv()
    blob_service = BlobServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])
    container_name = "brochures"
    blob_service.create_container(container_name)
    for file in os.listdir("brochures"):
        with open(f"brochures/{file}", "rb") as data:
            blob_service.get_blob_client(container=container_name, blob=file).upload_blob(data)
    print("Datos cargados en Azure Blob Storage.")
    ```

    > **Nota:** Si no tienes un Storage Account, créalo con el SDK o portal y agrega la variable `AZURE_STORAGE_CONNECTION_STRING` a tu `.env`.

---

## Paso 4: Crear un índice en Azure AI Search desde Python

1. Usa el SDK para crear un índice vectorial sobre los datos cargados:

    ```python
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField, VectorSearch, HnswAlgorithmConfiguration, VectorSearchAlgorithmKind
    from azure.core.credentials import AzureKeyCredential
    import os
    from dotenv import load_dotenv

    load_dotenv()
    search_client = SearchIndexClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
    )
    index_name = "brochures-index"
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String")
    ]
    vector_search = VectorSearch(
        algorithm_configurations=[
            HnswAlgorithmConfiguration(
                name="vector-config",
                kind=VectorSearchAlgorithmKind.HNSW
            )
        ]
    )
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )
    search_client.create_index(index)
    print("Índice creado en Azure AI Search.")
    ```

    > **Nota:** Para indexar el contenido de los PDFs, deberás extraer el texto (por ejemplo, usando PyPDF2) y cargarlo como documentos en el índice.

---

## Paso 5: Indexar el contenido de los PDFs

1. Extrae el texto de los PDFs y súbelo al índice:

    ```python
    import os
    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential
    from PyPDF2 import PdfReader
    from dotenv import load_dotenv

    load_dotenv()
    search_client = SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name="brochures-index",
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
    )
    docs = []
    for file in os.listdir("brochures"):
        if file.endswith(".pdf"):
            reader = PdfReader(f"brochures/{file}")
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
            docs.append({"id": file, "content": text})
    search_client.upload_documents(documents=docs)
    print("Documentos indexados.")
    ```

    > **Consejo:** Puedes dividir los textos largos en fragmentos para mejorar la recuperación.

---

## Paso 6: Crear una aplicación RAG en Python

1. Crea un archivo `rag_app.py` con el siguiente código:

    ```python
    import os
    from openai import AzureOpenAI
    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential
    from dotenv import load_dotenv

    load_dotenv()
    openai_client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version="2023-05-15",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )
    search_client = SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name="brochures-index",
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
    )

    def search_docs(query):
        results = search_client.search(query, top=3)
        return "\n".join([doc["content"][:500] for doc in results])

    prompt = [
        {"role": "system", "content": "Eres un asistente de viajes que responde usando solo la información proporcionada."}
    ]

    print("Escribe tu pregunta (o 'quit' para salir):")
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() == "quit":
            break
        context = search_docs(user_input)
        prompt.append({"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {user_input}"})
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # Cambia por el nombre de tu deployment
            messages=prompt
        )
        answer = response.choices[0].message.content
        print(f"AI: {answer}")
        prompt.append({"role": "assistant", "content": answer})
    ```

---

## Paso 7: Ejecutar y probar la aplicación RAG

1. Ejecuta la app:

    ```bash
    python rag_app.py
    ```

2. Prueba preguntas como:
    - ¿Dónde puedo hospedarme en Nueva York?
    - ¿Qué actividades recomienda Margie's Travel?

---

## Paso 8: Limpieza de recursos

1. Elimina los recursos creados para evitar costos innecesarios:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml import MLClient
    import os
    from dotenv import load_dotenv

    load_dotenv()
    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
        workspace_name=os.environ["AZURE_WORKSPACE_NAME"]
    )
    ml_client.workspaces.begin_delete(os.environ["AZURE_WORKSPACE_NAME"])
    print("Workspace eliminado.")
    ```

---

## Resumen

En este laboratorio, automatizaste la carga, indexación y consulta de tus propios datos en Azure, y creaste una aplicación RAG usando solo el SDK de Python. Este enfoque es ideal para soluciones empresariales reproducibles y escalables.

---

**¡Listo! Has completado el laboratorio RAG con tus propios datos usando solo el SDK de Python de Azure.**
