"""
Workflow Example - Microsoft Agent Framework

This sample demonstrates:
- Creating multi-agent workflows
- Orchestrating multiple specialized agents
- Sequential execution patterns
- Agent handoffs and collaboration

Prerequisites:
- Azure OpenAI resource with deployed model
- Azure CLI authentication (run: az login)
- Environment variables configured
"""

import asyncio
import os
from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from agent_framework import ChatCompletionAgent, Workflow, function_tool


# Define tools for the research agent
@function_tool
def search_web(query: str) -> str:
    """Search the web for information."""
    # Mock implementation
    return f"Search results for '{query}': Found relevant articles about the topic."


@function_tool
def get_statistics(topic: str) -> str:
    """Get statistical data about a topic."""
    # Mock implementation
    return f"Statistics for {topic}: Market size $5B, Growth rate 15% YoY"


async def main():
    print("=== Microsoft Agent Framework - Workflow Example ===\n")
    
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
        
        print("Creating specialized agents for the workflow...\n")
        
        # Agent 1: Research Agent - Gathers information
        research_agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            name="ResearchAgent",
            instructions="""You are a research specialist. Your job is to gather information 
            about topics using available tools. Provide comprehensive research summaries.""",
            tools=[search_web, get_statistics]
        )
        
        # Agent 2: Analysis Agent - Analyzes the research
        analysis_agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            name="AnalysisAgent",
            instructions="""You are a data analyst. Review research findings and provide 
            detailed analysis with insights, trends, and recommendations."""
        )
        
        # Agent 3: Writing Agent - Creates final report
        writing_agent = ChatCompletionAgent(
            client=client,
            model=deployment,
            name="WritingAgent",
            instructions="""You are a professional writer. Transform analysis into clear, 
            well-structured reports suitable for business audiences."""
        )
        
        # Create a workflow with sequential execution
        print("Building workflow: Research → Analysis → Writing\n")
        
        workflow = Workflow()
        
        # Add agents to the workflow in sequence
        workflow.add_agent(research_agent)
        workflow.add_agent(analysis_agent)
        workflow.add_agent(writing_agent)
        
        # Define the execution flow
        workflow.add_edge(research_agent, analysis_agent)
        workflow.add_edge(analysis_agent, writing_agent)
        
        # Execute the workflow
        topic = "AI Agent Frameworks"
        print(f"Starting workflow for topic: '{topic}'\n")
        print("=" * 60)
        
        # Step 1: Research
        print("\n[Step 1: Research Phase]")
        research_result = await research_agent.run(
            f"Research the topic: {topic}. Gather key information and statistics."
        )
        print(f"Research Agent Output:\n{research_result}\n")
        
        # Step 2: Analysis
        print("[Step 2: Analysis Phase]")
        analysis_result = await analysis_agent.run(
            f"Analyze this research:\n{research_result}\n\nProvide insights and trends."
        )
        print(f"Analysis Agent Output:\n{analysis_result}\n")
        
        # Step 3: Writing
        print("[Step 3: Writing Phase]")
        final_report = await writing_agent.run(
            f"Create a professional report based on this analysis:\n{analysis_result}"
        )
        print(f"Writing Agent Output:\n{final_report}\n")
        
        print("=" * 60)
        print("\n=== Workflow Complete ===")
        print(f"\nWorkflow successfully processed: {topic}")
        print(f"Agents involved: {len(workflow.agents)}")
        print(f"Pipeline: {' → '.join([agent.name for agent in workflow.agents])}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("1. Set environment variables in .env file")
        print("2. Run 'az login' to authenticate")
        print("3. Verify Azure OpenAI resource access")


async def parallel_workflow_example():
    """
    Bonus: Example of parallel agent execution
    This demonstrates how multiple agents can work on different tasks simultaneously
    """
    print("\n=== Parallel Workflow Example ===\n")
    
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
    
    # Create multiple specialized agents
    code_agent = ChatCompletionAgent(
        client=client,
        model=deployment,
        name="CodeAgent",
        instructions="You are a code generation expert."
    )
    
    doc_agent = ChatCompletionAgent(
        client=client,
        model=deployment,
        name="DocAgent",
        instructions="You are a documentation expert."
    )
    
    test_agent = ChatCompletionAgent(
        client=client,
        model=deployment,
        name="TestAgent",
        instructions="You are a testing expert."
    )
    
    # Execute agents in parallel
    task = "Create a Python function to calculate Fibonacci numbers"
    
    results = await asyncio.gather(
        code_agent.run(f"{task}"),
        doc_agent.run(f"Write documentation for: {task}"),
        test_agent.run(f"Write test cases for: {task}")
    )
    
    print("Code Agent:", results[0][:100], "...")
    print("Doc Agent:", results[1][:100], "...")
    print("Test Agent:", results[2][:100], "...")


if __name__ == "__main__":
    asyncio.run(main())
    # Uncomment to try parallel workflow:
    # asyncio.run(parallel_workflow_example())
