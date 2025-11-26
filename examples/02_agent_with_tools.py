"""
Agent with Tools Sample - Microsoft Agent Framework

This sample demonstrates:
- Creating custom function tools for an agent
- Using function decorators and type hints
- Tool invocation during agent execution
- Providing contextual information to the LLM

Prerequisites:
- Azure OpenAI resource with deployed model
- Azure CLI authentication (run: az login)
- Environment variables configured
"""

import asyncio
import os
from typing import Annotated
from datetime import datetime
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from agent_framework import ChatCompletionAgent, function_tool


# Define custom tools using the @function_tool decorator
@function_tool
def get_weather(
    location: Annotated[str, "The city and country, e.g., 'London, UK'"]
) -> str:
    """Get the current weather for a given location."""
    # In a real application, this would call a weather API
    return f"The weather in {location} is sunny with a temperature of 22°C."


@function_tool
def get_current_time(
    timezone: Annotated[str, "The timezone, e.g., 'UTC', 'America/New_York'"] = "UTC"
) -> str:
    """Get the current time in a specific timezone."""
    # Simplified implementation - in production, use proper timezone handling
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"The current time in {timezone} is {current_time}."


@function_tool
def calculate_trip_distance(
    origin: Annotated[str, "The starting city"],
    destination: Annotated[str, "The destination city"]
) -> str:
    """Calculate the distance between two cities."""
    # Mock implementation - in production, use a real distance API
    distances = {
        ("Paris", "London"): 344,
        ("New York", "Los Angeles"): 3944,
        ("Tokyo", "Sydney"): 7823,
    }
    
    key = (origin, destination)
    reverse_key = (destination, origin)
    
    distance = distances.get(key) or distances.get(reverse_key, 1000)
    return f"The distance from {origin} to {destination} is approximately {distance} km."


async def main():
    print("=== Microsoft Agent Framework - Agent with Tools Sample ===\n")
    
    # Get Azure OpenAI configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    try:
        # Create Azure OpenAI client
        token_provider = get_bearer_token_provider(
            AzureCliCredential(),
            "https://cognitiveservices.azure.com/.default"
        )
        
        client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version
        )
        
        # Create an AI agent with custom tools
        agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            instructions="You are a helpful travel assistant. Use the available tools to help users with weather, time, and distance information.",
            tools=[get_weather, get_current_time, calculate_trip_distance]
        )
        
        # Example 1: Weather query
        print("Example 1: Weather Query")
        print("User: What's the weather like in Paris, France?")
        response1 = await agent.run("What's the weather like in Paris, France?")
        print(f"Agent: {response1}\n")
        
        # Example 2: Time query
        print("Example 2: Time Query")
        print("User: What time is it in New York?")
        response2 = await agent.run("What time is it in America/New_York timezone?")
        print(f"Agent: {response2}\n")
        
        # Example 3: Complex query using multiple tools
        print("Example 3: Multi-Tool Query")
        print("User: I'm planning a trip from Paris to London. How far is it and what's the weather in London?")
        response3 = await agent.run(
            "I'm planning a trip from Paris to London. How far is it and what's the weather in London?"
        )
        print(f"Agent: {response3}\n")
        
        print("=== Sample Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set environment variables in .env file")
        print("2. Run 'az login' to authenticate")
        print("3. Verify Azure OpenAI resource access")


if __name__ == "__main__":
    asyncio.run(main())
