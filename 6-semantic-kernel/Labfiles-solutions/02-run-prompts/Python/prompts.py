import os
import asyncio
from dotenv import load_dotenv
from openai.types.chat import chat_completion
from semantic_kernel import Kernel
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion, AzureAIInferenceChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.prompt_template import KernelPromptTemplate, HandlebarsPromptTemplate, PromptTemplateConfig

async def main():

    load_dotenv()
    # Set your values in the .env file
    api_key = os.getenv("GITHUB_TOKEN")
    endpoint = os.getenv("GITHUB_ENDPOINT")
    model = os.getenv("GITHUB_MODEL")

    # Create a kernel with Azure OpenAI chat completion
    kernel = Kernel()
    chat_completion = AzureAIInferenceChatCompletion(
        api_key=api_key,
        endpoint=endpoint,
        ai_model_id=model,
    )
    kernel.add_service(chat_completion)

    # Create the chat history
    chat_history = ChatHistory()

    async def get_reply():
        # Get the reply from the chat completion service
        reply = await chat_completion.get_chat_message_content(
            chat_history=chat_history,
            kernel=kernel,
            settings=AzureAIInferenceChatPromptExecutionSettings()
        )
        print("Assistant:", reply)
        chat_history.add_assistant_message(str(reply))

    # Create a semantic kernel prompt template
    sk_prompt_template = KernelPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            You are a helpful career advisor. Based on the user's skillls and interest, suggest up to 3 suitable roles.
            Return the output as JSON in the following format:
            "Role Recomendation":
            {
            "recommendedRoles": [],
            "industries": [],
            "estimatedSalaryRange": ""
            }

            My skills are: {{$skills}}. My interests are: {{$interests}}. What are some roles that would be suitable for me?
            """,
            name= "recommended_roles_prompt",
            template_format="semantic-kernel"
        )
    )
    

    # Render the Semantic Kernel prompt with arguments
    sk_rendered_prompt = await sk_prompt_template.render(
        kernel,
        KernelArguments(
            skills="Software Engineering, C#, Python, Drawing, Guitar, Dance",
            interests="Education, Psychology, Programming, Helping Others"
        )
    )

    # Add the Semantic Kernel prompt to the chat history and get the reply
    chat_history.add_user_message(sk_rendered_prompt)
    await get_reply()

    # Create a handlebars template
    hb_prompt_template = HandlebarsPromptTemplate(
        prompt_template_config=PromptTemplateConfig(
            template="""
            <message role="system">
            Instructions: You are a career advisor. Analyze the skill gap between the user's current skills and the requirements of the target role.
            </message>
            <message role="user">Target Role: {{targetRole}}</message>
            <message role="user">Current Skills: {{currentSkills}}</message>

            <message role="assistant">
            "Skill Gap Analysis":
            {
                "missingSkills": [],
                "coursesToTake": [],
                "certificationSuggestions": []
            }
            </message>
            """,
            name="missing_skills_prompt",
            template_format="handlebars"
        )
    )

    # Render the Handlebars prompt with arguments
    hb_rendered_prompt = await hb_prompt_template.render(
        kernel,
        KernelArguments(
            targetRole="Game Developer",
            currentSkills = "Software Engineering, C#, Python, Drawing, Guitar, Dance"
        )
    )

    # Add the Handlebars prompt to the chat history and get the reply
    chat_history.add_user_message(hb_rendered_prompt)
    await get_reply()

    # Get a follow-up prompt from the user
    print("Assistant: How can I help you?")
    user_input = input("User: ")

    # Add the user input to the chat history and get the reply
    chat_history.add_user_message(user_input)
    await get_reply()


if __name__ == "__main__":
        asyncio.run(main())