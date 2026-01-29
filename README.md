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
│   ├── 01_basic_agent.py              # Single agent with tools
│   ├── 02_workflow.py                 # Multi-agent handoff workflow
│   ├── 03_strict_workflow.py          # Workflow with restricted handoff paths
│   ├── 04_strict_workflow_nobypass.py # Workflow preventing direct agent bypass
│   └── 05_tracing-observability.py    # Workflow with OpenTelemetry tracing
└── .gitignore
```

## Samples

### 1. Basic Agent (`01_basic_agent.py`)

A simple example showing how to create and run a single AI agent with tool calling using Azure OpenAI.

**Key Concepts:**
- Creating a `ChatAgent` with `AzureOpenAIChatClient`
- Defining tools using the `@ai_function` decorator
- Azure AD authentication with `AzureCliCredential`
- Running queries and handling tool invocations

### 2. Multi-Agent Workflow (`02_workflow.py`)

Demonstrates a customer support system with multiple specialized agents coordinated through handoffs.

**Key Concepts:**
- Creating multiple `ChatAgent` instances (triage, refund, order, return agents)
- Building handoff workflows with `HandoffBuilder`
- Setting a coordinator agent with `.set_coordinator()`
- Handling `RequestInfoEvent` and `HandoffUserInputRequest` for user interaction
- Custom termination conditions

### 3. Strict Workflow (`03_strict_workflow.py`)

Shows how to restrict which agents can hand off to which other agents, creating controlled conversation flows.

**Key Concepts:**
- Defining explicit handoff paths with `.add_handoff(source, [targets])`
- Preventing triage from routing directly to refund agent
- Creating agent hierarchies (return agent → refund agent)
- Bi-directional handoffs back to triage for re-routing

### 4. Strict Workflow - No Bypass (`04_strict_workflow_nobypass.py`)

Similar to example 3, but with enhanced instructions to prevent agents from bypassing the defined handoff rules.

**Key Concepts:**
- Agent instructions that explicitly state routing constraints
- Enforcing workflow policies through both code and prompts
- Defense-in-depth approach to agent coordination

### 5. Tracing & Observability (`05_tracing-observability.py`)

Demonstrates how to add OpenTelemetry tracing to agent workflows for monitoring and debugging.

**Key Concepts:**
- Configuring observability with `setup_observability()`
- Sending traces to Azure Application Insights
- OTLP exporter support for LangSmith or other backends
- Environment variables: `APPLICATIONINSIGHTS_CONNECTION_STRING`, `OTEL_EXPORTER_OTLP_ENDPOINT`

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
