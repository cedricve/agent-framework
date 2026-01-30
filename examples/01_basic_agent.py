
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

async def main():
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

    # Managed Identity example:
    # Works in Azure App Service, Azure Functions, AKS, VMs, etc.
    #token_provider = get_bearer_token_provider(
    #    ManagedIdentityCredential(),
    #    "https://cognitiveservices.azure.com/.default"
    #)

    # Service Principal example:
    # Work in local development and production environments.
    #credential = ClientSecretCredential(
    #    tenant_id=os.getenv("AZURE_TENANT_ID"),
    #    client_id=os.getenv("AZURE_CLIENT_ID"),
    #    client_secret=os.getenv("AZURE_CLIENT_SECRET")  # Store in Key Vault or secrets manager
    #)
    #token_provider = get_bearer_token_provider(
    #    credential,
    #    "https://cognitiveservices.azure.com/.default"
    #)

    # DefaultAzureCredential example:
    # Works in local development and production environments.
    # 1. Environment variables (service principal)
    # 2. Workload Identity (Kubernetes)
    # 3. Managed Identity (Azure services)
    # 4. Azure CLI (local dev)
    # 5. Azure PowerShell
    # 6. Interactive browser login
    #token_provider = get_bearer_token_provider(
    #    DefaultAzureCredential(),
    #    "https://cognitiveservices.azure.com/.default"
    #)

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

    # Ask a sample question (this is just illustrative; actual implementation may vary)
    response = await agent.run("What is the new Microsoft Framework about?")
    print("Agent response:", response)

    # Ask a question using the tool
    response_with_tool = await agent.run("What's the weather in New York?")
    print("Agent response with tool:", response_with_tool)

    # Buy tickets using the tool
    response_buy_tickets = await agent.run("Buy 2 tickets for the concert of Coldplay.")
    print("Agent response for buying tickets:", response_buy_tickets)

if __name__ == "__main__":
    asyncio.run(main())

    