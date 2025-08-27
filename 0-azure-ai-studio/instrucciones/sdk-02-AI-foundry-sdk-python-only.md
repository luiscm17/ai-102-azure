---
lab:
    title: "Laboratorio: Automatización de modelos generativos en Azure - Parte 1: Azure CLI (OpenAI clásico)"
    description: "Aprende a crear y consumir un modelo generativo en Azure usando Azure CLI para recursos de Azure OpenAI clásico."
---

# Laboratorio: Automatización de modelos generativos en Azure - Parte 1: Azure CLI (OpenAI clásico)

En esta primera parte aprenderás a crear y consumir modelos generativos en Azure usando **Azure CLI** para recursos de Azure OpenAI clásico. El objetivo es automatizar el ciclo de vida de recursos y modelos, evitando pasos manuales en el portal.

> **Duración estimada:** 20 minutos

---

## 1. Crear grupo de recursos y recurso Azure OpenAI

```bash
az group create --name <nombre-grupo> --location <region>

az cognitiveservices account create \
    --name openai-lab-sdk \
    --resource-group <nombre-grupo> \
    --kind OpenAI \
    --sku S0 \
    --location eastus
```

---

## 2. Explorar modelos y versiones disponibles

Antes de crear el deployment, explora los modelos y versiones disponibles en tu recurso Azure OpenAI. Así podrás elegir el modelo correcto y evitar errores.

### Opción 1: Azure CLI (con jq)

```bash
az cognitiveservices account list-models -n opengpt41-foundry-rs -g rg-gpt41-sdk | jq '.[] | { name: .name, format: .format, version: .version, sku: .skus[0].name, capacity: .skus[0].capacity.default }'
```

Esto mostrará un json como el siguiente:

```json
{
  "name": "Phi-3.5-vision-instruct",
  "format": "Microsoft",
  "version": "2",
  "sku": "GlobalStandard",
  "capacity": 1
}
```

Así puedes elegir el modelo y versión correctos para tu deployment.

> Si no tienes jq, puedes instalarlo con: `sudo apt-get install jq` (Linux) o usar el script Python siguiente.

### Opción 2: Python (procesando el JSON)

Si prefieres hacerlo en Python (por ejemplo, para integrarlo en un notebook o script):

```python
import json

with open("models.json") as f:
    models = json.load(f)

for m in models:
    name = m.get("name")
    version = m.get("version")
    status = m.get("lifecycleStatus")
    deprecation = m.get("deprecation", {}).get("inference")
    print(f"{name}\t{version}\t{status}\tDeprecado: {deprecation}")
```

Esto te permite filtrar y visualizar solo la información relevante para crear tu deployment.

---

## 3. Crear el deployment del modelo

Para desplegar un modelo en Azure OpenAI con CLI, usa el siguiente comando generalizado:

```bash
az cognitiveservices account deployment create -n opengpt41-foundry-rs \
    -g rg-gpt41-sdk \
    --deployment-name Phi-3.5-vision-instruct \
    --model-name Phi-3.5-vision-instruct \
    --model-version 2 \
    --model-format Microsoft \
    --sku-capacity 1 \
    --sku-name GlobalStandard
```

**Explicación de parámetros clave:**

- `--resource-group`: Grupo de recursos donde está tu recurso OpenAI.
- `--name`: Nombre del recurso OpenAI.
- `--deployment-name`: Nombre que le das a este deployment (puede ser cualquier identificador único).
- `--model-name`: Nombre exacto del modelo (ejemplo: `gpt-4.1`, `gpt-4o`).
- `--model-version`: Versión exacta del modelo (ejemplo: `2025-04-14`).
- `--model-format`: Siempre `OpenAI` para modelos OpenAI.
- `--sku-name`: SKU compatible con el modelo (ejemplo: `GlobalStandard`, `Standard`, etc. Consulta la lista de SKUs válidos para tu modelo con el comando de exploración de modelos).
- `--sku-capacity`: Número de instancias a aprovisionar. Para pruebas/labs, usa `1` (mínimo recomendado).

**Ejemplo para gpt-4.1:**

```bash
az cognitiveservices account deployment create \
    -g <nombre-grupo> \
    -n openai-lab-sdk \
    --deployment-name gpt41-deployment \
    --model-name gpt-4.1 \
    --model-version "2025-04-14" \
    --model-format OpenAI \
    --sku-capacity 1 \
    --sku-name GlobalStandard
```

> **Nota:** Si recibes errores de SKU o capacidad, revisa los valores válidos en la salida del comando de exploración de modelos. La capacidad mínima suele ser 1.

---

## 4. Obtener endpoint y claves

```bash
az cognitiveservices account keys list  -n opengpt41-foundry-rs -g rg-gpt41-sdk

az cognitiveservices account show  -n opengpt41-foundry-rs -g rg-gpt41-sdk | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

Guarda el endpoint y una API key para usarlos en tu aplicación Python.

---

## 5. Consumir el modelo desde Python

```python
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2023-05-15",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

DEPLOYMENT = "gpt-4o"  # Cambia por el nombre de tu deployment

