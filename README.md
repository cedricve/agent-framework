# Microsoft Agent Framework - Python Sample Project

This repository contains Python sample projects demonstrating the capabilities of **Microsoft Agent Framework**, the next-generation framework combining the best of Semantic Kernel and AutoGen.

## Overview

Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python. It provides:

- **AI Agents**: Individual agents that use LLMs to process user inputs, call tools and MCP servers, and generate responses
- **Workflows**: Graph-based workflows that connect multiple agents and functions for complex, multi-step tasks
- **Enterprise Features**: Thread-based state management, type safety, filters, telemetry, and extensive model support

## Prerequisites

Before running these samples, ensure you have:

- **Python 3.10 or later**
- [Azure OpenAI resource](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/create-resource) with a deployed model (e.g., `gpt-4o-mini`)
- [Azure CLI installed](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and authenticated (`az login`)
- User has Cognitive Services OpenAI User or Contributor roles for the Azure OpenAI resource

## Project Structure

```
├── README.md
├── requirements.txt
├── .env.example
├── examples/
│   ├── 01_basic_agent.py           # Simple agent example
│   ├── 02_agent_with_tools.py      # Agent with function calling
│   ├── 03_multi_turn_conversation.py  # Multi-turn chat with threads
│   └── 04_workflow_example.py      # Multi-agent workflow
└── .gitignore
```

## Samples

### 1. Basic Agent (`01_basic_agent.py`)

A simple example showing how to create and run a basic AI agent using Azure OpenAI.

**Key Concepts:**
- Creating an AI agent with Azure OpenAI
- Setting custom instructions
- Running simple queries

### 2. Agent with Tools (`02_agent_with_tools.py`)

Demonstrates how to equip an agent with custom function tools for enhanced capabilities.

**Key Concepts:**
- Creating custom tools using decorators
- Function descriptions and parameters
- Tool invocation during agent execution

### 3. Multi-Turn Conversation (`03_multi_turn_conversation.py`)

Shows how to maintain context across multiple interactions using agent threads.

**Key Concepts:**
- Creating and managing agent threads
- Maintaining conversation state
- Multi-turn dialogue handling

### 4. Workflow Example (`04_workflow_example.py`)

Advanced example showing how to orchestrate multiple agents in a workflow.

**Key Concepts:**
- Creating multi-agent workflows
- Sequential and parallel execution
- Agent coordination patterns

## Getting Started

### 1. Install Dependencies

```bash
pip install agent-framework
# or
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your Azure OpenAI details:

```bash
cp .env.example .env
```

Edit `.env`:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### 3. Login to Azure

```bash
az login
```

### 4. Run a Sample

```bash
python examples/01_basic_agent.py
```

## Installation

Install the Microsoft Agent Framework:

```bash
pip install agent-framework
```

## Learn More

- [Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- [Quick Start Guide](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [Migration from Semantic Kernel](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/)
- [Migration from AutoGen](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

## Contributing

This is a sample project for learning purposes. Feel free to extend and customize the examples for your own use cases.

## License

MIT

## Notes

- Microsoft Agent Framework is currently in **public preview**
- Uses Azure CLI credentials for authentication by default
- Alternatively, you can use `ApiKeyCredential` if you prefer API key authentication
