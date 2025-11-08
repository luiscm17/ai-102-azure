import os
import asyncio
from dotenv import load_dotenv

# Import namespaces
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion
from semantic_kernel.functions.kernel_arguments import KernelArguments


async def main():

    load_dotenv()
    # Set your values in the .env file
    api_key = os.environ["GITHUB_TOKEN"]
    endpoint = os.environ["GITHUB_ENDPOINT"]
    model = os.environ["GITHUB_MODEL"]


    # Create a kernel with Azure OpenAI chat completion
    kernel = Kernel()
    chat_completion = AzureAIInferenceChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    ai_model_id=model,
    )

    # You can do the following if you have set the necessary environment variables or created a .env file
    kernel.add_service(chat_completion)

    # Test the chat completion service
    response = await kernel.invoke_prompt(
    "Give me a list of 10 breakfast foods with eggs and cheese", 
    KernelArguments())
    print("Assistant > " + str(response))

if __name__ == "__main__":
        asyncio.run(main())