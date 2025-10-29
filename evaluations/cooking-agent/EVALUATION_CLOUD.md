# 🌩️ Cloud Evaluation with Azure AI Foundry

This guide covers the **cloud-based evaluation** approach using Azure AI Foundry SDK's evaluation service.

## Why Cloud Evaluation?

Instead of running evaluations locally, cloud evaluation offers:

✅ **Scalability**: Handle large datasets without local compute limitations  
✅ **Centralization**: All results logged to Azure AI Foundry project  
✅ **Visibility**: View results in Azure portal with rich visualizations  
✅ **History**: Track evaluation runs over time  
✅ **Collaboration**: Share results with team members  
✅ **Integration**: Seamlessly connects with Azure ML pipelines  

## Prerequisites

### 1. Azure AI Foundry Project

Create a project at [ai.azure.com](https://ai.azure.com):

1. Navigate to Azure AI Foundry
2. Create a new project (or use existing)
3. Note your **project endpoint**

### 2. Storage Account

Ensure your Azure AI project has a connected storage account:

1. In Azure portal, navigate to your AI Foundry hub
2. Check **Storage** under Settings
3. If not connected, add a storage account

### 3. Azure OpenAI Deployment

Deploy a GPT model for evaluators:

1. Create Azure OpenAI resource (or use existing)
2. Deploy `gpt-4o-mini` (or other GPT model)
3. Note your deployment name

### 4. Authentication

Authenticate with Azure:

```bash
az login
```

Or configure managed identity if running in Azure.

## Configuration

### Environment Variables

Create/update `.env` file:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_KEY=your-api-key-here

# Azure AI Foundry Project Configuration
# Format: https://<account>.services.ai.azure.com/api/projects/<project-id>
PROJECT_ENDPOINT=https://your-account.services.ai.azure.com/api/projects/your-project-id

# Model Endpoint
# Format: https://<account>.services.ai.azure.com
MODEL_ENDPOINT=https://your-account.services.ai.azure.com
```

**Finding your values:**

**PROJECT_ENDPOINT**:
1. Open [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project
3. Go to **Settings** → **Connection string**
4. Copy the endpoint URL

**MODEL_ENDPOINT**:
1. In Azure AI Foundry project
2. Go to **Overview**
3. Copy the base services URL (without `/api/projects/...`)

**AZURE_OPENAI_API_KEY**:
1. Go to Azure portal
2. Navigate to your Azure OpenAI resource
3. Go to **Keys and Endpoint**
4. Copy Key 1 or Key 2

### Install Dependencies

```bash
pip install -r requirements-eval.txt
```

This installs:
- `azure-ai-projects` - Cloud evaluation SDK
- `azure-identity` - Azure authentication

## Usage

### Step 1: Generate Test Responses

Run the agent with test queries:

```bash
python run_agent.py
```

This creates `test_responses.json` with 10 agent responses.

### Step 2: Submit Cloud Evaluation

Run the evaluation script:

```bash
python evaluate.py
```

### What Happens

1. **Data Preparation**: Converts `test_responses.json` → `evaluation_data.jsonl`
2. **Project Connection**: Connects to Azure AI Foundry project
3. **Dataset Upload**: Uploads JSONL to Azure (versioned as `cooking-agent-test-data v1.0`)
4. **Evaluator Configuration**: Sets up 3 evaluators:
   - Relevance (measures response relevance)
   - Coherence (assesses logical structure)
   - Fluency (evaluates language quality)
5. **Job Submission**: Submits evaluation job to cloud
6. **Returns ID**: Get evaluation ID for tracking

### Example Output

```
======================================================================
🔬 Cooking Agent Cloud Evaluation
======================================================================

📊 Preparing evaluation data from test_responses.json...
✅ Created evaluation dataset: evaluation_data.jsonl (10 records)

🔧 Configuring Azure AI Foundry project...
✅ Project endpoint: https://...services.ai.azure.com/api/projects/...
✅ Model deployment: gpt-4o-mini

🌐 Connecting to Azure AI Foundry project...
✅ Connected to Azure AI Foundry project

📤 Uploading evaluation dataset...
✅ Dataset uploaded: cooking-agent-test-data (v1.0)
   Dataset ID: azureml://...

📋 Configuring evaluators...
✅ Configured 6 evaluators:
   Quality Evaluators:
   - relevance
   - coherence
   - fluency
   Agent Evaluators:
   - intent_resolution
   - tool_call_accuracy
   - task_adherence

🚀 Submitting cloud evaluation...
✅ Evaluation submitted successfully!
======================================================================
📊 Evaluation Details:
   Name: Cooking Agent Evaluation
   Status: NotStarted
   ID: ...
======================================================================

🎯 Next Steps:
   1. View evaluation progress in Azure AI Foundry portal
   2. Check evaluation results under the Evaluation tab
   3. Monitor status: NotStarted

💡 Tip: Results will be automatically logged to your Azure AI project
```

### Step 3: View Results in Portal

1. Open [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project
3. Click **Evaluation** tab in left sidebar
4. Find "Cooking Agent Evaluation" in the list
5. Click to view:
   - Overall metrics (avg relevance, coherence, fluency)
   - Per-response scores
   - Detailed evaluator outputs
   - Execution logs

## Evaluators

### Quality Evaluators

All evaluators use the configured GPT model to assess responses:

#### 1. Relevance Evaluator
- **Measures**: How well response addresses the query
- **Score Range**: 1-5
- **Model ID**: `EvaluatorIds.RELEVANCE`

#### 2. Coherence Evaluator
- **Measures**: Logical structure and flow of response
- **Score Range**: 1-5
- **Model ID**: `EvaluatorIds.COHERENCE`

#### 3. Fluency Evaluator
- **Measures**: Grammatical correctness and natural language quality
- **Score Range**: 1-5
- **Model ID**: `EvaluatorIds.FLUENCY`

### Agent-Specific Evaluators

These evaluators are designed specifically for agentic workflows:

#### 4. Intent Resolution Evaluator
- **Measures**: How well the agent identifies and understands user's request
- **Evaluates**: Intent detection, clarifying questions, scope awareness
- **Score Range**: 1-5 (Pass/Fail with threshold=3)
- **Model ID**: `EvaluatorIds.INTENT_RESOLUTION`
- **Best for**: Conversational agents that need to understand user intent

#### 5. Tool Call Accuracy Evaluator
- **Measures**: Accuracy and efficiency of tool calls made by the agent
- **Evaluates**:
  - Relevance and helpfulness of tools invoked
  - Correctness of parameters used
  - Missing or excessive tool calls
- **Score Range**: 1-5 (Pass/Fail with threshold=3)
- **Model ID**: `EvaluatorIds.TOOL_CALL_ACCURACY`
- **Best for**: Agents that use multiple tools to complete tasks
- **Supports**: Function tools, File Search, Azure AI Search, Bing Grounding, Code Interpreter, OpenAPI, and more

#### 6. Task Adherence Evaluator
- **Measures**: How well agent stays on track to complete assigned tasks
- **Evaluates**: Adherence to system instructions and task scope
- **Score Range**: 1-5 (Pass/Fail with threshold=3)
- **Model ID**: `EvaluatorIds.TASK_ADHERENCE`
- **Best for**: Task-oriented agents that need to follow specific instructions

### Data Mapping

Each evaluator receives:
```json
{
  "query": "${data.query}",     // User's question
  "response": "${data.response}" // Agent's answer
}
```

## Troubleshooting

### Error: PROJECT_ENDPOINT not found

**Solution**: Set environment variable in `.env`:
```bash
PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project-id>
```

### Error: Failed to upload dataset

**Possible causes**:
1. Storage account not connected to project
2. Insufficient permissions
3. Dataset name/version already exists

**Solution**:
- Check storage account in Azure portal
- Verify you have Contributor role on project
- Change dataset version in `evaluate.py`

### Error: Authentication failed

**Solution**: Run `az login` and try again:
```bash
az login
python evaluate.py
```

### Error: Model deployment not found

**Solution**: Verify deployment name matches:
```bash
# Check deployments in Azure OpenAI Studio
# Update .env with correct name
AZURE_OPENAI_DEPLOYMENT=your-actual-deployment-name
```

## Benefits of Cloud Evaluation

### For Development
- ✅ No local compute needed
- ✅ Consistent evaluation environment
- ✅ Automatic result storage
- ✅ Historical tracking

### For Teams
- ✅ Centralized results
- ✅ Shared visibility
- ✅ Role-based access
- ✅ Audit trails

### For Production
- ✅ Scalable to thousands of evaluations
- ✅ Integration with CI/CD pipelines
- ✅ Automated quality gates
- ✅ Compliance and governance

## Next Steps

1. **Automate**: Integrate `evaluate.py` into CI/CD pipeline
2. **Expand**: Add more evaluators (groundedness, safety, etc.)
3. **Monitor**: Set up alerts for metric degradation
4. **Compare**: Run evaluations on model updates to track improvements
5. **Customize**: Create custom evaluators for domain-specific metrics

## Reference

- [Azure AI Foundry Cloud Evaluation Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/cloud-evaluation)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [Built-in Evaluators](https://learn.microsoft.com/azure/ai-studio/how-to/evaluate-generative-ai-app)
