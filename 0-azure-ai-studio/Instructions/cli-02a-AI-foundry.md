---
lab:
    title: "Create a generative AI chat app with Azure CLI and SDK"
    description: "Learn how to use the Azure CLI to provision an Azure AI Foundry hub, project, and model, and the Azure OpenAI SDK to build a chat app that connects to a language model."
---

# Create a generative AI chat app

In this exercise, you use the Azure CLI to create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model, then build a simple chat app that connects to the model using the Azure OpenAI SDK.

> **Note**: The code uses Azure CLI 2.63.0 and the latest stable Azure SDK for Python libraries as of August 2025: `openai==1.51.0`. Check [Azure CLI Releases](https://learn.microsoft.com/en-us/cli/azure/release-notes-azure-cli) and [Azure SDK Releases](https://azure.github.io/azure-sdk-for-python/releases.html) for updates.

This exercise takes approximately **40** minutes.

## Prerequisites

- An Azure subscription with **Owner** role access.
- Python 3.9 or later installed.
- Azure CLI 2.63.0 installed ([Installation Guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)).
- A local folder to store lab files.
- Familiarity with Azure CLI and Python SDK authentication (e.g., `DefaultAzureCredential`).

## Setup Your Development Environment

1. Install and authenticate the Azure CLI:

    ```bash
    az login
    ```

2. Create a local folder and set up a Python virtual environment:

    ```bash
    mkdir ai102-chat-lab
    cd ai102-chat-lab
    python -m venv labenv
    source labenv/bin/activate  # Linux/macOS
    labenv\Scripts\activate      # Windows
    ```

3. Create a `requirements.txt` file with the following content:

    ```text
    azure-identity==1.18.0
    azure-mgmt-resource==23.1.1
    azure-mgmt-cognitiveservices==13.5.0
    openai==1.51.0
    python-dotenv==1.0.1
    ```

4. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

    **Explanation**:
    - `azure-identity`: Handles authentication for cleanup.
    - `azure-mgmt-resource`: Manages resource groups for cleanup.
    - `azure-mgmt-cognitiveservices`: Retrieves Azure AI Services keys.
    - `openai`: Provides access to Azure OpenAI models.
    - `python-dotenv`: Loads environment variables.

    **Documentation**: [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python), [PyPI: openai](https://pypi.org/project/openai/)

5. Create a `.env` file based on `.env.example`:

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

Create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model using the Azure CLI.

1. Create a resource group:

    ```bash
    az group create --name $AZURE_RESOURCE_GROUP --location $AZURE_LOCATION
    ```

    Replace `$AZURE_RESOURCE_GROUP` and `$AZURE_LOCATION` with the values from your `.env` file (e.g., `ai102-chat-group` and `eastus2`).

2. Create an Azure AI Foundry hub:

    ```bash
    az ml workspace create \
        --kind hub \
        --name $AZURE_AI_HUB_NAME \
        --resource-group $AZURE_RESOURCE_GROUP \
        --location $AZURE_LOCATION \
        --display-name "${AZURE_AI_HUB_NAME} Display"
    ```

    **Explanation**:
    - Creates a hub using `az ml workspace create` with `--kind hub`, as per [Azure CLI: az ml workspace](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest).
    - The hub automatically provisions dependent resources (Storage, Key Vault, Container Registry, Application Insights).

3. Create an Azure AI Services resource for OpenAI:

    ```bash
    az cognitiveservices account create \
        --name "${AZURE_AI_HUB_NAME}-aiservices" \
        --resource-group $AZURE_RESOURCE_GROUP \
        --location $AZURE_LOCATION \
        --kind OpenAI \
        --sku S0
    ```

    **Explanation**:
    - Creates an Azure AI Services resource for OpenAI model access using `az cognitiveservices account create`.

4. Create a hub-based project:

    ```bash
    az ml workspace create \
        --kind project \
        --name $AZURE_AI_PROJECT_NAME \
        --resource-group $AZURE_RESOURCE_GROUP \
        --location $AZURE_LOCATION \
        --hub-id "/subscriptions/$AZURE_SUBSCRIPTION_ID/resourceGroups/$AZURE_RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$AZURE_AI_HUB_NAME" \
        --display-name "${AZURE_AI_PROJECT_NAME} Display"
    ```

    **Explanation**:
    - Creates a project linked to the hub using `--kind project` and `--hub-id`.

5. Create a YAML file for the `gpt-4o` deployment named `chat-deployment.yaml`:

    ```bash
    cat > chat-deployment.yaml << EOF
    name: $AZURE_OPENAI_MODEL_DEPLOYMENT
    endpoint_name: $AZURE_AI_HUB_NAME-endpoint
    model:
      name: gpt-4o
      version: 2024-08-01
    sku_name: Standard
    sku_capacity: 50
    EOF
    ```

6. Create an online endpoint:

    ```bash
    az ml online-endpoint create \
        --name $AZURE_AI_HUB_NAME-endpoint \
        --resource-group $AZURE_RESOURCE_GROUP \
        --workspace-name $AZURE_AI_HUB_NAME
    ```

7. Deploy the `gpt-4o` model:

    ```bash
    az ml online-deployment create \
        --file chat-deployment.yaml \
        --resource-group $AZURE_RESOURCE_GROUP \
        --workspace-name $AZURE_AI_HUB_NAME
    ```

    **Explanation**:
    - Creates an online endpoint using `az ml online-endpoint create`.
    - Deploys `gpt-4o` using `az ml online-deployment create` with YAML configuration, setting `sku_capacity: 50` for 50K TPM.

8. Retrieve the Azure AI Services endpoint and key, and update `.env`:

    ```bash
    AI_SERVICES_NAME="${AZURE_AI_HUB_NAME}-aiservices"
    AZURE_OPENAI_ENDPOINT=$(az cognitiveservices account show --name $AI_SERVICES_NAME --resource-group $AZURE_RESOURCE_GROUP --query properties.endpoint -o tsv)
    AZURE_OPENAI_API_KEY=$(az cognitiveservices account keys list --name $AI_SERVICES_NAME --resource-group $AZURE_RESOURCE_GROUP --query key1 -o tsv)
    cat > .env << EOF
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY
    AZURE_OPENAI_MODEL_DEPLOYMENT=$AZURE_OPENAI_MODEL_DEPLOYMENT
    AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID
    AZURE_RESOURCE_GROUP=$AZURE_RESOURCE_GROUP
    AZURE_LOCATION=$AZURE_LOCATION
    AZURE_AI_HUB_NAME=$AZURE_AI_HUB_NAME
    AZURE_AI_PROJECT_NAME=$AZURE_AI_PROJECT_NAME
    EOF
    ```

    **Explanation**:
    - Retrieves the endpoint and key using `az cognitiveservices account show` and `az cognitiveservices account keys list`.
    - Updates `.env` with the retrieved values, aligning with `.env.example`.

    **Documentation**: [az ml workspace](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest), [az cognitiveservices account](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest), [az ml online-endpoint](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest), [az ml online-deployment](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest)

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

    > **Tip**: If the app fails due to rate limits, wait a few seconds and try again. If quota is insufficient, adjust `sku_capacity` in `chat-deployment.yaml`.

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

In this exercise, you used the Azure CLI to create an Azure AI Foundry hub, a hub-based project, and deploy the `gpt-4o` model, then built a client application to chat with the model using the Azure OpenAI SDK.

## Additional Notes

- **Quota Issues**: Try `AZURE_LOCATION=swedencentral` if quota limits are exceeded.
- **Troubleshooting**: Use `az --verbose` for detailed CLI output or add `import logging; logging.basicConfig(level=logging.INFO)` to `cleanup.py` for debugging.
- **Responsible AI**: Ensure prompts comply with Azure’s content policies.

**Resources**:
- [Azure AI Foundry Concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)