---
lab:
    title: "Laboratorio: Afinar un modelo de lenguaje usando solo SDK Python de Azure"
    description: "Aprende a afinar, implementar y probar un modelo de lenguaje en Azure usando únicamente el SDK de Python."
---

# Laboratorio: Afinar un modelo de lenguaje usando solo SDK Python de Azure

En este laboratorio, afinarás un modelo de lenguaje en Azure usando únicamente el SDK de Python moderno (azure-ai-ml, azure-identity, openai). No se requieren pasos manuales en el portal.

> **Duración estimada:** 60 minutos

---

## Introducción

El fine-tuning permite personalizar el comportamiento de un modelo de lenguaje para casos de uso específicos. Automatizar el ciclo completo (carga de datos, afinado, despliegue y prueba) es clave para soluciones empresariales reproducibles.

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
    pip install azure-ai-ml azure-identity openai python-dotenv
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
    ```

2. Carga las variables en tus scripts usando `python-dotenv`:

    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    # ...
    ```

---

## Paso 3: Descargar y preparar los datos de entrenamiento

1. Descarga el [conjunto de datos de entrenamiento](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl) y guárdalo como `travel-finetune-hotel.jsonl`.
2. (Opcional) Revisa el archivo para entender el formato JSONL requerido para fine-tuning.

---

## Paso 4: Crear o conectar el workspace de Azure ML

1. Crea un archivo `setup_workspace.py` y agrega el siguiente código para crear o conectar el workspace:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import Workspace
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
    # Si el workspace no existe, créalo
    try:
        ws = ml_client.workspaces.get(os.environ["AZURE_WORKSPACE_NAME"])
        print("Workspace ya existe.")
    except Exception:
        print("Creando workspace...")
        ws = Workspace(
            name=os.environ["AZURE_WORKSPACE_NAME"],
            location="eastus",
            display_name="Lab Fine-tune",
            description="Workspace para laboratorio de fine-tuning"
        )
        ml_client.workspaces.begin_create_or_update(ws).result()
        print("Workspace creado.")
    ```

2. Ejecuta el script:

    ```bash
    python setup_workspace.py
    ```

---

## Paso 5: Afinar el modelo de lenguaje desde Python

1. Usa el SDK para iniciar un trabajo de fine-tuning:

    ```python
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import FineTuningJob
    import os
    from dotenv import load_dotenv

    load_dotenv()
    ml_client = MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
        workspace_name=os.environ["AZURE_WORKSPACE_NAME"]
    )
    job = FineTuningJob(
        display_name="ft-travel",
        model="gpt-4o",
        training_data="./travel-finetune-hotel.jsonl",
        method="supervised"
    )
    job = ml_client.jobs.begin_create_or_update(job).result()
    print(f"Fine-tuning job iniciado: {job.name}")
    ```

    > **Nota:** El fine-tuning puede tardar varios minutos. Puedes monitorear el estado del trabajo con el SDK.

---

## Paso 6: Implementar el modelo afinado

1. Cuando el trabajo de fine-tuning termine, implementa el modelo afinado:

    ```python
    from azure.ai.ml.entities import ManagedOnlineDeployment
    deployment = ManagedOnlineDeployment(
        name="ft-travel-deployment",
        model=job.outputs["model"],
        instance_type="Standard_DS3_v2",
        instance_count=1
    )
    ml_client.online_deployments.begin_create_or_update(deployment).result()
    print("Modelo afinado implementado.")
    ```

---

## Paso 7: Probar y comparar el modelo base y el modelo afinado

1. Crea un archivo `test_models.py` con el siguiente código:

    ```python
    import os
    from openai import AzureOpenAI
    from dotenv import load_dotenv

    load_dotenv()
    openai_client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version="2023-05-15",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )
    prompts = [
        "¿Dónde debería hospedarme en Roma?",
        "Principalmente voy por la comida. ¿Dónde debería hospedarme para estar a poca distancia de restaurantes asequibles?",
        "¿Cuáles son algunas delicias locales que debería probar?",
        "¿Cuál es la mejor época del año para visitar en términos del clima?",
        "¿Cuál es la mejor manera de moverse por la ciudad?"
    ]
    for model in ["gpt-4o", "ft-travel-deployment"]:  # Cambia por el nombre real de tu deployment
        print(f"\nRespuestas del modelo: {model}")
        for prompt in prompts:
            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "Eres un asistente de viajes de IA..."}, {"role": "user", "content": prompt}]
            )
            print(f"Q: {prompt}\nA: {response.choices[0].message.content}\n")
    ```

2. Ejecuta el script y compara las respuestas del modelo base y el modelo afinado.

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

En este laboratorio, automatizaste el fine-tuning, despliegue y prueba de un modelo de lenguaje en Azure usando solo el SDK de Python. Este enfoque es ideal para soluciones empresariales reproducibles y escalables.

---

**¡Listo! Has completado el laboratorio de fine-tuning usando solo el SDK de Python de Azure.**
