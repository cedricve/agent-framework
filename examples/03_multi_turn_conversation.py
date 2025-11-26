"""
Multi-Turn Conversation Sample - Microsoft Agent Framework

This sample demonstrates:
- Creating and managing agent threads for conversation history
- Maintaining context across multiple turns
- Building interactive chat experiences
- Thread-based state management

Prerequisites:
- Azure OpenAI resource with deployed model
- Azure CLI authentication (run: az login)
- Environment variables configured
"""

import asyncio
import os
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from agent_framework import ChatCompletionAgent, AgentThread


async def main():
    print("=== Microsoft Agent Framework - Multi-Turn Conversation Sample ===\n")
    
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
        
        # Create an AI agent
        agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            instructions="You are a knowledgeable assistant helping with programming questions. Remember context from previous messages."
        )
        
        # Create a thread to maintain conversation state
        thread = AgentThread()
        
        print("Starting a multi-turn conversation about Python programming...\n")
        
        # Turn 1: Initial question
        print("Turn 1:")
        print("User: What are list comprehensions in Python?")
        response1 = await agent.run(
            "What are list comprehensions in Python?",
            thread=thread
        )
        print(f"Agent: {response1}\n")
        
        # Turn 2: Follow-up question (agent should remember context)
        print("Turn 2:")
        print("User: Can you show me an example?")
        response2 = await agent.run(
            "Can you show me an example?",
            thread=thread
        )
        print(f"Agent: {response2}\n")
        
        # Turn 3: Related question building on previous context
        print("Turn 3:")
        print("User: What about nested list comprehensions?")
        response3 = await agent.run(
            "What about nested list comprehensions?",
            thread=thread
        )
        print(f"Agent: {response3}\n")
        
        # Turn 4: Asking about performance
        print("Turn 4:")
        print("User: Are they faster than regular loops?")
        response4 = await agent.run(
            "Are they faster than regular loops?",
            thread=thread
        )
        print(f"Agent: {response4}\n")
        
        # Display thread statistics
        print("=== Thread Statistics ===")
        print(f"Total messages in thread: {len(thread.messages)}")
        print(f"Conversation maintained context across {len(thread.messages) // 2} turns")
        
        print("\n=== Sample Complete ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set environment variables in .env file")
        print("2. Run 'az login' to authenticate")
        print("3. Verify Azure OpenAI resource access")


async def interactive_chat():
    """
    Bonus: Interactive chat mode
    Uncomment the call to this function in __main__ to try it!
    """
    print("=== Interactive Chat Mode ===")
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    token_provider = get_bearer_token_provider(
        AzureCliCredential(),
        "https://cognitiveservices.azure.com/.default"
    )
    
    client = AsyncAzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=api_version
    )
    
    agent = ChatCompletionAgent(
        client=client,
        model=deployment,
        instructions="You are a friendly and helpful assistant."
    )
    
    thread = AgentThread()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        response = await agent.run(user_input, thread=thread)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
    # Uncomment the line below to try interactive chat mode:
    # asyncio.run(interactive_chat())
