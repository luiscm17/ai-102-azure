import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

token = os.environ["GITHUB_TOKEN"]
endpoint = os.environ["GITHUB_ENDPOINT"]
model = os.environ["GITHUB_MODEL"]

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    model=model
)

print(response.choices[0].message.content)

