# Copyright (c) Microsoft. All rights reserved.

import os
from typing import Annotated, Any

import anyio
from dotenv import load_dotenv
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

"""
This sample demonstrates how to expose an Azure AI Agent as an MCP server.

Prerequisites:
- Azure AI Foundry project with a deployed model
- Azure CLI authentication (run `az login`)
- .env file with:
  - AZURE_AI_PROJECT_ENDPOINT
  - AZURE_AI_MODEL_DEPLOYMENT_NAME

To run this sample, set up your MCP host (like Claude Desktop or VSCode Github Copilot Agents)
with the following configuration:
```json
{
    "servers": {
        "agent-framework": {
            "command": "uv",
            "args": [
                "--directory=<path to project>/agent-framework/agents/mcp",
                "run",
                "agent_as_mcp_server.py"
            ],
            "env": {
                "AZURE_AI_PROJECT_ENDPOINT": "<your-project-endpoint>",
                "AZURE_AI_MODEL_DEPLOYMENT_NAME": "<your-model-deployment>"
            }
        }
    }
}
```
"""

# Load environment variables
load_dotenv('../azure_ai_agents/.env')


def get_specials() -> Annotated[str, "Returns the specials from the menu."]:
    return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """


def get_item_price(
    menu_item: Annotated[str, "The name of the menu item."],
) -> Annotated[str, "Returns the price of the menu item."]:
    return "$9.99"


async def run() -> None:
    # Verify environment variables
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    if not endpoint:
        raise ValueError("AZURE_AI_PROJECT_ENDPOINT environment variable is required")
    
    print(f"Using Azure AI endpoint: {endpoint[:50]}...")
    print(f"Using model deployment: {model}")
    
    # Create Azure AI agent
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential) as chat_client,
    ):
        # Define an agent
        # Agent's name and description provide better context for AI model
        agent = chat_client.create_agent(
            name="RestaurantAgent",
            instructions="Answer questions about the menu.",
            tools=[get_specials, get_item_price],
        )
        
        print(f"Created agent: {agent.name}")
        print("Starting MCP server...")

        # Expose the agent as an MCP server
        server = agent.as_mcp_server()

        # Run server
        from mcp.server.stdio import stdio_server

        async def handle_stdin(stdin: Any | None = None, stdout: Any | None = None) -> None:
            async with stdio_server() as (read_stream, write_stream):
                await server.run(read_stream, write_stream, server.create_initialization_options())

        await handle_stdin()


if __name__ == "__main__":
    anyio.run(run)
