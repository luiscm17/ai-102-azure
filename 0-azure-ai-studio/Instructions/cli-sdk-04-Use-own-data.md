---
lab:
    title: "Create a generative AI app that uses your own data with Azure CLI and SDK"
    description: "Learn how to use the Azure CLI to provision an Azure AI Foundry hub, project, and models, and the Azure SDK for Python to build a Retrieval Augmented Generation (RAG) chat app that grounds prompts using your own data."
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique for building applications that integrate custom data sources into prompts for generative AI models. This lab, designed for the **AI-102: Designing and Implementing a Microsoft Azure AI Solution** certification, uses the **Azure CLI** to provision an Azure AI Foundry hub, project, and models, and the **Azure SDK for Python** to manage data and implement a RAG-based chat app with the provided `rag-app.py`.

> **Note**: The code uses the latest Azure CLI (2.63.0) and Azure SDK for Python libraries as of August 2025: `azure-mgmt-search==9.2.0`, `azure-search-documents==11.5.3`, `openai==1.51.0`. Check [Azure CLI Releases](https://learn.microsoft.com/en-us/cli/azure/release-notes-azure-cli) and [Azure SDK Releases](https://azure.github.io/azure-sdk-for-python/releases.html) for updates.

This exercise takes approximately **45** minutes.

## Prerequisites

- An Azure subscription with **Owner** role access.
- Python 3.9 or later installed.
- Azure CLI 2.63.0 installed ([Installation Guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)).
- A local folder to store lab files and data.
- Familiarity with Azure CLI and Python SDK authentication (e.g., `DefaultAzureCredential`).

## Setup Your Development Environment

1. Install and authenticate the Azure CLI:

    ```bash
    az login
    ```

2. Create a local folder and set up a Python virtual environment:

    ```bash
    mkdir ai102-rag-lab
    cd ai102-rag-lab
    python -m venv labenv
    source labenv/bin/activate  # Linux/macOS
    labenv\Scripts\activate      # Windows
    ```

3. Create a `requirements.txt` file with the following content:

    ```text
    azure-identity==1.18.0
    azure-mgmt-resource==23.1.1
    azure-mgmt-search==9.2.0
    azure-search-documents==11.5.3
    openai==1.51.0
    python-dotenv==1.0.1
    azure-storage-blob==12.23.1
    ```

4. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

    **Explanation**:
    - `azure-identity`: Handles authentication.
    - `azure-mgmt-resource`: Manages resource groups.
    - `azure-mgmt-search`: Creates Azure AI Search services.
    - `azure-search-documents`: Interacts with search indexes.
    - `openai`: Provides access to Azure OpenAI models.
    - `python-dotenv`: Loads environment variables.
    - `azure-storage-blob`: Manages blob storage for data uploads.

    **Documentation**: [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python), [PyPI: azure-search-documents](https://pypi.org/project/azure-search-documents/)

5. Create a `.env` file:

    ```bash
    touch .env  # Linux/macOS
    type nul > .env  # Windows
    ```

    Add the following content:

    ```env
    OPEN_AI_ENDPOINT=https://your-openai-resource.openai.azure.com/
    OPEN_AI_KEY=your-openai-api-key
    CHAT_MODEL=gpt-4o
    EMBEDDING_MODEL=text-embedding-ada-002
    SEARCH_ENDPOINT=https://your-search-service.search.windows.net
    SEARCH_KEY=your-search-api-key
    INDEX_NAME=brochures-index
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    AZURE_RESOURCE_GROUP=rg-rag-openai-lab
    AZURE_LOCATION=eastus2
    AZURE_AI_HUB_NAME=ragapp-hub-sdk-cli
    AZURE_AI_PROJECT_NAME=ragapp-pj-sdk-cli
    ```

## Create an Azure AI Foundry Hub and Project

Create an Azure AI Foundry hub, an Azure AI Services resource, and a hub-based project using the Azure CLI.

1. Create a resource group:

    ```bash
    az group create --name $AZURE_RESOURCE_GROUP --location $AZURE_LOCATION
    ```

    Replace `$AZURE_RESOURCE_GROUP` and `$AZURE_LOCATION` with the values from your `.env` file (e.g., `ai102-rag-group` and `eastus2`).

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

5. Retrieve the Azure AI Services endpoint and key, and update `.env`:

    ```bash
    AI_SERVICES_NAME="${AZURE_AI_HUB_NAME}-aiservices"
    OPEN_AI_ENDPOINT=$(az cognitiveservices account show --name $AI_SERVICES_NAME --resource-group $AZURE_RESOURCE_GROUP --query properties.endpoint -o tsv)
    OPEN_AI_KEY=$(az cognitiveservices account keys list --name $AI_SERVICES_NAME --resource-group $AZURE_RESOURCE_GROUP --query key1 -o tsv)
    cat > .env << EOF
    OPEN_AI_ENDPOINT=$OPEN_AI_ENDPOINT
    OPEN_AI_KEY=$OPEN_AI_KEY
    CHAT_MODEL=$CHAT_MODEL
    EMBEDDING_MODEL=$EMBEDDING_MODEL
    SEARCH_ENDPOINT=$SEARCH_ENDPOINT
    SEARCH_KEY=$SEARCH_KEY
    INDEX_NAME=$INDEX_NAME
    AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID
    AZURE_RESOURCE_GROUP=$AZURE_RESOURCE_GROUP
    AZURE_LOCATION=$AZURE_LOCATION
    AZURE_AI_HUB_NAME=$AZURE_AI_HUB_NAME
    AZURE_AI_PROJECT_NAME=$AZURE_AI_PROJECT_NAME
    EOF
    ```

    **Explanation**:
    - Retrieves the endpoint and key using `az cognitiveservices account show` and `az cognitiveservices account keys list`.
    - Updates `.env` with the retrieved values, preserving other variables.

    **Documentation**: [az ml workspace](https://learn.microsoft.com/en-us/cli/azure/ml/workspace?view=azure-cli-latest), [az cognitiveservices account](https://learn.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest)

## Deploy Models

Deploy `text-embedding-ada-002` and `gpt-4o` models using the Azure CLI.

1. Create a YAML file for the `text-embedding-ada-002` deployment named `embedding-deployment.yaml`:

    ```bash
    cat > embedding-deployment.yaml << EOF
    name: $EMBEDDING_MODEL
    endpoint_name: $AZURE_AI_HUB_NAME-endpoint
    model:
      name: text-embedding-ada-002
      version: 2
    sku_name: Standard
    sku_capacity: 50
    EOF
    ```

2. Create a YAML file for the `gpt-4o` deployment named `chat-deployment.yaml`:

    ```bash
    cat > chat-deployment.yaml << EOF
    name: $CHAT_MODEL
    endpoint_name: $AZURE_AI_HUB_NAME-endpoint
    model:
      name: gpt-4o
      version: 2024-08-01
    sku_name: Standard
    sku_capacity: 50
    EOF
    ```

3. Create an online endpoint:

    ```bash
    az ml online-endpoint create \
        --name $AZURE_AI_HUB_NAME-endpoint \
        --resource-group $AZURE_RESOURCE_GROUP \
        --workspace-name $AZURE_AI_HUB_NAME
    ```

4. Deploy the models:

    ```bash
    az ml online-deployment create \
        --file embedding-deployment.yaml \
        --resource-group $AZURE_RESOURCE_GROUP \
        --workspace-name $AZURE_AI_HUB_NAME
    az ml online-deployment create \
        --file chat-deployment.yaml \
        --resource-group $AZURE_RESOURCE_GROUP \
        --workspace-name $AZURE_AI_HUB_NAME
    ```

    **Explanation**:
    - Creates an online endpoint using `az ml online-endpoint create`.
    - Deploys `text-embedding-ada-002` and `gpt-4o` using `az ml online-deployment create` with YAML configurations.
    - Sets `sku_capacity: 50` for 50K TPM, aligning with the lab’s requirements.

    **Documentation**: [az ml online-endpoint](https://learn.microsoft.com/en-us/cli/azure/ml/online-endpoint?view=azure-cli-latest), [az ml online-deployment](https://learn.microsoft.com/en-us/cli/azure/ml/online-deployment?view=azure-cli-latest)

## Add Data to Your Project

Upload travel brochures to Azure Blob Storage.

1. Download the [zipped archive of brochures](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) and extract it to a `brochures` folder in `ai102-rag-lab`.

2. Create a script named `upload_data.py`:

    ```bash
    touch upload_data.py  # Linux/macOS
    type nul > upload_data.py  # Windows
    ```

3. Add the following code to `upload_data.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient
    from dotenv import load_dotenv
    import os
    import glob

    # Load environment variables
    load_dotenv()

    # Initialize credentials
    credential = DefaultAzureCredential()
    hub_name = os.getenv("AZURE_AI_HUB_NAME")

    # Get storage account name
    storage_account_name = f"{hub_name}storage"
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=credential
    )

    # Create container
    container_name = "brochures"
    container_client = blob_service_client.create_container(container_name, public_access="none")

    # Upload brochures
    brochure_files = glob.glob("brochures/*.pdf")
    for file_path in brochure_files:
        blob_name = os.path.basename(file_path)
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
        print(f"Uploaded: {blob_name}")
    ```

    **Explanation**:
    - Uses `azure-storage-blob==12.23.1` to upload data to the storage account created with the hub.

    **Documentation**: [azure-storage-blob](https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob?view=azure-python)

4. Run the script:

    ```bash
    python upload_data.py
    ```

## Create an Index for Your Data

Create an Azure AI Search service and index.

1. Create a script named `create_search_index.py`:

    ```bash
    touch create_search_index.py  # Linux/macOS
    type nul > create_search_index.py  # Windows
    ```

2. Add the following code to `create_search_index.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.search import SearchManagementClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SearchField,
        SearchFieldDataType,
        VectorSearch,
        VectorSearchProfile,
        HnswAlgorithmConfiguration
    )
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Initialize credentials and clients
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    search_service_name = os.getenv("AZURE_AI_HUB_NAME") + "search"
    index_name = os.getenv("INDEX_NAME")

    # Create Azure AI Search service
    search_mgmt_client = SearchManagementClient(credential, subscription_id)
    search_service = search_mgmt_client.services.begin_create_or_update(
        resource_group_name=resource_group,
        service_name=search_service_name,
        service={
            "location": os.getenv("AZURE_LOCATION"),
            "sku": {"name": "basic"},
            "properties": {"replica_count": 1, "partition_count": 1}
        }
    ).result()
    print(f"Created search service: {search_service.name}")

    # Create search index with vector search
    search_index_client = SearchIndexClient(
        endpoint=f"https://{search_service_name}.search.windows.net",
        credential=credential
    )
    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True, retrievable=True),
        SearchField(
            name="vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="hnsw-profile"
        )
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw-config")],
        profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw-config")]
    )
    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    index_result = search_index_client.create_or_update_index(index)
    print(f"Created index: {index_result.name}")

    # Save search endpoint and key to .env
    search_key = search_mgmt_client.admin_keys.get(resource_group, search_service_name).primary_key
    with open(".env", "w") as f:
        f.write(f"OPEN_AI_ENDPOINT={os.getenv('OPEN_AI_ENDPOINT')}\n")
        f.write(f"OPEN_AI_KEY={os.getenv('OPEN_AI_KEY')}\n")
        f.write(f"CHAT_MODEL={os.getenv('CHAT_MODEL')}\n")
        f.write(f"EMBEDDING_MODEL={os.getenv('EMBEDDING_MODEL')}\n")
        f.write(f"SEARCH_ENDPOINT=https://{search_service_name}.search.windows.net\n")
        f.write(f"SEARCH_KEY={search_key}\n")
        f.write(f"INDEX_NAME={index_name}\n")
        f.write(f"AZURE_SUBSCRIPTION_ID={subscription_id}\n")
        f.write(f"AZURE_RESOURCE_GROUP={resource_group}\n")
        f.write(f"AZURE_LOCATION={os.getenv('AZURE_LOCATION')}\n")
        f.write(f"AZURE_AI_HUB_NAME={os.getenv('AZURE_AI_HUB_NAME')}\n")
        f.write(f"AZURE_AI_PROJECT_NAME={os.getenv('AZURE_AI_PROJECT_NAME')}\n")
    print("Updated .env with search endpoint and key")
    ```

    **Explanation**:
    - Uses `azure-mgmt-search==9.2.0` and `azure-search-documents==11.5.3` for search service and index creation.

    **Documentation**: [SearchManagementClient.services.begin_create_or_update](https://learn.microsoft.com/en-us/python/api/azure-mgmt-search/azure.mgmt.search.operations.servicesoperations?view=azure-python)

3. Run the script:

    ```bash
    python create_search_index.py
    ```

## Test the Index with a Sample Query

Verify the index with a sample search.

1. Create a script named `test_index.py`:

    ```bash
    touch test_index.py  # Linux/macOS
    type nul > test_index.py  # Windows
    ```

2. Add the following code to `test_index.py`:

    ```python
    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Initialize client
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_key = os.getenv("SEARCH_KEY")
    index_name = os.getenv("INDEX_NAME")
    credential = AzureKeyCredential(search_key)
    search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential)

    # Perform a sample search
    query = "New York accommodations"
    results = search_client.search(search_text=query, query_type="simple")
    for result in results:
        print(f"ID: {result['id']}, Content: {result['content'][:100]}..., Score: {result['@search.score']}")
    ```

    **Explanation**:
    - Uses `azure-search-documents==11.5.3` for search queries.

    **Documentation**: [SearchClient.search](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python)

3. Run the script:

    ```bash
    python test_index.py
    ```

## Create a RAG Client App

Use the provided `rag-app.py`.

1. Create `rag-app.py` with the following content:

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
            open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
            open_ai_key = os.getenv("OPEN_AI_KEY")
            chat_model = os.getenv("CHAT_MODEL")
            embedding_model = os.getenv("EMBEDDING_MODEL")
            search_url = os.getenv("SEARCH_ENDPOINT")
            search_key = os.getenv("SEARCH_KEY")
            index_name = os.getenv("INDEX_NAME")

            # Get an Azure OpenAI chat client
            chat_client = AzureOpenAI(
                api_version="2024-08-01",
                azure_endpoint=open_ai_endpoint,
                api_key=open_ai_key
            )

            # Initialize prompt with system message
            prompt = [
                {"role": "system", "content": "You are a travel assistant that provides information on travel services available from Margie's Travel."}
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

                # Add the user input message to the prompt
                prompt.append({"role": "user", "content": input_text})

                # Additional parameters to apply RAG pattern using the AI Search index
                rag_params = {
                    "data_sources": [
                        {
                            "type": "azure_search",
                            "parameters": {
                                "endpoint": search_url,
                                "index_name": index_name,
                                "authentication": {
                                    "type": "api_key",
                                    "key": search_key,
                                },
                                "query_type": "vector",
                                "embedding_dependency": {
                                    "type": "deployment_name",
                                    "deployment_name": embedding_model,
                                },
                            }
                        }
                    ],
                }

                # Submit the prompt with the data source options and display the response
                response = chat_client.chat.completions.create(
                    model=chat_model,
                    messages=prompt,
                    extra_body=rag_params
                )
                completion = response.choices[0].message.content
                print(completion)

                # Add the response to the chat history
                prompt.append({"role": "assistant", "content": completion})

        except Exception as ex:
            print(ex)

    if __name__ == '__main__':
        main()
    ```

    **Explanation**:
    - Uses `openai==1.51.0` with `api_version="2024-08-01"` for stability.
    - Matches the provided `rag-app.py` structure.

3. Run the chat application:

    ```bash
    python rag-app.py
    ```

4. Enter prompts like `Where should I go on vacation to see architecture?` or `Where can I stay there?`. Enter `quit` to exit.

## Clean Up

Delete resources to avoid costs.

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

## Additional Notes

- **Quota Issues**: Try `AZURE_LOCATION=swedencentral` if quota limits are exceeded.
- **Index Processing**: Wait a few minutes if `test_index.py` returns no results.
- **Troubleshooting**: Use `az --verbose` for detailed CLI output or add `import logging; logging.basicConfig(level=logging.INFO)` to Python scripts for debugging.
- **Responsible AI**: Ensure brochures comply with Azure’s content policies.

**Resources**:

- [Azure AI Foundry Concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
