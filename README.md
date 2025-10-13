# 🚀 Azure AI Foundry E2E Workshop

[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI-Foundry-blue?style=for-the-badge&logo=microsoft)](https://ai.azure.com)
[![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-orange?style=for-the-badge&logo=jupyter)](https://jupyter.org)

**End-to-End Azure AI Foundry Development Laboratory**

*Master Azure AI Foundry through hands-on experimentation and real-world applications*

---

🎯 [Getting Started](#-getting-started) • 📚 [Learning Path](#-learning-path) • 🔧 [Setup Guide](#-environment-setup) • 🛠️ [Troubleshooting](#-troubleshooting--support)

---

## 🎯 Mission Statement

This comprehensive laboratory transforms you from an AI enthusiast into an Azure AI Foundry expert. Through progressive, hands-on modules, you'll master:

1. Setup, Authentication, Quick Start
2. Prompting, Embeddings, RAG, Phi-4, DeepSeek
3. Agents – File Search, Bing, Azure Functions
4. Multi-Agent Orchestration + Tracing
5. Model Context Protocol (MCP) with Agents
6. AI Red Teaming & Security Testing
7. Agent Framework – Advanced Agent Development
8. Frameworks – AutoGen, Semantic Kernel
9. Observability & Evaluation
10. AI Language Services with Low-Code Workflows
11. AI Vision with Low-Code Solutions
12. Content Understanding & Document Classification
13. Responsible AI & Content Safety


> **🎓 Laboratory Format**: One day intensive hands-on experience  
> **🎯 Target Audience**: Developers, AI practitioners, and solution architects  
> **💡 Learning Approach**: Progressive complexity with real-world applications

---

## 📁 Repository Structure

```
ai-foundry-e2e-lab/
├── 📚 initial-setup/           # Start here - Authentication & environment setup
├── 💬 chat-rag/               # Chat completion and RAG fundamentals
├── 🤖 agents/                 # AI Agents development and tools
├── 🔄 multi-agent/            # Multi-agent systems and orchestration
├── 🔌 agents-with-mcp/        # Model Context Protocol (MCP) integration
├── 🔴 ai-red-teaming-agent/   # AI Red Teaming and Security Testing
├── 🤖⚙️ agent-framework/        # Microsoft Agent Framework for advanced agent development
├── 🏗️ sk-and-autogen/          # Semantic Kernel and AutoGen frameworks
├── 📊 observalibility/         # Monitoring, evaluation, and quality assurance
├── 🗣️ ai-language/             # AI Language Services with Logic Apps low-code workflows
├── 👁️ ai-vision/               # AI Vision Services with low-code solutions
├── 📄 content-understanding/   # Document classification and content extraction
└── 🛡️ responsible-ai/          # Responsible AI, Content Safety, and PII Detection
```

---

## 🚀 Getting Started

### Step 1: Repository Setup

```powershell
# Clone the laboratory repository
git clone https://github.com/dhangerkapil/ai-foundry-e2e-lab.git
cd ai-foundry-e2e-lab

# Verify Python version
python --version  # Should be 3.10 or higher
```

### Step 2: Python Environment Configuration

**Option A: Using UV (Recommended - Fastest)**
```powershell
# Install UV package manager for Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create and activate virtual environment
uv venv
.\.venv\Scripts\Activate.ps1
```

**Option B: Using Standard venv**
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
# Install core dependencies
pip install -r requirements.txt

# Register Jupyter kernel
python -m ipykernel install --user --name=ai-foundry-lab --display-name="AI Foundry Lab"
```

### Step 4: Azure AI Foundry Setup

1. **Create Azure AI Foundry Project**
   - Navigate to [Azure AI Foundry Portal](https://ai.azure.com)
   - Create a new project with Standard pricing tier
   - Choose region based on model availability (East US 2 recommended)

2. **Deploy Required Models & Services**
   
   | Model Type | Recommended Models | Purpose |
   |------------|-------------------|---------|
   | **Chat/Completion** | `gpt-4o`, `gpt-4o-mini` | Primary reasoning & conversation |
   | **Text Embeddings** | `text-embedding-3-large` | Vector search & RAG |
   | **(Optional) Image Embeddings** | `cohere-embed-v3-english` | Image search & multimodal tasks |
   | **Image Generation** | `dall-e-3` | Image creation from text |
   | **Specialized** | `phi-4`, `deepseek-r1` | Domain-specific tasks |

3. **Configure an Azure OpenAI Resource**
   - Create an Azure OpenAI resource in the same region as your AI Foundry project
   - Connect this resource to your AI Foundry project
      - Navigate to your AI Foundry project → Management Center → Connected Resources → Add Connection → Select Azure OpenAI

<img src="foundry-connection.png" width="75%"/>

4. **Configure an Azure Search Service**
   - Create an Azure AI Search resource in Azure
   - Connect this resource to your AI Foundry project
      - Navigate to your AI Foundry project → Management Center → Connected Resources → Add Connection → Select Azure AI Search

5. **Configure Grounding with Bing Search**
   - Create a new Grounding with Bing Search resource in Azure
   - Connect this resource to your AI Foundry project
      - Navigate to your AI Foundry project → Management Center → Connected Resources → Add Connection → Select Grounding with Bing Search

6. **Create Content Understanding Resource**
   - Create an Azure AI Content Understanding multi-service resource following the [official documentation](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/how-to/create-multi-service-resource)
   - Ensure the resource is created in a supported region (westus, swedencentral, australiaeast)
  
7. **Configure Environment Variables**
   - Copy `.env.example` to `.env` in the root directory and update values accordingly
   - This repository expects the `.env` file to be in the root directory, if you want to store it elsewhere or name it something else, update the `load_dotenv()` calls in notebooks
   - Many of the Environment Variables needed can be found in the Overview tab of your Azure AI Foundry project or the connected resources in the Management Center tab
   - For example, AZURE_OPENAI variables-
<img src="env-example.png" width="75%"/>   

---

## 📚 Learning Path

Follow this structured learning path to master Azure AI Foundry:

### 🎯 Phase 1: Foundation (Start Here)
**Location:** `initial-setup/`

| Notebook | Description |
|----------|-------------|
| 🔐 [Authentication](initial-setup/1-authentication.ipynb) | Azure credential setup and security |
| ⚙️ [Environment Setup](initial-setup/2-environment_setup.ipynb) | Development environment configuration |
| 🚀 [Quick Start](initial-setup/3-quick_start.ipynb) | First AI model interaction |

### 💬 Phase 2: Chat & RAG Fundamentals
**Location:** `chat-rag/`

| Notebook | Description |
|----------|-------------|
| 💬 [Basic Chat Completion](chat-rag/1-basic-chat-completion.ipynb) | Foundation models and prompting |
| 🔍 [Embeddings](chat-rag/2-embeddings.ipynb) | Vector representations and similarity |
| 📚 [Basic RAG](chat-rag/3-basic-rag.ipynb) | Retrieval-Augmented Generation |
| 🧠 [Phi-4](chat-rag/4-phi-4.ipynb) | Microsoft's reasoning model |
| 🤖 [DeepSeek R1](chat-rag/5-deep-seek-r1.ipynb) | Advanced reasoning capabilities |

### 🤖 Phase 3: AI Agents Development  
**Location:** `agents/`

| Notebook | Description |
|----------|-------------|
| 🤖 [Agent Basics](agents/1-basics.ipynb) | Fundamental agent concepts |
| 💻 [Code Interpreter](agents/2-code_interpreter.ipynb) | Code execution capabilities |
| 📄 [File Search](agents/3-file-search.ipynb) | Document processing |
| 🌐 [Bing Grounding](agents/4-bing_grounding.ipynb) | Web search integration |
| 🔍 [Agents + AI Search](agents/5-agents-aisearch.ipynb) | Enterprise search integration |
| ⚡ [Agents + Azure Functions](agents/6-agents-az-functions.ipynb) | Serverless integration |

### 🔄 Phase 4: Multi-Agent Systems
**Location:** `multi-agent/`

| Notebook | Description |
|----------|-------------|
| 👥 [Multi-Agent Solution](multi-agent/multi-agent-solution.ipynb) | Collaborative AI systems |
| 📊 [Multi-Agent with Tracing](multi-agent/multi-agent-solution-with-tracing.ipynb) | Advanced monitoring |

### 🔌 Phase 5: Model Context Protocol (MCP) Integration
**Location:** `agents-with-mcp/`

| Implementation | Description |
|----------|-------------|
| 🔌 [MCP Inventory Agent](agents-with-mcp/README.md) | Complete working implementation of agents that connect to MCP servers for dynamic tool discovery. Features an intelligent inventory management agent for a cosmetics retailer with automated restock and clearance recommendations. Includes both client and server implementations with interactive chat interface. |

### 🔴 Phase 6: AI Red Teaming & Security Testing
**Location:** `ai-red-teaming-agent/`

| Implementation | Description |
|----------|-------------|
| 🔴 [AI Red Teaming Agent](ai-red-teaming-agent/README.md) | Advanced AI security testing and vulnerability assessment using red teaming methodologies. Features automated adversarial prompt generation, safety evaluation, and comprehensive security analysis of AI systems. |

### 🤖⚙️ Phase 7: Microsoft Agent Framework
**Location:** `agent-framework/`

The **Microsoft Agent Framework** is an open-source development kit that unifies and extends Semantic Kernel and AutoGen into the next-generation foundation for AI agent development. Built by the same teams, it offers two primary capabilities: **AI Agents** for autonomous decision-making with tool integration and conversation management, and **Workflows** for orchestrating complex multi-agent processes with type safety and checkpointing. Currently in public preview, it combines AutoGen's simple abstractions with Semantic Kernel's enterprise features while adding robust workflow capabilities.

📖 [Official Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) • 🔗 [GitHub Repository](https://github.com/microsoft/agent-framework)

| Notebook | Description |
|----------|-------------|
| 🤖 [Basic Agent Usage](agent-framework/azure_ai_basic.ipynb) | Fundamental agent concepts with automatic lifecycle management |
| ⚙️ [Explicit Settings](agent-framework/azure_ai_with_explicit_settings.ipynb) | Agent creation with explicit configuration patterns |
| 🔄 [Existing Agent Management](agent-framework/azure_ai_with_existing_agent.ipynb) | Working with pre-existing agents using agent IDs |
| 💬 [Thread Management](agent-framework/azure_ai_with_existing_thread.ipynb) | Conversation thread continuity and management |
| 🔧 [Function Tools](agent-framework/azure_ai_with_function_tools.ipynb) | Comprehensive function tool integration patterns |
| 💻 [Code Interpreter](agent-framework/azure_ai_with_code_interpreter.ipynb) | Python code execution and mathematical problem solving |
| 📄 [File Search](agent-framework/azure_ai_with_file_search.ipynb) | Document-based question answering with file uploads |
| 🌐 [Bing Grounding](agent-framework/azure_ai_with_bing_grounding.ipynb) | Web search integration using Bing Grounding |
| 🔌 [MCP Integration](agent-framework/azure_ai_with_mcp.ipynb) | Model Context Protocol (MCP) tool integration |

### 🏗️ Phase 8: Semantic Kernel + AutoGen
**Location:** `sk-and-autogen/`

| Notebook | Description |
|----------|-------------|
| 🔧 [RAG + Semantic Kernel + Agents](sk-and-autogen/1-rag-sk-agents-aisearch.ipynb) | Microsoft's orchestration framework |
| 🤖 [AutoGen Multi-Agent RAG](sk-and-autogen/2-autogen-multi-agent-rag.ipynb) | Automated agent generation |
| ❤️ [AutoGen Personalized Analytics](sk-and-autogen/3-autogen-personalized-heart-rate.ipynb) | Health domain specialization |

### 📊 Phase 9: Quality & Operations
**Location:** `observalibility/`

| Notebook | Description |
|----------|-------------|
| 👁️ [Observability](observalibility/1-Observability.ipynb) | Monitoring and telemetry |
| 📈 [Evaluation](observalibility/2-evaluation.ipynb) | Quality assessment and benchmarking |

### 🗣️ Phase 10: AI Language Services with Low-Code Workflows
**Location:** `ai-language/`

| Implementation | Description |
|----------|-------------|
| 🔤 [AI Language Service Lab](ai-language/README.md) | Low-code Logic Apps for PII removal, language detection, and translation. Build workflow solutions for processing multilingual customer feedback with privacy compliance and centralized analytics. |

### 👁️ Phase 11: AI Vision Services with Low-Code Solutions  
**Location:** `ai-vision/`

| Implementation | Description |
|----------|-------------|
| 👀 [AI Vision Lab Guide](ai-vision/README.md) | Azure AI Vision low-code exercises including OCR, face detection, image analysis, and video indexing using Vision Studio |
| 📓 [AI Vision Services Notebook](ai-vision/LabFiles/AI_vision_services_lab.ipynb) | Hands-on Jupyter notebook for computer vision capabilities |

### 📄 Phase 12: Content Understanding & Document Classification
**Location:** `content-understanding/`

| Implementation | Description |
|----------|-------------|
| 📄 [Content Understanding Lab Guide](content-understanding/README.md) | Azure AI Content Understanding for document classification and field extraction from bundled PDF files |
| 📓 [Classifier Notebook](content-understanding/classifier.ipynb) | Hands-on Jupyter notebook for building document classifiers and analyzers |
| 🐍 [Content Understanding Client](content-understanding/content_understanding_client.py) | Python client implementation for Azure AI Content Understanding API |
| 📋 [Sample Data](content-understanding/Data/) | Sample PDF documents for testing classification and extraction workflows |

### 🛡️ Phase 13: Responsible AI & Content Safety
**Location:** `responsible-ai/`

| Implementation | Description |
|----------|-------------|
| 🛡️ [Responsible AI Lab Guide](responsible-ai/README.md) | Comprehensive exploration of AI safety including manual and automated evaluations, content safety filters, PII detection and masking |
| 📊 [Evaluation Data](responsible-ai/Files/Evaluations/) | Manual and automated evaluation datasets for AI model testing |
| 🛡️ [Content Safety Data](responsible-ai/Files/Content_Safety/) | Bulk datasets for text and image moderation testing |
| 📚 [Sample Documents](responsible-ai/Files/Contoso/) | Corporate documents for PII detection and content analysis exercises |

---

## 🔧 Environment Setup

### 📋 System Requirements

**Essential Components:**
- 🐍 [Python 3.10+](https://www.python.org/downloads/) - Latest stable version
- ☁️ [Azure Subscription](https://ai.azure.com) - Active subscription with Azure AI Foundry access
- 💻 [Visual Studio Code](https://code.visualstudio.com/) - Recommended development environment
- 🛠️ [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) - For resource management
- 📦 [Git](https://git-scm.com/downloads) - Version control

**Knowledge Prerequisites:**
- ✅ Intermediate Python programming skills
- ✅ Basic understanding of machine learning concepts
- ✅ Familiarity with REST APIs and web services
- ✅ Experience with Azure services (recommended)

### 🔧 Development Environment Setup

**Visual Studio Code (Recommended)**
```powershell
# Install required extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

**Alternative: JupyterLab**
```powershell
# Launch JupyterLab
jupyter lab
```

---

## 🛠️ Troubleshooting & Support

### ⚡ Common Issues & Solutions

**Kernel Issues in VS Code:**
```powershell
# Refresh kernel registration
python -m ipykernel install --user --name=ai-foundry-lab --display-name="AI Foundry Lab"
# Reload VS Code: Ctrl+Shift+P → "Developer: Reload Window"
```

**Environment Activation Problems:**
```powershell
# Set PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify virtual environment
python -c "import sys; print(sys.executable)"
```

**Azure Authentication Issues:**
```powershell
# Recommended: Use Azure CLI authentication
az login --tenant YOUR_TENANT_ID
az account show

# Alternative: Clear cached credentials and re-login
az account clear
az login --tenant YOUR_TENANT_ID
az account show
```

> **Note:** If you see deprecation warnings about the Azure Account extension in VS Code, use `az login` in the terminal instead. The Azure Account extension for VS Code has been deprecated in favor of Azure CLI authentication.

### 📚 Additional Resources

- 📖 [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- 🎥 [Video Tutorials](https://learn.microsoft.com/en-us/shows/ai-show/)
- 💡 [Best Practices Guide](https://learn.microsoft.com/en-us/azure/ai-services/responsible-use-of-ai-overview)
- 🔍 [GitHub Issues](https://github.com/dhangerkapil/ai-foundry-e2e-lab/issues) - Report bugs or request features

---

## 🤝 Community & Contributions

### 🌟 Ways to Contribute
- 📝 **Documentation**: Improve clarity and add examples
- 🐛 **Bug Reports**: Help us identify and fix issues  
- 💡 **Feature Requests**: Suggest new capabilities and improvements
- 🔄 **Pull Requests**: Contribute code and enhancements

### 📋 Contribution Guidelines
Please review our [Contributing Guide](CONTRIBUTING.md) for:
- Code style and formatting standards
- Testing requirements and procedures
- Pull request process and review criteria  
- Community guidelines and expectations

---

## 📄 License & Attribution

**License:** MIT License  
**Repository:** [github.com/dhangerkapil/ai-foundry-e2e-lab](https://github.com/dhangerkapil/ai-foundry-e2e-lab)
