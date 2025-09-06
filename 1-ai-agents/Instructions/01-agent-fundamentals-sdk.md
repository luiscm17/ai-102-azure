---
lab:
    title: 'Explore AI Agent development'
    description: 'Take your first steps in developing AI agents by using the Azure AI Agents Python SDK to create a simple AI agent that assists employees with expense claims.'
---

# Explore AI Agent development

In this exercise, you use the Azure AI Agents Python SDK to create a simple AI agent that assists employees with expense claims, replacing the Azure AI Foundry portal-based workflow with programmatic steps. The lab covers creating a `.env` file for configuration, provisioning a resource group, an Azure AI Foundry resource, a project, deploying the `gpt-5-mini` model, configuring an agent with a vector store and code interpreter, and testing it programmatically. You’ll also use Azure CLI to retrieve necessary endpoints and API keys.

This exercise takes approximately **30** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors. Ensure you have sufficient permissions (Owner or Contributor role at the subscription scope, and Azure AI User role at the project scope) and model quota in your chosen region.

## Prerequisites

- An Azure subscription with Owner or Contributor role permissions.
- Python 3.9 or later installed.
- Azure CLI 2.63.0 installed ([Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)).
- The `Expenses_Policy.docx` document downloaded from [GitHub](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-agent-fundamentals/Expenses_Policy.docx) and saved locally.
- Required Python packages installed in a virtual environment:

  ```bash
  pip install azure-identity azure-mgmt-resource azure-ai-projects==1.0.0b11 python-dotenv
  ```

## Create a .env file for configuration

To follow best practices, you’ll store configuration settings in a `.env` file. You must create this file manually and populate it with environment variables.

1. Create a file named `.env` in a working directory (e.g., `agent-workshop`) using a text editor.

2. Add the following line to the `.env` file, replacing `your-subscription-id` with your Azure subscription ID (find it with `az account show --query id -o tsv`):

    ```bash
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    ```

    > **Note**: The `.env` file will be updated later with the Azure AI Foundry resource endpoint and API key after provisioning the resource.

3. Save the `.env` file in the same directory where you’ll run the Python scripts, alongside the `Expenses_Policy.docx` file.

## Create an Azure AI Foundry project and agent

Let's provision the necessary Azure resources and create an AI agent using the Azure AI Agents Python SDK. You’ll create a resource group, an Azure AI Foundry resource, deploy the `gpt-5-mini` model, create a vector store, and configure an agent programmatically.

1. **Provision a resource group**:

   A resource group is a logical container for Azure resources, enabling organized management and cleanup. For this lab, you’ll create a resource group named `rg-agent-workshop` in the `eastus2` region, which supports Azure AI Foundry resources.

   Create a Python file named `create_resource_group.py` in your working directory and add the following code:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    RESOURCE_GROUP = "rg-agent-workshop"
    LOCATION = "eastus2"

    # Authenticate
    credential = DefaultAzureCredential()

    # Create resource group
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    print(f"Creating resource group {RESOURCE_GROUP}...")
    resource_client.resource_groups.create_or_update(
        RESOURCE_GROUP,
        {"location": LOCATION}
    )
    print(f"Resource group {RESOURCE_GROUP} created successfully.")
    ```

   Run the script:

    ```bash
    python create_resource_group.py
    ```

    **Purpose and Characteristics**:
    - **Purpose**: The resource group (`rg-agent-workshop`) organizes all resources for this lab, ensuring they can be managed and deleted together. It’s essential for AI-102 labs to maintain clean resource allocation.
    - **Characteristics**: Located in `eastus2`, a region supporting Azure AI Foundry resources. Uses the `Standard` tier implicitly. No additional cost is incurred for the resource group itself, only for resources within it.
    - **Relevance**: Aligns with AI-102 objectives for resource management and provisioning.

2. **Provision an Azure AI Foundry resource**:

   The Azure AI Foundry resource (an AI Services account) provides access to the model catalog and agent services, serving as the foundation for hosting projects and model deployments.

   Create a Python file named `create_foundry_resource.py` and add the following code:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    RESOURCE_GROUP = "rg-agent-workshop"
    LOCATION = "eastus2"
    AI_FOUNDRY_RESOURCE_NAME = "ai102-foundry"

    # Authenticate
    credential = DefaultAzureCredential()

    # Create Azure AI Foundry resource
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    print(f"Creating Azure AI Foundry resource {AI_FOUNDRY_RESOURCE_NAME}...")
    resource_client.resources.begin_create_or_update(
        resource_group_name=RESOURCE_GROUP,
        resource_provider_namespace="Microsoft.CognitiveServices",
        parent_resource_path="",
        resource_type="accounts",
        resource_name=AI_FOUNDRY_RESOURCE_NAME,
        parameters={
            "kind": "AIServices",
            "location": LOCATION,
            "sku": {"name": "S0"},
            "properties": {}
        },
        api_version="2023-05-01"
    ).result()
    print(f"Azure AI Foundry resource {AI_FOUNDRY_RESOURCE_NAME} created successfully.")
    ```

   Run the script:

    ```bash
    python create_foundry_resource.py
    ```

    **Purpose and Characteristics**:
    - **Purpose**: The AI Services account (`ai102-foundry`) enables access to Azure AI Foundry’s model catalog (e.g., `gpt-5-mini`) and agent services, serving as the backend for projects and deployments. It’s critical for hosting AI agents in AI-102 labs.
    - **Characteristics**: Uses the `S0` SKU (standard tier) for scalability and supports multiple model deployments. Located in `eastus2` for compatibility with AI Foundry resources. Provides an endpoint for API access and supports keyless authentication.
    - **Relevance**: Supports AI-102 objectives for deploying and managing AI services programmatically.

