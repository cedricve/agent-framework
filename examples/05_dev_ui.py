
import os
import asyncio
from azure.identity import AzureCliCredential, get_bearer_token_provider
from agent_framework import ChatAgent, ai_function
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv
from agent_framework.devui import serve

load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

@ai_function
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    print(f"[TOOL CALLED] get_weather(location='{location}')")
    return f"The weather in {location} is sunny."


print("This is the main entry point of the application.")
print("Environment variables for Azure OpenAI have been set.")
print(f"Endpoint: {endpoint}")
print(f"Deployment: {deployment}")
print(f"API Version: {api_version}")

# Create a token provider for Azure AD authentication
token_provider = get_bearer_token_provider(
    AzureCliCredential(),
    "https://cognitiveservices.azure.com/.default"
)

# Create a chat client
chat_client = AzureOpenAIChatClient(
    azure_endpoint=endpoint,
    ad_token_provider=token_provider,
    api_version=api_version,
    deployment_name=deployment
)

# Here you can initialize and run your ChatAgent or other components as needed.
agent = ChatAgent(
    chat_client=chat_client,
    instructions="You are a helpful assistant. If you call a tool, use the provided functions, do not make up responses, just use the responses from the tools as is.",
    name="AzureOpenAIChatAgent",
    tools=[get_weather]
)
# Further implementation would go here. 
print("ChatAgent initialized.")

serve(entities=[agent], auto_open=True)
