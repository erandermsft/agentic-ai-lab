# MCP (Model Context Protocol) Examples

This folder contains examples demonstrating how to work with MCP using Agent Framework, including both consuming MCP tools in your agents and exposing your agents as MCP servers.

## What is MCP?

The Model Context Protocol (MCP) is an open standard for connecting AI agents to data sources and tools. It enables secure, controlled access to local and remote resources through a standardized protocol.

## Examples

| Sample | File | Description |
|--------|------|-------------|
| **Azure AI with Hosted MCP** | [`azure_ai_with_mcp.ipynb`](azure_ai_with_mcp.ipynb) | Interactive notebook showing how to use hosted MCP tools with Azure AI Foundry agents, including basic integration, multi-tool configuration, and thread-based conversations |
| **Agent as MCP Server** | [`agent_as_mcp_server.py`](agent_as_mcp_server.py) | Shows how to expose an Agent Framework agent as an MCP server that other AI applications can connect to |
| **API Key Authentication** | [`mcp_api_key_auth.py`](mcp_api_key_auth.py) | Demonstrates API key authentication with MCP servers |

## 📓 Azure AI with Hosted MCP Tools

The **`azure_ai_with_mcp.ipynb`** notebook provides comprehensive examples of integrating Azure AI Foundry agents with hosted MCP servers.

### What You'll Learn

- **Basic MCP Integration**: Create agents with hosted MCP tools (Microsoft Learn MCP server)
- **Multi-Tool Configuration**: Use multiple MCP tools with different approval modes
- **Thread-Based Conversations**: Maintain conversation context across multiple queries
- **Azure AI Observability**: Built-in monitoring and tracing for production scenarios

### Key Features Demonstrated

- ✅ **Hosted MCP Server**: Azure AI Foundry manages the MCP server infrastructure
- ✅ **Persistent Agents**: Server-side agent creation with stateful conversations
- ✅ **Tool Approval Workflow**: Configurable approval mechanisms (`never_require`, `always_require`)
- ✅ **Observability**: Built-in Azure AI observability for monitoring and debugging
- ✅ **Microsoft Learn Integration**: Search and retrieve Microsoft documentation

### Examples in the Notebook

1. **Example 1: Basic MCP Integration**
   - Simple agent with Microsoft Learn MCP server
   - Auto-approval for documentation queries
   - Azure AI observability setup

2. **Example 2: Multi-Tool MCP Configuration**
   - Multiple MCP tools with different approval modes
   - Custom headers for authentication
   - Tool-specific security settings

3. **Example 3: Thread-Based Conversation**
   - Conversation context persistence
   - Multi-query interactions
   - Thread management patterns

### Prerequisites for Azure AI MCP Notebook

- **Azure AI Foundry Project**: Access to an Azure AI Foundry project with deployed models
- **Environment Variables**: Configure `.env` file with:
  - `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI Foundry project endpoint
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your model deployment name (e.g., gpt-4o)
- **Authentication**: Azure CLI installed and authenticated (`az login`)
- **Dependencies**: Agent Framework packages installed (`pip install agent-framework --pre`)

## 🔧 Python Script Examples

### Agent as MCP Server

**Prerequisites:**
- `OPENAI_API_KEY` environment variable
- `OPENAI_RESPONSES_MODEL_ID` environment variable

## 🚀 Getting Started

### For Azure AI Foundry MCP Integration

1. **Open the Notebook**: Navigate to [`azure_ai_with_mcp.ipynb`](azure_ai_with_mcp.ipynb)
2. **Configure Environment**: Set up your `.env` file in the `agents/azure_ai_agents/` directory
3. **Run Examples**: Execute cells sequentially to see each MCP pattern in action
4. **Experiment**: Modify queries, approval modes, and tool configurations

### For Agent as MCP Server

Run the Python script to expose your agent as an MCP server that other applications can connect to.

## 📖 Learn More

- **MCP Official Docs**: [Model Context Protocol](https://modelcontextprotocol.io/)
- **Azure AI MCP Docs**: [Using MCP with Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents)
- **Agent Framework Docs**: [Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
