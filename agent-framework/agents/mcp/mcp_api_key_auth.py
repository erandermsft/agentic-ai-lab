# Copyright (c) Microsoft. All rights reserved.

import os
import asyncio
from dotenv import load_dotenv

from agent_framework import HostedMCPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

"""
MCP Authentication Example with Azure AI Foundry

This example demonstrates how to authenticate with MCP servers using API key headers
with Azure AI Foundry agents.

Prerequisites:
- Azure AI Foundry project with a deployed model
- Azure CLI authentication (run `az login`)
- .env file with:
  - AZURE_AI_PROJECT_ENDPOINT
  - AZURE_AI_MODEL_DEPLOYMENT_NAME
  - MCP_SERVER_URL (optional, for testing)
  - MCP_API_KEY (optional, for testing)

For more authentication examples including OAuth 2.0 flows, see:
- https://github.com/modelcontextprotocol/python-sdk/tree/main/examples/clients/simple-auth-client
- https://github.com/modelcontextprotocol/python-sdk/tree/main/examples/servers/simple-auth
"""

# Load environment variables
load_dotenv('../azure_ai_agents/.env')


async def api_key_auth_example() -> None:
    """Example of using API key authentication with MCP server and Azure AI Foundry."""
    
    # Verify Azure AI environment variables
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    if not endpoint:
        raise ValueError("AZURE_AI_PROJECT_ENDPOINT environment variable is required")
    
    print(f"Using Azure AI endpoint: {endpoint[:50]}...")
    print(f"Using model deployment: {model}")
    
    # MCP server configuration (optional - for custom MCP servers)
    mcp_server_url = os.getenv("MCP_SERVER_URL", "https://your-mcp-server-url")
    api_key = os.getenv("MCP_API_KEY", "your-api-key")

    # Create authentication headers
    # Common patterns:
    # - Bearer token: "Authorization": f"Bearer {api_key}"
    # - API key header: "X-API-Key": api_key
    # - Custom header: "Authorization": f"ApiKey {api_key}"
    auth_headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Create Azure AI agent with MCP tool that uses authentication
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential) as chat_client,
    ):
        print("\nCreating agent with authenticated MCP tool...")
        
        # Create agent with HostedMCPTool that includes authentication headers
        agent = chat_client.create_agent(
            name="AuthenticatedMCPAgent",
            instructions="You are a helpful assistant that can access authenticated MCP tools.",
            tools=HostedMCPTool(
                name="Authenticated MCP Tool",
                url=mcp_server_url,
                headers=auth_headers,  # Authentication headers
            ),
        )
        
        print(f"✅ Created agent: {agent.name}\n")

        # Test the agent
        query = "What tools are available to you?"
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(api_key_auth_example())
