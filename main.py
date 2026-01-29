
import os
import asyncio
from azure.identity import AzureCliCredential, get_bearer_token_provider
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

# Set environment variables for printing
os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
os.environ["AZURE_OPENAI_DEPLOYMENT"] = deployment
os.environ["AZURE_OPENAI_API_VERSION"] = api_version


async def main():
    print("This is the main entry point of the application.")
    print("Environment variables for Azure OpenAI have been set.")
    print(f"Endpoint: {os.environ['AZURE_OPENAI_ENDPOINT']}")
    print(f"Deployment: {os.environ['AZURE_OPENAI_DEPLOYMENT']}")
    print(f"API Version: {os.environ['AZURE_OPENAI_API_VERSION']}")
    
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
        instructions="You are a helpful assistant.",
        name="AzureOpenAIChatAgent"
    )
    # Further implementation would go here. 
    print("ChatAgent initialized.")

    # Ask a sample question (this is just illustrative; actual implementation may vary)
    response = await agent.run("What is the new Microsoft Framework about?")
    print("Agent response:", response)


if __name__ == "__main__":
    asyncio.run(main())