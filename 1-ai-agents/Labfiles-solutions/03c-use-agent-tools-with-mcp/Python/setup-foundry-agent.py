from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from dotenv import load_dotenv
import os
import subprocess
from pathlib import Path

from openai import project

def validate_environment():
    """Validate required environment variables."""
    required_vars = [
        "AZURE_SUBSCRIPTION_ID", "RESOURCE_GROUP_NAME", "LOCATION",
        "FOUNDRY_RESOURCE_NAME", "FOUNDRY_PROJECT_NAME", "MODEL_DEPLOYMENT_NAME"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def create_resource_group(client, resource_group_name, location):
    """Create or update the resource group."""
    print(f"Creating/Updating resource group: {resource_group_name}...")
    return client.resource_groups.create_or_update(
        resource_group_name=resource_group_name,
        parameters={"location": location}
    )

def create_foundry_resource(client, resource_group_name, resource_name, location):
    """Create the Azure AI Foundry resource."""
    print(f"Creating Azure AI Foundry resource: {resource_name}...")
    return client.accounts.begin_create(
        resource_group_name=resource_group_name,
        account_name=resource_name,
        account={
            "location": location,
            "kind": "AIServices",
            "sku": {"name": "S0"},
            "identity": {"type": "SystemAssigned"},
            "properties": {
                "allowProjectManagement": True,
                "customSubDomainName": resource_name,
                "publicNetworkAccess": "Enabled"
            }
        }
    ).result()

def create_foundry_project(client, resource_group_name, account_name, project_name, location):
    """Create a project within the Foundry resource."""
    print(f"Creating project: {project_name}...")
    return client.projects.begin_create(
        resource_group_name=resource_group_name,
        account_name=account_name,
        project_name=project_name,
        project={
            "location": location,
            "identity": {"type": "SystemAssigned"},
            "properties": {}
        }
    ).result()

def run_deployment_script():
    """Run the model deployment shell script with environment variables."""
    print("Starting model deployment...")
    try:

        script_dir = Path(__file__).parent
        # Set up environment variables
        env = {
            **os.environ,  # Include existing environment
            'FOUNDRY_RESOURCE_NAME': os.getenv('FOUNDRY_RESOURCE_NAME'),
            'RESOURCE_GROUP': os.getenv('RESOURCE_GROUP_NAME'),
            'MODEL_DEPLOYMENT_NAME': os.getenv('MODEL_DEPLOYMENT_NAME'),
            'MODEL_NAME': os.getenv('MODEL_NAME', 'gpt-4.1'),
            'MODEL_VERSION': os.getenv('MODEL_VERSION', '2025-04-14'),
            'MODEL_CAPACITY': os.getenv('MODEL_CAPACITY', '50')
        }
        
        # Run the script
        subprocess.run(
            [str(script_dir / "model-deployment.sh")],
            shell=True,
            env=env,
            check=True,
            text=True
        )
        print("Model deployment completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error during model deployment: {e}")
        raise

def main():
    # Load environment variables
    load_dotenv()
    validate_environment()

    # Initialize clients
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_client = ResourceManagementClient(credential, subscription_id)
    foundry_client = CognitiveServicesManagementClient(
        credential=credential,
        subscription_id=subscription_id,
        api_version="2025-04-01-preview"
    )

    # Create resources
    resource_group = create_resource_group(
        resource_client,
        os.getenv("RESOURCE_GROUP_NAME"),
        os.getenv("LOCATION")
    )

    foundry_resource = create_foundry_resource(
        foundry_client,
        resource_group.name,
        os.getenv("FOUNDRY_RESOURCE_NAME"),
        os.getenv("LOCATION")
    )

    project = create_foundry_project(
        foundry_client,
        resource_group.name,
        foundry_resource.name,
        os.getenv("FOUNDRY_PROJECT_NAME"),
        os.getenv("LOCATION")
    )
    
    # Run the model deployment script
    run_deployment_script()
    # Get the project endpoint
    project_endpoint = f"{foundry_resource.properties.endpoint}/api/projects/{os.getenv('FOUNDRY_PROJECT_NAME')}"
    print("\n" + "="*50)
    print(f"Foundry Project Endpoint: {project_endpoint}")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()