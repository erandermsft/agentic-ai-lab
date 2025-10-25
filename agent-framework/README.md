# Microsoft Agent Framework

## 🤖 Introduction

The **Microsoft Agent Framework** is an open-source development kit for building **AI agents** and **multi-agent workflows** for .NET and Python. It brings together and extends ideas from the Semantic Kernel and AutoGen projects, combining their strengths while adding new capabilities. Built by the same teams, it is the unified foundation for building AI agents going forward.

The Agent Framework offers two primary categories of capabilities:

### � AI Agents
Individual agents that use LLMs to process user inputs, call tools and MCP servers to perform actions, and generate responses. AI agents are suitable for applications that require:
- **Autonomous Decision-Making**: Dynamic problem-solving without predefined sequences
- **Tool Integration**: Seamless interaction with external APIs, databases, and services
- **Conversation Management**: Multi-turn conversations with persistent context
- **Model Flexibility**: Support for Azure OpenAI, OpenAI, and Azure AI providers

### 🔄 Workflows  
Graph-based workflows that connect multiple agents and functions to perform complex, multi-step tasks. Workflows provide:
- **Structured Orchestration**: Explicit control over multi-agent execution paths
- **Type Safety**: Strong typing with comprehensive validation
- **Checkpointing**: State persistence for long-running processes
- **Human-in-the-Loop**: Built-in patterns for human interaction and approval

### 🎯 Why Agent Framework?

The Agent Framework is the **direct successor** to Semantic Kernel and AutoGen, created by the same teams. It combines:
- **AutoGen's** simple abstractions for single- and multi-agent patterns
- **Semantic Kernel's** enterprise-grade features (thread management, type safety, telemetry)
- **New capabilities** including robust workflows and advanced state management

> **Note**: Microsoft Agent Framework is currently in **public preview**. This represents the next generation of both Semantic Kernel and AutoGen.

### 📚 Learn More