3. **Retrieve endpoint and API key for the Azure AI Foundry resource**:

   To interact with the AI Foundry resource, you need its endpoint and API key, which will be stored in the `.env` file.

   Run the following Azure CLI commands to retrieve the endpoint and API key, replacing `rg-agent-workshop` and `ai102-foundry` with your resource group and AI Foundry resource names:

    ```bash
    # Retrieve endpoint
    az cognitiveservices account show \
      --resource-group rg-agent-workshop \
      --name ai102-foundry \
      --query properties.endpoint -o tsv > endpoint.txt

    # Retrieve API key
    az cognitiveservices account keys list \
      --resource-group rg-agent-workshop \
      --name ai102-foundry \
      --query key1 -o tsv > apikey.txt
    ```

   Open the `.env` file and append the endpoint and API key from the output files:

    ```bash
    echo "AI_FOUNDRY_ENDPOINT=$(cat endpoint.txt)" >> .env
    echo "AI_FOUNDRY_API_KEY=$(cat apikey.txt)" >> .env
    rm endpoint.txt apikey.txt
    ```

    Your `.env` file should now include:

    ```bash
    AZURE_SUBSCRIPTION_ID=your-subscription-id
    AI_FOUNDRY_ENDPOINT=https://ai102-foundry.cognitiveservices.azure.com/
    AI_FOUNDRY_API_KEY=your-api-key
    ```

    > **Note**: This step ensures secure storage of credentials in the `.env` file, following best practices for environment variable management. In the original lab, this information was obtained via the portal, as shown in the screenshots.

4. **Provision a model deployment**:

   Deploy the `gpt-5-mini` model to the AI Foundry resource to provide the AI capabilities for the agent, using the **Standard deployment in Azure AI Foundry resources** option for global processing and content filtering.

    ```bash
    az cognitiveservices account deployment create \
        --name agent-foundry-lab1 \
        --resource-group rg-agent-workshop \
        --deployment-name gpt5mini-deployment \
        --model-name gpt-5-mini \
        --model-version "2025-08-07" \
        --model-format OpenAI \
        --sku-name GlobalStandard \
        --sku-capacity 50
    ```

    **Purpose and Characteristics**:
    - **Purpose**: The `gpt-5-mini` model deployment provides the AI processing power for the agent, enabling natural language understanding, generation, and tool interactions. It’s deployed using the **Standard deployment** option, which supports global processing, content filtering, and keyless authentication.
    - **Characteristics**: Uses the `GlobalStandard` SKU with a capacity of 50 (equivalent to ~50K TPM, adjusted for lab needs). The `gpt-5-mini` model is a lightweight, efficient model optimized for generative AI tasks. Deployed within the project for seamless integration with agents.
    - **Relevance**: Essential for AI-102 objectives related to deploying and managing AI models for generative AI applications, aligning with Azure AI Foundry’s model catalog.

