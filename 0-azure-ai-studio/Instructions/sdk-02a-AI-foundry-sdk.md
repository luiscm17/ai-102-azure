---
lab:
    title: "Create a generative AI chat app with Azure SDK for Python"
    description: "Learn how to use the Azure Machine Learning SDK to provision an Azure AI Foundry hub, project, and model, and build a chat app that connects to a language model."
---

# Create a generative AI chat app

In this exercise, you use the Azure Machine Learning SDK for Python to create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model, then build a simple chat app that connects to the model using the Azure OpenAI SDK.

> **Note**: The code uses the latest stable Azure SDK for Python libraries as of August 2025: `azure-ai-ml==1.21.0`, `openai==1.51.0`. Check [Azure SDK Releases](https://azure.github.io/azure-sdk-for-python/releases.html) for updates.

This exercise takes approximately **40** minutes.

## Prerequisites

- An Azure subscription with **Owner** role access.
- Python 3.9 or later installed.
- A local folder to store lab files.
- Familiarity with Python and Azure SDK authentication (e.g., `DefaultAzureCredential`).

## Setup Your Development Environment

1. Create a local folder and set up a Python virtual environment:

    ```bash
    mkdir ai102-chat-lab
    cd ai102-chat-lab
    python -m venv labenv
    source labenv/bin/activate  # Linux/macOS
    labenv\Scripts\activate      # Windows
    ```

2. Create a `requirements.txt` file with the following content:

    ```text
    azure-ai-ml==1.21.0
    azure-identity==1.18.0
    azure-mgmt-resource==23.1.1
    azure-mgmt-cognitiveservices==13.5.0
    openai==1.51.0
    python-dotenv==1.0.1
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

    **Explanation**:
    - `azure-ai-ml`: Manages Azure AI Foundry hubs, projects, and model deployments.
    - `azure-identity`: Handles authentication.
    - `azure-mgmt-resource`: Manages resource groups.
    - `azure-mgmt-cognitiveservices`: Creates Azure AI Services resources.
    - `openai`: Provides access to Azure OpenAI models.
    - `python-dotenv`: Loads environment variables.

    **Documentation**: [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python), [PyPI: azure-ai-ml](https://pypi.org/project/azure-ai-ml/)

4. Create a `.env` file based on `.env.example`:

    ```bash
    touch .env  # Linux/macOS
    type nul > .env  # Windows
    ```

    Add the following content:

    ```env
    AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
    AZURE_OPENAI_API_KEY=your-openai-api-key
    AZURE_OPENAI_MODEL_DEPLOYMENT=gpt-4o
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    AZURE_RESOURCE_GROUP=ai102-chat-group
    AZURE_LOCATION=eastus2
    AZURE_AI_HUB_NAME=ai102-hub
    AZURE_AI_PROJECT_NAME=ai102-project
    ```

## Deploy a Model in an Azure AI Foundry Project

Create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model using the Azure Machine Learning SDK.

1. Create a script named `provision_hub_project_model.py`:

    ```bash
    touch provision_hub_project_model.py  # Linux/macOS
    type nul > provision_hub_project_model.py  # Windows
    ```

2. Add the following code to `provision_hub_project_model.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import Hub, Project, AzureOpenAIModel, AzureOpenAIDeployment
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Initialize credentials and clients
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    location = os.getenv("AZURE_LOCATION")
    hub_name = os.getenv("AZURE_AI_HUB_NAME")
    project_name = os.getenv("AZURE_AI_PROJECT_NAME")
    model_deployment = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")

    # Create resource group
    resource_client = ResourceManagementClient(credential, subscription_id)
    rg_result = resource_client.resource_groups.create_or_update(
        resource_group,
        {"location": location}
    )
    print(f"Created resource group: {rg_result.name}")

    # Create Azure AI Foundry hub
    ml_client = MLClient(credential, subscription_id, resource_group)
    hub = Hub(
        name=hub_name,
        location=location,
        display_name=f"{hub_name} Display",
        resource_group=resource_group
    )
    created_hub = ml_client.workspaces.begin_create(hub).result()
    print(f"Created hub: {created_hub.name}")

    # Create Azure AI Services resource for OpenAI
    cog_client = CognitiveServicesManagementClient(credential, subscription_id)
    ai_services_name = f"{hub_name}-aiservices"
    ai_services_params = {
        "location": location,
        "kind": "OpenAI",
        "sku": {"name": "S0"},
        "properties": {}
    }
    ai_services_result = cog_client.accounts.begin_create(
        resource_group_name=resource_group,
        account_name=ai_services_name,
        account=ai_services_params
    ).result()
    print(f"Created AI Services resource: {ai_services_result.name}")

    # Create hub-based project
    project = Project(
        name=project_name,
        location=location,
        display_name=f"{project_name} Display",
        resource_group=resource_group,
        hub_id=created_hub.id
    )
    created_project = ml_client.workspaces.begin_create(project).result()
    print(f"Created project: {created_project.name}")

    # Deploy gpt-4o model
    model_config = AzureOpenAIModel(
        name="gpt-4o",
        version="2024-08-01"
    )
    deployment = AzureOpenAIDeployment(
        name=model_deployment,
        model=model_config,
        sku_name="Standard",
        sku_capacity=50  # 50K TPM
    )
    deployment_result = ml_client.deployments.begin_create_or_update(deployment).result()
    print(f"Deployed model: {deployment_result.name}")

    # Save AI Services endpoint and key to .env
    ai_services_key = cog_client.accounts.list_keys(resource_group, ai_services_name).key1
    with open(".env", "w") as f:
        f.write(f"AZURE_OPENAI_ENDPOINT=https://{ai_services_name}.openai.azure.com/\n")
        f.write(f"AZURE_OPENAI_API_KEY={ai_services_key}\n")
        f.write(f"AZURE_OPENAI_MODEL_DEPLOYMENT={model_deployment}\n")
        f.write(f"AZURE_SUBSCRIPTION_ID={subscription_id}\n")
        f.write(f"AZURE_RESOURCE_GROUP={resource_group}\n")
        f.write(f"AZURE_LOCATION={location}\n")
        f.write(f"AZURE_AI_HUB_NAME={hub_name}\n")
        f.write(f"AZURE_AI_PROJECT_NAME={project_name}\n")
    print("Updated .env with AI Services endpoint and key")
    ```

    **Explanation**:
    - Creates a resource group using `azure-mgmt-resource`.
    - Creates an Azure AI Foundry hub using `MLClient.workspaces.begin_create` with `Hub` entity, aligning with [Azure AI Foundry concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d).
    - Creates an Azure AI Services resource (`kind: OpenAI`) for model access using `azure-mgmt-cognitiveservices`.
    - Creates a hub-based project using `Project` entity.
    - Deploys the `gpt-4o` model with `AzureOpenAIDeployment`, setting `sku_capacity=50` for 50K TPM.
    - Updates `.env` with the Azure AI Services endpoint and key, aligning with `.env.example`.

    **Documentation**: [MLClient.workspaces.begin_create](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations?view=azure-python), [MLClient.deployments.begin_create_or_update](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.operations.deploymentoperations?view=azure-python)

3. Run the script:

    ```bash
    python provision_hub_project_model.py
    ```

## Create a Client Application to Chat with the Model

Create a chat app using the provided `chat-app.py`, updated to use the Azure OpenAI SDK.

1. Create a script named `chat-app.py`:

    ```bash
    touch chat-app.py  # Linux/macOS
    type nul > chat-app.py  # Windows
    ```

2. Add the following code to `chat-app.py`, based on the provided template:

    ```python
    import os
    from dotenv import load_dotenv
    from openai import AzureOpenAI

    def main(): 
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try: 
            # Get configuration settings 
            load_dotenv()
            openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
            model_deployment = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")

            # Initialize the OpenAI client
            openai_client = AzureOpenAI(
                azure_endpoint=openai_endpoint,
                api_key=openai_api_key,
                api_version="2024-08-01"
            )

            # Initialize prompt with system message
            prompt = [
                {"role": "system", "content": "You are a helpful AI assistant that answers questions."}
            ]

            # Loop until the user types 'quit'
            while True:
                # Get input text
                input_text = input("Enter the prompt (or type 'quit' to exit): ")
                if input_text.lower() == "quit":
                    break
                if len(input_text) == 0:
                    print("Please enter a prompt.")
                    continue
                
                # Get a chat completion
                prompt.append({"role": "user", "content": input_text})
                response = openai_client.chat.completions.create(
                    model=model_deployment,
                    messages=prompt
                )
                completion = response.choices[0].message.content
                print(completion)
                prompt.append({"role": "assistant", "content": completion})

        except Exception as ex:
            print(ex)

    if __name__ == '__main__': 
        main()
    ```

    **Explanation**:
    - Replaces `AIProjectClient` with `AzureOpenAI` from `openai==1.51.0`.
    - Uses `api_version="2024-08-01"` for compatibility with `gpt-4o`.
    - Aligns with `.env.example` variables (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_MODEL_DEPLOYMENT`), removing `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT`.
    - Maintains the provided structure for chat history and user interaction.

    **Documentation**: [AzureOpenAI.chat.completions.create](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)

