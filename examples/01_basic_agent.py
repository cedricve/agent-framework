"""
Basic Agent Sample - Microsoft Agent Framework

This sample demonstrates:
- Creating an AI agent using Azure OpenAI
- Setting custom instructions for the agent
- Running simple queries and getting responses

Prerequisites:
- Azure OpenAI resource with deployed model
- Azure CLI authentication (run: az login)
- Environment variables configured
"""

import asyncio
import os
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from agent_framework import ChatCompletionAgent


async def main():
    print("=== Microsoft Agent Framework - Basic Agent Sample ===\n")
    
    # Get Azure OpenAI configuration from environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    try:
        # Create Azure OpenAI client with Azure CLI authentication
        token_provider = get_bearer_token_provider(
            AzureCliCredential(),
            "https://cognitiveservices.azure.com/.default"
        )
        
        client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version
        )
        
        # Create an AI agent with custom instructions
        agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            instructions="You are a helpful and friendly assistant that provides clear, concise answers."
        )
        
        # Example 1: Simple question
        print("Example 1: Simple Question")
        print("User: What is the capital of France?")
        response1 = await agent.run("What is the capital of France?")
        print(f"Agent: {response1}\n")
        
        # Example 2: Creative task
        print("Example 2: Creative Task")
        print("User: Tell me a joke about a pirate.")
        response2 = await agent.run("Tell me a joke about a pirate.")
        print(f"Agent: {response2}\n")
        
        # Example 3: Explanation request
        print("Example 3: Explanation Request")
        print("User: Explain quantum computing in simple terms.")
        response3 = await agent.run("Explain quantum computing in simple terms.")
        print(f"Agent: {response3}\n")
        
        print("=== Sample Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set AZURE_OPENAI_ENDPOINT in .env file or environment")
        print("2. Set AZURE_OPENAI_DEPLOYMENT in .env file or environment")
        print("3. Run 'az login' to authenticate with Azure CLI")
        print("4. Verify you have access to the Azure OpenAI resource")


if __name__ == "__main__":
    asyncio.run(main())
