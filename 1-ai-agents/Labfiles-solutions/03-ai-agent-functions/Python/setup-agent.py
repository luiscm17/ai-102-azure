from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ToolSet
import os
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Iniciate the client
agent_client = AgentsClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

# Create a toolset for the agent (we'll add our functions later)
toolset = ToolSet()

# Create the agent
with agent_client:
    agent = agent_client.create_agent(
        model=model_deployment,
        name="support-agent",
        instructions="""You are a technical support agent that helps users with their issues.
        When a user reports a problem, collect their email and a description of the issue.
        Be polite, professional, and helpful at all times.""",
        toolset=toolset
    )
    print(f"Agent created: {agent.name}")