- 📖 **Official Documentation**: [Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- 🔗 **GitHub Repository**: [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Additional examples and source code
- 🚀 **Get Started**: Follow the notebooks below for hands-on learning

---

This folder contains comprehensive examples for the Microsoft Agent Framework, organized into three main categories:

## 📂 Folder Structure

### 🤖 **[agents/azure_ai_agents/](agents/azure_ai_agents/)** - Azure AI Agent Examples
Core agent development patterns using Azure AI services. These notebooks demonstrate single-agent capabilities with various tools and integrations including function tools, code interpreter, file search,and Bing grounding.

📖 **[View Azure AI Agents Documentation](agents/azure_ai_agents/README.md)** - Detailed guide for all agent examples

### 🔌 **[agents/mcp/](agents/mcp/)** - Model Context Protocol Examples
Examples demonstrating MCP (Model Context Protocol) integration with Agent Framework:
- Exposing agents as MCP servers
- API key authentication patterns
- Connecting AI applications to tools and data sources

📖 **[View MCP Documentation](agents/mcp/README.md)** - MCP integration guide

### 🔄 **[workflows/](workflows/)** - Multi-Agent Workflows & Orchestration
Graph-based workflow examples showing how to connect multiple agents and functions for complex tasks. Includes patterns for:
- Sequential and concurrent orchestration
- Checkpointing and state management
- Human-in-the-loop interactions
- Agent composition and nesting
- Magentic multi-agent coordination

📖 **[View Workflows Documentation](workflows/README.md)** - Comprehensive guide with 40+ workflow samples

### 🛡️ **[middleware/](middleware/)** - Middleware Patterns & Interceptors
Interactive notebooks demonstrating middleware patterns for agent execution interception:
- Agent, function, and chat middleware
- Security validation and logging
- Exception handling and retry logic
- Result transformation and streaming support
- Shared state management

📖 **[View Middleware Documentation](middleware/README.md)** - Complete middleware guide with 9 notebooks

### 🧠 **[context_providers/](context_providers/)** - Agent Memory & Context Management
Examples demonstrating how to build agents with memory using context providers:
- Custom memory providers for long-term memory
- User fact extraction and storage
- Context injection before agent invocation
- Memory persistence patterns
- Multi-provider composition with AggregateContextProvider

📖 **[View Context Providers Documentation](context_providers/README.md)** - Agent memory patterns guide

### 📊 **[observability/](observability/)** - Observability & Telemetry
Comprehensive examples demonstrating observability and telemetry collection for agents and workflows using OpenTelemetry and Azure Application Insights:
- **Agent Observability**: Trace LLM calls, tool executions, and token usage
- **Chat Client Observability**: Monitor Azure AI chat clients with multiple tools
- **Azure AI Foundry Integration**: Automatic Application Insights integration
- **Custom Spans & Metrics**: Add custom telemetry to your applications


### 🎨 **[devui/](devui/)** - Development UI & Testing
Sample agents and workflows designed for interactive testing with the Agent Framework DevUI - a lightweight web interface for agent development.

📖 **[View DevUI Documentation](devui/README.md)** - Getting started with the development interface

---

## 📚 Available Notebooks in agents/azure_ai_agents/

### Basic Examples
- **`azure_ai_basic.ipynb`** - Basic Azure AI agent usage with automatic lifecycle management
- **`azure_ai_with_explicit_settings.ipynb`** - Creating agents with explicit configuration settings

### Agent Management
- **`azure_ai_with_existing_agent.ipynb`** - Working with pre-existing agents using agent IDs
- **`azure_ai_with_existing_thread.ipynb`** - Managing conversation threads for continuity

### Tool Integration
- **`azure_ai_with_function_tools.ipynb`** - Comprehensive function tool integration patterns
- **`azure_ai_with_code_interpreter.ipynb`** - Python code execution and mathematical problem solving
- **`azure_ai_with_file_search.ipynb`** - Document-based question answering with file uploads

### Advanced Features
- **`azure_ai_with_bing_grounding.ipynb`** - Web search integration using Bing Grounding

📖 **[View Azure AI Agents Documentation](agents/azure_ai_agents/README.md)** - Detailed guide for all agent examples

---

## 🔌 Available Examples in agents/mcp/

### MCP Integration Patterns
- **`azure_ai_with_mcp.ipynb`** - Using hosted MCP tools with Azure AI Foundry agents (basic, multi-tool, and thread-based examples)
- **`agent_as_mcp_server.py`** - Expose an Agent Framework agent as an MCP server
- **`mcp_api_key_auth.py`** - API key authentication with MCP servers

📖 **[View MCP Documentation](agents/mcp/README.md)** - Complete MCP integration guide

---

## �️ Available Notebooks in middleware/

### Middleware Patterns (9 Interactive Notebooks)
- **`1-agent_and_run_level_middleware.ipynb`** - Agent-level vs run-level middleware
- **`2-function_based_middleware.ipynb`** - Function-based middleware patterns
- **`3-class_based_middleware.ipynb`** - Class-based middleware with inheritance
- **`4-decorator_middleware.ipynb`** - Decorator-based middleware (@agent_middleware, @function_middleware)
- **`5-chat_middleware.ipynb`** - Chat middleware for message interception
- **`6-exception_handling_with_middleware.ipynb`** - Exception handling patterns
- **`7-middleware_termination.ipynb`** - Early termination patterns
- **`8-override_result_with_middleware.ipynb`** - Result override for streaming/non-streaming
- **`9-shared_state_middleware.ipynb`** - Shared state with middleware containers

📖 **[View Middleware Documentation](middleware/README.md)** - Complete middleware guide

---

### Prerequisites

1. **Install Dependencies**: Make sure you have the agent-framework packages installed. Install in your virtual environment:

   **Alternative Installation Options:**

   **Development mode** - Install the entire framework with all sub-packages (simplest approach):
   ```bash
   pip install agent-framework --pre
   ```
   This installs the core and every integration package, making sure that all features are available without additional steps. The `--pre` flag is required while Agent Framework is in preview.

   **Selective install** - Install only specific integrations to keep dependencies lighter:
   ```bash
   # Core only (includes Azure OpenAI and OpenAI support by default)
   pip install agent-framework-core --pre

   # Core + Azure AI integration
   pip install agent-framework-azure-ai --pre

   # Core + Microsoft Copilot Studio integration
   pip install agent-framework-copilotstudio --pre

   # Core + both Microsoft Copilot Studio and Azure AI integration
   pip install agent-framework-microsoft agent-framework-azure-ai --pre
   ```

   **Supported Platforms:** Python 3.10+, Windows/macOS/Linux

2. **Azure Authentication**: Authenticate with Azure CLI:
   ```bash
   az login
   ```

## 🚀 Getting Started

### Prerequisites

1. **Install Dependencies**: Make sure you have the agent-framework packages installed. Install in your virtual environment:

   **Alternative Installation Options:**

   **Development mode** - Install the entire framework with all sub-packages (simplest approach):
   ```bash
   pip install agent-framework --pre
   ```
   This installs the core and every integration package, making sure that all features are available without additional steps. The `--pre` flag is required while Agent Framework is in preview.

   **Selective install** - Install only specific integrations to keep dependencies lighter:
   ```bash
   # Core only (includes Azure OpenAI and OpenAI support by default)
   pip install agent-framework-core --pre

   # Core + Azure AI integration
   pip install agent-framework-azure-ai --pre

   # Core + Microsoft Copilot Studio integration
   pip install agent-framework-copilotstudio --pre

   # Core + both Microsoft Copilot Studio and Azure AI integration
   pip install agent-framework-microsoft agent-framework-azure-ai --pre
   ```

   **Supported Platforms:** Python 3.10+, Windows/macOS/Linux

2. **Azure Authentication**: Authenticate with Azure CLI:
   ```bash
   az login
   ```

3. **Environment Configuration**: Set up your environment variables by copying the sample file in the `agents/azure_ai_agents/` folder:

   Copy the .env_sample file to create a .env file:
   ```bash
   cd agents/azure_ai_agents
   cp .env_sample .env
   ```

   Edit the .env file and add your values:
   ```
   AZURE_AI_PROJECT_ENDPOINT="your-project-endpoint"
   AZURE_AI_MODEL_DEPLOYMENT_NAME="your-model-deployment-name"
   TENANT_ID="your-tenant-id"
   ```

   For samples using Bing Grounding search (like `azure_ai_with_bing_grounding.ipynb`), you'll also need:
   ```
   BING_CONNECTION_ID="/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{ai-service-name}/projects/{project-name}/connections/{connection-name}"
   ```

   To get your Bing connection ID:
   - Go to Azure AI Foundry portal
   - Navigate to your project's "Connected resources" section
   - Add a new connection for "Grounding with Bing Search"
   - Copy the connection ID

### Running the Notebooks

1. **Start Jupyter**: Launch Jupyter Notebook or JupyterLab from the agent-framework folder:
   ```bash
   jupyter notebook
   ```

2. **Navigate**: Go to the `agents/azure_ai_agents/` folder and open any notebook

3. **Execute**: Run the cells in order, following the explanations and examples

## 📖 Learning Path

### Beginner
**Start with Azure AI Agents (agents/azure_ai_agents/)**
1. `azure_ai_basic.ipynb` - Understand fundamental concepts
2. `azure_ai_with_explicit_settings.ipynb` - Configuration patterns
3. `azure_ai_with_function_tools.ipynb` - Tool integration basics

### Intermediate
**Explore Advanced Agent Features**
1. `azure_ai_with_existing_agent.ipynb` - Agent persistence (agents/azure_ai_agents/)
2. `azure_ai_with_existing_thread.ipynb` - Conversation management (agents/azure_ai_agents/)
3. `azure_ai_with_file_search.ipynb` - Document search (agents/azure_ai_agents/)
4. **Context Providers (context_providers/)**:
   - `1-azure_ai_memory_context_providers.ipynb` - Agent memory and user fact extraction
5. **Middleware Basics (middleware/)**:
   - `1-agent_and_run_level_middleware.ipynb` - Middleware fundamentals
   - `2-function_based_middleware.ipynb` - Function-based patterns
   - `3-class_based_middleware.ipynb` - Class-based patterns

### Advanced
**Master Complex Patterns**
1. **MCP Integration (agents/mcp/)**:
   - `azure_ai_with_mcp.ipynb` - Hosted MCP tools with Azure AI Foundry
   - `agent_as_mcp_server.py` - Expose agents as MCP servers
2. **Advanced Middleware (middleware/)**:
   - `6-exception_handling_with_middleware.ipynb` - Exception handling
   - `7-middleware_termination.ipynb` - Termination patterns
   - `8-override_result_with_middleware.ipynb` - Result override with streaming
3. **Web Integration (agents/azure_ai_agents/)**:
   - `azure_ai_with_bing_grounding.ipynb` - Web search integration
   - `azure_ai_with_code_interpreter.ipynb` - Code execution

### Expert
**Multi-Agent Systems & Workflows**
1. Explore **workflows/** folder for orchestration patterns
2. Use **devui/** for interactive testing and development
3. Combine agents, middleware, and MCP for production systems

## 🔧 Key Features Demonstrated

### Core Concepts
- ✅ Agent creation and lifecycle management
- ✅ Authentication patterns with Azure CLI
- ✅ Environment configuration and best practices
- ✅ Error handling and resource cleanup
- ✅ Middleware interception and modification

### Tool Integration
- ✅ Function tools for custom capabilities
- ✅ Code interpreter for Python execution
- ✅ File search for document-based Q&A
- ✅ Web search with Bing integration
- ✅ External API integration via OpenAPI
- ✅ MCP (Model Context Protocol) servers

### Advanced Patterns
- ✅ Multi-turn conversations
- ✅ Thread management and persistence
- ✅ Agent reuse patterns
- ✅ Tool combination strategies
- ✅ User approval workflows
- ✅ Context providers for agent memory
- ✅ Custom memory extraction and injection
- ✅ Middleware security and validation
- ✅ Exception handling with middleware
- ✅ Result transformation and streaming
- ✅ Agent-to-MCP server exposure

### Observability & Monitoring
- ✅ OpenTelemetry integration for agents and workflows
- ✅ Azure Application Insights automatic setup
- ✅ Trace ID generation for debugging
- ✅ Agent invocation and LLM call tracing
- ✅ Tool execution monitoring
- ✅ Workflow executor and message passing spans
- ✅ Token usage and performance metrics
- ✅ Custom spans and metrics
- ✅ Application Insights query patterns

## 💡 Tips for Success

1. **Environment Setup**: Ensure all environment variables are properly configured
2. **Authentication**: Keep your Azure CLI session active
3. **Resource Management**: Always clean up resources to avoid unnecessary costs
4. **Error Handling**: Pay attention to error handling patterns in the examples
5. **Best Practices**: Follow the documented best practices for production usage

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Errors**: Run `az login` and verify your credentials
2. **Missing Environment Variables**: Check that all required variables are set
3. **Package Import Errors**: Ensure agent-framework packages are installed
4. **Resource Not Found**: Verify your Azure AI project configuration

---

## 🔄 Workflows - Multi-Agent Orchestration

The **[workflows/](workflows/)** folder contains 40+ examples demonstrating how to build complex, multi-agent systems using graph-based workflows.

### Quick Start with Workflows

1. **Start with the basics** in `workflows/_start-here/notebooks/`:
   - `step1_executors_and_edges.ipynb` - Core workflow concepts
   - `step2_agents_in_a_workflow.ipynb` - Adding agents to workflows
   - `step3_streaming.ipynb` - Event streaming basics

2. **Explore advanced patterns**:
   - **Orchestration** - Sequential and concurrent agent coordination
   - **Checkpointing** - Save and resume long-running workflows
   - **Human-in-the-Loop** - Interactive approval and feedback
   - **Magentic** - AI-driven multi-agent planning and execution

### Key Workflow Capabilities

- 🔀 **Control Flow**: Conditional routing, loops, and branching
- 🧩 **Composition**: Nest workflows and build modular systems
- ⚡ **Parallelism**: Fan-out/fan-in patterns for concurrent execution
- 💾 **State Management**: Shared state across agents and checkpoints
- 🔍 **Observability**: Built-in tracing and monitoring

📖 **[Full Workflows Documentation](workflows/README.md)**

---

## 🎨 DevUI - Interactive Development Interface

The **[devui/](devui/)** folder provides a web-based interface for testing agents and workflows interactively.

### Quick Start with DevUI

**Option 1: In-Memory Mode** (Simplest)
```bash
cd devui
python in_memory_mode.py
```
Opens browser at http://localhost:8090 with pre-configured samples

**Option 2: Directory Discovery**
```bash
cd devui
devui
```
Starts server at http://localhost:8080 with all samples

### DevUI Features

- 🌐 **Web Interface**: Interactive chat interface for testing
- 🔌 **OpenAI-Compatible API**: Standard endpoints for integration
- 📁 **Auto-Discovery**: Automatically finds agents and workflows
- 🎨 **Sample Gallery**: Pre-built examples to learn from

### Available DevUI Samples

- **foundry_agent/** - Azure AI Foundry agent integration
- **weather_agent_azure/** - Weather lookup with Azure services
- **spam_workflow/** - Email classification workflow
- **fanout_workflow/** - Parallel processing demonstration
- **workflow_agents/** - Multi-agent workflow examples

📖 **[Full DevUI Documentation](devui/README.md)**

---

## 🎓 Complete Learning Journey

### Phase 1: Single Agents (agents/azure_ai_agents/)
Start with the Azure AI agent notebooks to master individual agent patterns, tool integration, and Azure AI services.

### Phase 2: Agent Memory (context_providers/)
Learn how to build agents with long-term memory using context providers for fact extraction, storage, and context injection.

### Phase 3: MCP Integration (agents/mcp/)
Learn how to connect agents to external tools and data sources using Model Context Protocol, and expose your agents as MCP servers.

### Phase 4: Observability & Telemetry (observability/)
Master observability patterns for agents and workflows, including Application Insights integration, custom spans, and trace analysis.

### Phase 5: Middleware Patterns (middleware/)
Master execution interception with middleware for security, logging, exception handling, and result transformation across 9 interactive notebooks.

### Phase 6: Multi-Agent Workflows (workflows/)
Progress to the workflows folder to learn orchestration, state management, and complex multi-agent coordination.

### Phase 7: Interactive Development (devui/)
Use DevUI to experiment with your agents and workflows in a visual, interactive environment.

---