prompt = [
    {"role": "system", "content": "Eres un asistente útil de IA."}
]

print("Escribe tu pregunta (o 'quit' para salir):")
while True:
    user_input = input("Usuario: ")
    if user_input.lower() == "quit":
        break
    prompt.append({"role": "user", "content": user_input})
    response = openai_client.chat.completions.create(
        model=DEPLOYMENT,
        messages=prompt
    )
    answer = response.choices[0].message.content
    print(f"AI: {answer}")
    prompt.append({"role": "assistant", "content": answer})
```

---

## 6. Limpieza de recursos

Recuerda eliminar los recursos creados para evitar costos innecesarios. Puedes hacerlo con Azure CLI:

```bash
az group delete --name <nombre-grupo>
```

O desde el portal de Azure.

---

## Resumen

En esta parte, aprendiste a automatizar la creación y consumo de modelos generativos en Azure usando **Azure CLI** para recursos y deployments de Azure OpenAI clásico. Esto te permite construir flujos reproducibles y escalables, evitando pasos manuales en el portal.

---

**¡Listo! Has completado la Parte 1 del laboratorio!**

---

# Laboratorio: Automatización de modelos generativos en Azure - Parte 2: SDK Python (Foundry)

En esta segunda parte aprenderás a crear y consumir modelos generativos en Azure usando el **SDK Python** para recursos y proyectos de Azure AI Foundry. El objetivo es automatizar el ciclo de vida de proyectos y modelos Foundry, evitando pasos manuales en el portal.

> **Duración estimada:** 20 minutos

---

## 1. Instalar dependencias

```bash
pip install azure-identity azure-mgmt-cognitiveservices azure-ai-projects python-dotenv
```

---

## 2. Crear el recurso Foundry y un proyecto

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

load_dotenv()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = os.environ["AZURE_RESOURCE_GROUP"]
foundry_resource_name = os.environ["AZURE_FOUNDRY_RESOURCE"]
foundry_project_name = os.environ["AZURE_FOUNDRY_PROJECT"]
location = "eastus"

credential = DefaultAzureCredential()
client = CognitiveServicesManagementClient(
    credential=credential,
    subscription_id=subscription_id,
    api_version="2025-04-01-preview"
)

# Crear recurso Foundry
resource = client.accounts.begin_create(
    resource_group_name=resource_group,
    account_name=foundry_resource_name,
    account={
        "location": location,
        "kind": "AIServices",
        "sku": {"name": "S0",},
        "identity": {"type": "SystemAssigned"},
        "properties": {"allowProjectManagement": True, "customSubDomainName": foundry_resource_name}
    }
)
resource.result()

# Crear proyecto Foundry
project = client.projects.begin_create(
    resource_group_name=resource_group,
    account_name=foundry_resource_name,
    project_name=foundry_project_name,
    project={
        "location": location,
        "identity": {"type": "SystemAssigned"},
        "properties": {}
    }
)
project.result()
print("Proyecto Foundry creado correctamente.")
```

> **Nota:** Consulta la [documentación oficial](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects?pivots=fdp-project&tabs=python) para más detalles y ejemplos avanzados.

---

## 3. Desplegar un modelo en Foundry

El deployment de modelos se realiza con el SDK Python. El proceso y los parámetros pueden variar según el tipo de modelo y proyecto, pero los conceptos clave son:

- `model_name`: Nombre del modelo a desplegar.
- `model_version`: Versión específica del modelo.
- `deployment_name`: Nombre único para el deployment.
- `sku_name` y `capacity`: Algunos métodos del SDK permiten especificar SKU/capacidad, otros lo gestionan automáticamente.

**Ejemplo básico (pseudocódigo, consulta la documentación oficial para detalles según el SDK):**

```python
from azure.ai.projects import FoundryClient

client = FoundryClient(...)
deployment = client.deploy_model(
    project_name="<nombre-proyecto>",
    model_name="gpt-4.1",
    model_version="2025-04-14",
    deployment_name="gpt41-deployment",
    sku_name="GlobalStandard",  # si aplica
    capacity=1  # si aplica
)
print("Deployment creado:", deployment)
```

> **Recomendación:** Consulta siempre la documentación oficial del SDK para el método y parámetros exactos según el tipo de recurso/modelo.

---

## 4. Consumir el modelo desplegado en Foundry

Consulta la documentación de Foundry para obtener el endpoint y las credenciales del deployment, y usa el SDK adecuado para consumir el modelo.

---

## 5. Limpieza de recursos

Recuerda eliminar los recursos creados para evitar costos innecesarios. Puedes hacerlo con Azure CLI:

```bash
az group delete --name <nombre-grupo>
```

O desde el portal de Azure.

---

## Resumen

En esta parte, aprendiste a automatizar la creación y consumo de modelos generativos en Azure usando el **SDK Python** para recursos y proyectos de Azure AI Foundry. Esto te permite construir flujos reproducibles y escalables, evitando pasos manuales en el portal.

---

**¡Listo! Has completado la Parte 2 del laboratorio!**