5. **Create the Azure AI Foundry project and agent**:

   The project organizes agent-related resources, and the agent (`ExpensesAgent`) uses the deployed model, a vector store, and a code interpreter tool.

   Create a Python file named `configure_agent.py` and add the following code:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.agents import AgentsClient, CodeInterpreterToolDefinition
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()
    AI_FOUNDRY_RESOURCE_NAME = "ai102-foundry"
    PROJECT_NAME = "ai102-project"
    MODEL_DEPLOYMENT_NAME = "gpt-5-mini"
    AGENT_NAME = "ExpensesAgent"
    VECTOR_STORE_NAME = "Expenses_Vector_Store"
    DOC_PATH = "Expenses_Policy.docx"

    # Initialize project client
    project_endpoint = f"https://{AI_FOUNDRY_RESOURCE_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}"
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=credential
    )

    # Create vector store and upload document
    print(f"Creating vector store {VECTOR_STORE_NAME}...")
    vector_store = project_client.datasets.create_vector_store(VECTOR_STORE_NAME)
    with open(DOC_PATH, "rb") as doc_file:
        project_client.datasets.upload_file(
            vector_store_name=VECTOR_STORE_NAME,
            file_name="Expenses_Policy.docx",
            file_content=doc_file.read()
        )

    # Create agent
    agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=credential
    )
    print(f"Creating agent {AGENT_NAME}...")
    agent = agents_client.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name=AGENT_NAME,
        instructions="""You are an AI assistant for corporate expenses.

        You answer questions about expenses based on the expenses policy data.
        If a user wants to submit an expense claim, you get their email address, a description of the claim, and the amount to be claimed and write the claim details to a text file that the user can download.""",
        tools=[CodeInterpreterToolDefinition()],
        tool_resources={"vector_store": {"ids": [vector_store.id]}}
    )
    print("Agent created successfully.")
    ```

   Run the script:

    ```bash
    python configure_agent.py
    ```

    **Purpose and Characteristics**:

    - **Purpose (Project)**: The project (`ai102-project`) is a logical container within the AI Foundry resource, organizing agent-related resources like vector stores and agents. It enables structured development of AI solutions.
    - **Purpose (Vector Store)**: The vector store (`Expenses_Vector_Store`) stores the `Expenses_Policy.docx` file, enabling the agent to ground its responses in the document’s content for accurate answers (RAG-like workflow).
    - **Purpose (Agent)**: The `ExpensesAgent` uses the `gpt-5-mini` model to answer expense-related questions and process claims, leveraging the vector store for knowledge and the code interpreter for generating text files.
    - **Characteristics**: The project uses the AI Foundry resource’s endpoint. The vector store supports document-based grounding. The agent is configured with specific instructions and the code interpreter tool, which executes Python code for tasks like file generation.
    - **Relevance**: Aligns with AI-102 objectives for creating and managing AI agents, integrating knowledge sources, and using tools for advanced functionality.

## Test your agent

Now that you’ve created the agent programmatically, you can test it using the Python SDK to simulate the playground chat functionality.

1. Create a Python file named `test_agent.py` to test the agent’s responses to expense-related queries and claim submission:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.ai.agents import AgentsClient, MessageRole
    from dotenv import load_dotenv
    import os
    import time

    # Load environment variables
    load_dotenv()
    AI_FOUNDRY_RESOURCE_NAME = "ai102-foundry"
    PROJECT_NAME = "ai102-project"
    AGENT_NAME = "ExpensesAgent"

    # Initialize agents client
    project_endpoint = f"https://{AI_FOUNDRY_RESOURCE_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}"
    credential = DefaultAzureCredential()
    agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=credential
    )

    # Get agent ID
    agents = agents_client.list_agents()
    agent_id = next(agent.id for agent in agents if agent.name == AGENT_NAME)

    # Create a thread and test the agent
    print("Testing the agent...")
    thread = agents_client.create_thread()

    # Test 1: Query about meal claim limits
    agents_client.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="What's the maximum I can claim for meals?"
    )
    run = agents_client.create_thread_and_run(
        agent_id=agent_id,
        thread={"id": thread.id}
    )

    # Poll for run completion
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(2)
        run = agents_client.get_run(thread_id=thread.id, run_id=run.id)

    # Retrieve and print messages
    messages = agents_client.get_messages(thread_id=thread.id)
    for message in messages:
        for content in message.content:
            if content.type == "text":
                print(f"[{message.role}]: {content.text}")

    # Test 2: Submit an expense claim
    agents_client.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="I'd like to submit a claim for a meal."
    )
    agents_client.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="Email: fred@contoso.com"
    )
    agents_client.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="Breakfast cost me $20"
    )
    run = agents_client.create_thread_and_run(
        agent_id=agent_id,
        thread={"id": thread.id}
    )

    # Poll for run completion
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(2)
        run = agents_client.get_run(thread_id=thread.id, run_id=run.id)

    # Retrieve and download the expense claim file
    messages = agents_client.get_messages(thread_id=thread.id)
    for message in messages:
        for content in message.content:
            if content.type == "file":
                file_content = agents_client.get_file_content(content.file_id)
                with open(f"expense_claim_{content.file_id}.txt", "wb") as f:
                    f.write(file_content)
                print(f"Downloaded expense claim to expense_claim_{content.file_id}.txt")

    print("Agent testing completed.")
    ```

