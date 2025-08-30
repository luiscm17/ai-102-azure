---
lab:
    title: "Create a generative AI app that uses your own data with Azure SDK for Python"
    description: "Learn how to use the Azure Machine Learning SDK to provision an Azure AI Foundry hub, project, and models, and build a Retrieval Augmented Generation (RAG) chat app that grounds prompts using your own data."
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique for building applications that integrate custom data sources into prompts for generative AI models. This lab, designed for the **AI-102: Designing and Implementing a Microsoft Azure AI Solution** certification, uses the **Azure Machine Learning SDK for Python** to provision an Azure AI Foundry hub, project, and models, and implement a RAG-based chat app with the provided `rag-app.py`.

> **Note**: The code uses the latest stable Azure SDK for Python libraries as of August 2025: `azure-ai-ml==1.21.0`, `azure-mgmt-search==9.2.0`, `azure-search-documents==11.5.3`, `openai==1.51.0`. Check [Azure SDK Releases](https://azure.github.io/azure-sdk-for-python/releases.html) for updates.

This exercise takes approximately **45** minutes.

## Prerequisites

- An Azure subscription with **Owner** role access.
- Python 3.9 or later installed.
- A local folder to store lab files and data.
- Familiarity with Python and Azure SDK authentication (e.g., `DefaultAzureCredential`).

## Setup Your Development Environment

1. Create a local folder and set up a Python virtual environment:

    ```bash
    mkdir ai102-rag-lab
    cd ai102-rag-lab
    python -m venv labenv
    source labenv/bin/activate  # Linux/macOS
    labenv\Scripts\activate      # Windows
    ```

2. Create a `requirements.txt` file with the following content:

    ```text
    azure-ai-ml==1.21.0
    azure-identity==1.18.0
    azure-mgmt-resource==23.1.1
    azure-mgmt-search==9.2.0
    azure-search-documents==11.5.3
    openai==1.51.0
    python-dotenv==1.0.1
    azure-storage-blob==12.23.1
    ```

3. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

    **Explanation**:
    - `azure-ai-ml`: Manages Azure AI Foundry hubs, projects, and model deployments.
    - `azure-identity`: Handles authentication.
    - `azure-mgmt-resource`: Manages resource groups.
    - `azure-mgmt-search`: Creates Azure AI Search services.
    - `azure-search-documents`: Interacts with search indexes.
    - `openai`: Provides access to Azure OpenAI models.
    - `python-dotenv`: Loads environment variables.
    - `azure-storage-blob`: Manages blob storage for data uploads.

    **Documentation**: [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python), [PyPI: azure-ai-ml](https://pypi.org/project/azure-ai-ml/)

4. Create a `.env` file:

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
    AZURE_RESOURCE_GROUP=ai102-rag-group
    AZURE_LOCATION=eastus2
    AZURE_AI_HUB_NAME=ai102-hub
    AZURE_AI_PROJECT_NAME=ai102-project
    ```

## Create an Azure AI Foundry Hub and Project

1. Create a script named `provision_hub_project.py`:

    ```bash
    touch provision_hub_project.py  # Linux/macOS
    type nul > provision_hub_project.py  # Windows
    ```

2. Add the following code to `provision_hub_project.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import Hub, Project
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
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

    # Save hub endpoint and key to .env
    ai_services_key = cog_client.accounts.list_keys(resource_group, ai_services_name).key1
    with open(".env", "w") as f:
        f.write(f"OPEN_AI_ENDPOINT=https://{ai_services_name}.openai.azure.com/\n")
        f.write(f"OPEN_AI_KEY={ai_services_key}\n")
        f.write(f"CHAT_MODEL={os.getenv('CHAT_MODEL')}\n")
        f.write(f"EMBEDDING_MODEL={os.getenv('EMBEDDING_MODEL')}\n")
        f.write(f"SEARCH_ENDPOINT={os.getenv('SEARCH_ENDPOINT')}\n")
        f.write(f"SEARCH_KEY={os.getenv('SEARCH_KEY')}\n")
        f.write(f"INDEX_NAME={os.getenv('INDEX_NAME')}\n")
        f.write(f"AZURE_SUBSCRIPTION_ID={subscription_id}\n")
        f.write(f"AZURE_RESOURCE_GROUP={resource_group}\n")
        f.write(f"AZURE_LOCATION={location}\n")
        f.write(f"AZURE_AI_HUB_NAME={hub_name}\n")
        f.write(f"AZURE_AI_PROJECT_NAME={project_name}\n")
    print("Updated .env with hub endpoint and key")
    ```

    **Explanation**:
    - Creates a resource group using `azure-mgmt-resource`.
    - Creates an Azure AI Foundry hub using `MLClient.workspaces.begin_create` with `Hub` entity, aligning with [Azure AI Foundry concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d).[](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/create-hub-project-sdk)
    - Creates an Azure AI Services resource (`kind: OpenAI`) for model deployments.
    - Creates a hub-based project linked to the hub using `Project` entity.
    - Saves the Azure AI Services endpoint and key to `.env`.

    **Documentation**: [MLClient.workspaces.begin_create](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations?view=azure-python)

3. Run the script:

    ```bash
    python provision_hub_project.py
    ```

## Deploy Models

Deploy `text-embedding-ada-002` and `gpt-4o` models using the Azure Machine Learning SDK.

1. Create a script named `deploy_models.py`:

    ```bash
    touch deploy_models.py  # Linux/macOS
    type nul > deploy_models.py  # Windows
    ```

2. Add the following code to `deploy_models.py`:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml import MLClient
    from azure.ai.ml.entities import AzureOpenAIModel, AzureOpenAIDeployment
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()

    # Initialize credentials and clients
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    hub_name = os.getenv("AZURE_AI_HUB_NAME")
    chat_model = os.getenv("CHAT_MODEL")
    embedding_model = os.getenv("EMBEDDING_MODEL")

    # Create MLClient
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=hub_name
    )

    # Deploy text-embedding-ada-002
    embedding_model_config = AzureOpenAIModel(
        name="text-embedding-ada-002",
        version="2"
    )
    embedding_deployment = AzureOpenAIDeployment(
        name=embedding_model,
        model=embedding_model_config,
        sku_name="Standard",
        sku_capacity=50  # 50K TPM
    )
    embedding_result = ml_client.deployments.begin_create_or_update(embedding_deployment).result()
    print(f"Deployed model: {embedding_result.name}")

    # Deploy gpt-4o
    chat_model_config = AzureOpenAIModel(
        name="gpt-4o",
        version="2024-08-01"
    )
    chat_deployment = AzureOpenAIDeployment(
        name=chat_model,
        model=chat_model_config,
        sku_name="Standard",
        sku_capacity=50  # 50K TPM
    )
    chat_result = ml_client.deployments.begin_create_or_update(chat_deployment).result()
    print(f"Deployed model: {chat_result.name}")
    ```

    **Explanation**:
    - Uses `azure-ai-ml==1.21.0` to deploy models, replacing portal-based deployment.
    - Configures `text-embedding-ada-002` and `gpt-4o` with stable version `2024-08-01`.

    **Documentation**: [MLClient.deployments.begin_create_or_update](https://learn.microsoft.com/en-us/python/api/azure-ai-ml/azure.ai.ml.operations.deploymentoperations?view=azure-python)

3. Run the script:

    ```bash
    python deploy_models.py
    ```

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
    - Sets `public_access="none"` for security.

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
    - Configures vector search for compatibility with `text-embedding-ada-002`.

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
- **Troubleshooting**: Add `import logging; logging.basicConfig(level=logging.INFO)` to scripts for debugging.
- **Responsible AI**: Ensure brochures comply with Azure’s content policies.

**Resources**:

- [Azure AI Foundry Concepts](https://ai.azure.com/doc/azure/ai-foundry/concepts/ai-resources?tid=a15fc6ea-74f6-4722-83ac-9342d69e223d)
- [Azure SDK for Python](https://azure.github.io/azure-sdk-for-python)
- [AI-102 Training](https://learn.microsoft.com/en-us/training/courses/ai-102t00)
