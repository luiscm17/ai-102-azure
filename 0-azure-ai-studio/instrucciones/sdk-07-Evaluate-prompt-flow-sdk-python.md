---
lab:
    title: "Laboratorio: Evaluar el rendimiento de un modelo de IA generativa usando solo SDK Python de Azure"
    description: "Aprende a evaluar modelos y prompts para optimizar el rendimiento de tu aplicación de chat usando únicamente el SDK de Python de Azure."
---

# Laboratorio: Evaluar el rendimiento de un modelo de IA generativa usando solo SDK Python de Azure

En este laboratorio, aprenderás a evaluar el rendimiento de un modelo de IA generativa usando únicamente el SDK de Python de Azure (azure-ai-ml, openai, pandas, etc.), sin pasos manuales en el portal.

> **Duración estimada:** 30 minutos

---

## Introducción

La evaluación de modelos de IA generativa es fundamental para optimizar la calidad de las respuestas y la experiencia del usuario. Puedes realizar evaluaciones manuales y automatizadas desde código, comparar modelos y obtener métricas objetivas para mejorar tus soluciones.

> **Nota:** Algunas capacidades de evaluación pueden requerir recursos específicos o estar en vista previa. Consulta la [documentación oficial de Azure AI](https://learn.microsoft.com/azure/ai-services/openai/how-to/evaluate-models) para detalles y actualizaciones.

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
   pip install azure-ai-ml azure-identity openai python-dotenv pandas scikit-learn
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

## Paso 3: Descargar y preparar los datos de evaluación

1. Descarga el archivo [travel_evaluation_data.jsonl](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel_evaluation_data.jsonl) y guárdalo como `travel_evaluation_data.jsonl`.
2. Carga los datos en un DataFrame de pandas:

   ```python
   import pandas as pd
   df = pd.read_json("travel_evaluation_data.jsonl", lines=True)
   print(df.head())
   ```

---

## Paso 4: Desplegar y autenticar modelos desde Python

1. Usa el SDK para crear o conectar el workspace y desplegar los modelos (ejemplo con gpt-4o y gpt-4o-mini):

   ```python
   from azure.identity import DefaultAzureCredential
   from azure.ai.ml import MLClient
   from azure.ai.ml.entities import Workspace, ManagedOnlineDeployment
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
   # Desplegar modelo base (gpt-4o)
   deployment = ManagedOnlineDeployment(
       name="gpt4o-deployment",
       model="gpt-4o",
       instance_type="Standard_DS3_v2",
       instance_count=1
   )
   ml_client.online_deployments.begin_create_or_update(deployment).result()
   # Desplegar modelo mini (gpt-4o-mini)
   deployment_mini = ManagedOnlineDeployment(
       name="gpt4o-mini-deployment",
       model="gpt-4o-mini",
       instance_type="Standard_DS3_v2",
       instance_count=1
   )
   ml_client.online_deployments.begin_create_or_update(deployment_mini).result()
   print("Modelos desplegados.")
   ```

---

## Paso 5: Evaluación manual desde código

1. Crea un archivo `manual_evaluation.py` con el siguiente código:

   ```python
   import os
   import pandas as pd
   from openai import AzureOpenAI
   from dotenv import load_dotenv

   load_dotenv()
   df = pd.read_json("travel_evaluation_data.jsonl", lines=True)
   openai_client = AzureOpenAI(
       api_key=os.environ["AZURE_OPENAI_KEY"],
       api_version="2023-05-15",
       azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
   )
   system_message = "Asiste a los usuarios con consultas relacionadas con viajes, ofreciendo consejos, asesoramiento y recomendaciones como un agente de viajes experto."
   results = []
   for _, row in df.iterrows():
       response = openai_client.chat.completions.create(
           model="gpt-4o-mini",  # Cambia por el nombre de tu deployment
           messages=[{"role": "system", "content": system_message}, {"role": "user", "content": row["Question"]}]
       )
       results.append({
           "question": row["Question"],
           "expected": row["ExpectedResponse"],
           "output": response.choices[0].message.content
       })
   eval_df = pd.DataFrame(results)
   eval_df.to_csv("manual_eval_results.csv", index=False)
   print(eval_df.head())
   ```

2. Revisa el archivo generado y compara manualmente las respuestas del modelo con las esperadas.

---

## Paso 6: Evaluación automatizada y métricas

1. Crea un archivo `automated_evaluation.py` para calcular métricas objetivas:

   ```python
   import pandas as pd
   from sklearn.metrics import f1_score
   from sklearn.feature_extraction.text import CountVectorizer

   df = pd.read_csv("manual_eval_results.csv")
   # F1 Score basado en palabras
   def f1_for_row(row):
       y_true = row["expected"].split()
       y_pred = row["output"].split()
       # Vectorización simple
       vectorizer = CountVectorizer().fit([row["expected"], row["output"]])
       y_true_vec = vectorizer.transform([row["expected"]]).toarray()[0]
       y_pred_vec = vectorizer.transform([row["output"]]).toarray()[0]
       return f1_score(y_true_vec, y_pred_vec, average="weighted")
   df["f1_score"] = df.apply(f1_for_row, axis=1)
   print(df[["question", "f1_score"]].head())
   print(f"F1 Score promedio: {df['f1_score'].mean():.2f}")
   ```

2. Puedes agregar otras métricas como similitud semántica usando embeddings o relevancia con modelos adicionales.

---

## Paso 7: Consideraciones y mejores prácticas

- Realiza pruebas con diferentes modelos y prompts para comparar resultados.
- Usa conjuntos de datos variados y realistas para evaluar la robustez del modelo.
- Interpreta las métricas en contexto: un F1 alto no siempre implica respuestas útiles para el usuario.
- Documenta los experimentos y guarda los resultados para futuras comparaciones.
- Consulta la [documentación de evaluación de modelos en Azure](https://learn.microsoft.com/azure/ai-services/openai/how-to/evaluate-models) para más ejemplos y métricas avanzadas.

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

En este laboratorio, automatizaste la evaluación manual y automática de modelos de IA generativa usando solo el SDK de Python. Este enfoque es ideal para flujos de trabajo reproducibles y comparaciones objetivas entre modelos y prompts.

---

**¡Listo! Has completado el laboratorio de evaluación de modelos usando solo el SDK de Python de Azure.**
