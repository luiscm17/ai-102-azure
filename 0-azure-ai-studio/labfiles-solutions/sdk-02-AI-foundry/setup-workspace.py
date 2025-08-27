import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace

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
        display_name="Lab2 AI Chat",
        description="Workspace para laboratorio de chat generativo"
    )
    ml_client.workspaces.begin_create(workspace=ws).result()
    print("Workspace creado.")