2. Run the script to test the agent:

    ```bash
    python test_agent.py
    ```

    > **Note**: This step replaces the playground chat interface shown in the original lab’s screenshot. The script sends queries to the agent, retrieves responses, and downloads the expense claim file. If the agent fails to respond due to rate limits, wait a few seconds and retry. If quota issues persist, consider switching regions (e.g., `swedencentral`) or adjusting the `capacity` in `deploy_model.py`.

    The script tests the agent’s ability to answer questions based on the expenses policy (e.g., maximum meal claim) and process an expense claim by generating a downloadable text file, mirroring the original lab’s functionality.

## Clean up

Now that you’ve finished the exercise, you should delete the cloud resources to avoid unnecessary costs.

1. Create a Python file named `cleanup.py` to delete all resources:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.ai.projects import AIProjectClient
    from azure.ai.agents import AgentsClient
    from dotenv import load_dotenv
    import os

    # Load environment variables
    load_dotenv()
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    RESOURCE_GROUP = "rg-agent-workshop"
    AI_FOUNDRY_RESOURCE_NAME = "ai102-foundry"
    PROJECT_NAME = "ai102-project"
    AGENT_NAME = "ExpensesAgent"
    VECTOR_STORE_NAME = "Expenses_Vector_Store"

    # Authenticate
    credential = DefaultAzureCredential()

    # Initialize clients
    project_endpoint = f"https://{AI_FOUNDRY_RESOURCE_NAME}.services.ai.azure.com/api/projects/{PROJECT_NAME}"
    agents_client = AgentsClient(endpoint=project_endpoint, credential=credential)
    project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

    # Delete agent and threads
    print("Deleting agent and threads...")
    agents = agents_client.list_agents()
    agent_id = next((agent.id for agent in agents if agent.name == AGENT_NAME), None)
    if agent_id:
        agents_client.delete_agent(agent_id)
    threads = agents_client.list_threads()
    for thread in threads:
        agents_client.delete_thread(thread.id)

    # Delete vector store
    print(f"Deleting vector store {VECTOR_STORE_NAME}...")
    project_client.datasets.delete_vector_store(VECTOR_STORE_NAME)

    # Delete model deployment
    print(f"Deleting model deployment gpt-5-mini...")
    project_client.models.begin_delete_deployment("gpt-5-mini").wait()

    # Delete AI Foundry resource
    print(f"Deleting Azure AI Foundry resource {AI_FOUNDRY_RESOURCE_NAME}...")
    resource_client.resources.begin_delete(
        resource_group_name=RESOURCE_GROUP,
        resource_provider_namespace="Microsoft.CognitiveServices",
        parent_resource_path="",
        resource_type="accounts",
        resource_name=AI_FOUNDRY_RESOURCE_NAME,
        api_version="2023-05-01"
    ).wait()

    # Delete resource group
    print(f"Deleting resource group {RESOURCE_GROUP}...")
    resource_client.resource_groups.begin_delete(RESOURCE_GROUP).wait()

    print("Cleanup completed.")
    ```

2. Run the script to delete resources:

    ```bash
    python cleanup.py
    ```

    > **Note**: This step replaces the portal-based resource group deletion shown in the original lab. The script deletes the agent, threads, vector store, model deployment, AI Foundry resource, and resource group, ensuring no resources remain.

## Next steps

Learn about additional tools to extend your agents' capabilities, such as web search or custom functions, in the [Azure AI Foundry Agents documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/).
