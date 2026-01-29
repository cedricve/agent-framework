import os
import asyncio
from typing import Annotated
from azure.identity import AzureCliCredential, get_bearer_token_provider
from agent_framework import ai_function, HandoffBuilder, RequestInfoEvent, HandoffUserInputRequest, WorkflowOutputEvent
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv

from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework.observability import create_resource, enable_instrumentation

load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

@ai_function
def process_refund(order_number: Annotated[str, "Order number to process refund for"]) -> str:
    """Simulated function to process a refund for a given order number."""
    return f"Refund processed successfully for order {order_number}."

@ai_function
def check_order_status(order_number: Annotated[str, "Order number to check status for"]) -> str:
    """Simulated function to check the status of a given order number."""
    return f"Order {order_number} is currently being processed and will ship in 2 business days."

@ai_function
def process_return(order_number: Annotated[str, "Order number to process return for"]) -> str:
    """Simulated function to process a return for a given order number."""
    return f"Return initiated successfully for order {order_number}. You will receive return instructions via email."

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

    # Create a chat client
    chat_client = AzureOpenAIChatClient(
        azure_endpoint=endpoint,
        ad_token_provider=token_provider,
        api_version=api_version,
        deployment_name=deployment
    )

    # Create triage/coordinator agent
    triage_agent = chat_client.as_agent(
        instructions=(
            "You are frontline support triage. Route customer issues to the appropriate specialist agents. "
            "You can ONLY route to: order_agent (for order/shipping inquiries) or return_agent (for returns). "
            "You CANNOT route directly to refund_agent. For refund requests, route to return_agent first, "
            "who will then handle the refund process if appropriate."
        ),
        description="Triage agent that handles general inquiries.",
        name="triage_agent",
    )

    # Refund specialist: Handles refund requests
    refund_agent = chat_client.as_agent(
        instructions="You process refund requests.",
        description="Agent that handles refund requests.",
        name="refund_agent",
        # In a real application, an agent can have multiple tools; here we keep it simple
        tools=[process_refund],
    )

    # Order/shipping specialist: Resolves delivery issues
    order_agent = chat_client.as_agent(
        instructions="You handle order and shipping inquiries.",
        description="Agent that handles order tracking and shipping issues.",
        name="order_agent",
        # In a real application, an agent can have multiple tools; here we keep it simple
        tools=[check_order_status],
    )

    # Return specialist: Handles return requests
    return_agent = chat_client.as_agent(
        instructions="You manage product return requests.",
        description="Agent that handles return processing.",
        name="return_agent",
        # In a real application, an agent can have multiple tools; here we keep it simple
        tools=[process_return],
    )

    # Build the handoff workflow
    workflow = (
        HandoffBuilder(
            name="customer_support_handoff",
            participants=[triage_agent, refund_agent, order_agent, return_agent],
        )
        .with_start_agent(triage_agent) # Triage receives initial user input
        .with_termination_condition(
            # Custom termination: Check if one of the agents has provided a closing message.
            # This looks for the last message containing "welcome", which indicates the
            # conversation has concluded naturally.
            lambda conversation: len(conversation) > 0 and "welcome" in conversation[-1].text.lower()
        )
        # Triage cannot route directly to refund agent
        .add_handoff(triage_agent, [order_agent, return_agent])
        # Only the return agent can handoff to refund agent - users wanting refunds after returns
        .add_handoff(return_agent, [refund_agent])
        # All specialists can handoff back to triage for furefunrther routing
        .add_handoff(order_agent, [triage_agent])
        .add_handoff(return_agent, [triage_agent])
        .add_handoff(refund_agent, [triage_agent])
        #.with_autonomous_mode(agents=[triage_agent])
        .build()
    )

    # Start workflow with initial user message
    events = [event async for event in workflow.run_stream("I need help with my order")]

    # Process events and collect pending input requests
    pending_requests = []
    for event in events:
        if isinstance(event, RequestInfoEvent) and isinstance(event.data, HandoffUserInputRequest):
            pending_requests.append(event)
            request_data = event.data
            print(f"Agent {event.source_executor_id} is awaiting your input")
            # The request contains the most recent messages generated by the
            # agent requesting input
            for msg in request_data.agent_response.messages[-3:]:
                print(f"{msg.author_name}: {msg.text}")

    # Interactive loop: respond to requests
    while pending_requests:
        user_input = input("You: ")

        # Send responses to all pending requests
        responses = {req.request_id: HandoffUserInputRequest.create_response(user_input) for req in pending_requests}
        # You can also send a `HandoffUserInputRequest.terminate()` to end the workflow early
        events = [event async for event in workflow.send_responses_streaming(responses)]

        # Process new events
        pending_requests = []
        for event in events:
            if isinstance(event, RequestInfoEvent) and isinstance(event.data, HandoffUserInputRequest):
                pending_requests.append(event)
                request_data = event.data
                print(f"Agent {event.source_executor_id} is awaiting your input")
                for msg in request_data.agent_response.messages[-3:]:
                    print(f"{msg.author_name}: {msg.text}")
            elif isinstance(event, WorkflowOutputEvent):
                print("Workflow has completed.")
                print("Final conversation:")
                for msg in event.data.conversation:
                    print(f"{msg.author_name}: {msg.text}")


if __name__ == "__main__":
    asyncio.run(main())