3. Run the application:

    ```bash
    python chat-app.py
    ```

4. When prompted, enter a question, such as `What is the fastest animal on Earth?`, and review the response. Try follow-up questions like `Where can I see one?` or `Are they endangered?`. Enter `quit` to exit.

    > **Tip**: If the app fails due to rate limits, wait a few seconds and try again. If quota is insufficient, adjust `sku_capacity` in `provision_hub_project_model.py`.

## Clean Up

Delete resources to avoid unnecessary Azure costs.

1. Create a script named `cleanup.py`:

    ```bash
    touch cleanup.py  # Linux/macOS
    type nul > cleanup.py  # Windows
    ```

2. Add the following code to `cleanup.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Initialize credentials and client
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Delete resource group
    resource_client.resource_groups.begin_delete(resource_group).wait()
    print(f"Deleted resource group: {resource_group}")
    ```

    **Documentation**: [ResourceManagementClient.begin_delete](https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcegroups?view=azure-python)

3. Run the script:

    ```bash
    python cleanup.py
    ```

## Summary

In this exercise, you used the Azure Machine Learning SDK to create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model, then built a client application to chat with the model using the Azure OpenAI SDK.

## Additional Notes

- **Quota Issues**: Try `AZURE_LOCATION=swedencentral` if quota limits are exceeded.
- **Troubleshooting**: Add `import logging; logging.basicConfig(level=logging.INFO)` to scripts for debugging.
- **Responsible AI**: Ensure prompts comply with Azure’s content policies.

**Resources**:
- [Azure AI Foundry Concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d)
- [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python)
- [AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)