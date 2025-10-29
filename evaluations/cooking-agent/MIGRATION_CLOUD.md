# 🌩️ Migration to Azure AI Foundry Cloud Evaluation

## Summary of Changes

This document summarizes the migration from local evaluation (azure-ai-evaluation) to cloud-based evaluation (azure-ai-projects).

## What Changed

### 1. Evaluation Approach

**Before (Local Evaluation)**:
- Used `azure-ai-evaluation` package
- Ran evaluations locally using `evaluate()` API
- Results saved to `evaluation_results/` directory
- Required local compute resources
- Used ToolCallAccuracyEvaluator, RelevanceEvaluator, CoherenceEvaluator

**After (Cloud Evaluation)**:
- Uses `azure-ai-projects` package
- Submits evaluation jobs to Azure AI Foundry
- Results stored in Azure AI project (cloud)
- Scalable cloud compute
- Uses built-in evaluators: Relevance, Coherence, Fluency

### 2. Files Modified

#### `evaluate.py`
- **Old**: Local evaluation with azure-ai-evaluation SDK
- **New**: Cloud evaluation with AIProjectClient
- **Changes**:
  - Removed local evaluator instantiation
  - Added dataset upload to Azure
  - Added cloud evaluation submission
  - Simplified data preparation (removed conversation history)
  - Added PROJECT_ENDPOINT and MODEL_ENDPOINT configuration

#### `requirements-eval.txt`
```diff
- azure-ai-evaluation>=1.0.0
+ azure-ai-projects>=1.0.0
  azure-identity>=1.14.0
```

#### `.env.example`
```diff
  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
  AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
+ PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project-id>
+ MODEL_ENDPOINT=https://<account>.services.ai.azure.com
```

### 3. New Files Created

#### `EVALUATION_CLOUD.md`
- Comprehensive guide for cloud evaluation
- Prerequisites and setup instructions
- Detailed configuration steps
- Troubleshooting guide
- Benefits and use cases

#### `setup-cloud-eval.ps1`
- PowerShell setup script
- Automated dependency installation
- Environment configuration validation
- Authentication testing

### 4. Files Updated

#### `README.md`
- Updated evaluation section to reference cloud evaluation
- Added quick start guide for cloud evaluation
- Updated metrics description
- Added reference to EVALUATION_CLOUD.md

## New Requirements

### Azure Resources

1. **Azure AI Foundry Project**
   - Create at https://ai.azure.com
   - Note the PROJECT_ENDPOINT

2. **Storage Account**
   - Must be connected to Azure AI project
   - Required for dataset uploads

3. **Azure OpenAI Resource**
   - Deploy a GPT model (e.g., gpt-4o-mini)
   - Note the AZURE_OPENAI_ENDPOINT

### Environment Variables

Four environment variables now required:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project-id>
MODEL_ENDPOINT=https://<account>.services.ai.azure.com
```

## Workflow Changes

### Old Workflow (Local)
```
1. python run_agent.py → test_responses.json
2. python evaluate.py → evaluation_results/ (local files)
3. View results in local JSON files
```

### New Workflow (Cloud)
```
1. python run_agent.py → test_responses.json
2. python evaluate.py → Submit to Azure
3. View results in Azure AI Foundry portal
   - Navigate to https://ai.azure.com
   - Go to your project → Evaluation tab
   - See metrics, visualizations, history
```

## Benefits of Cloud Evaluation

### Scalability
- ✅ No local compute limitations
- ✅ Handle large datasets
- ✅ Parallel evaluation execution

### Centralization
- ✅ All results in one place
- ✅ Historical tracking
- ✅ Version control for datasets

### Collaboration
- ✅ Team-wide access
- ✅ Shared results
- ✅ Role-based permissions

### Integration
- ✅ CI/CD pipeline integration
- ✅ Azure ML workflows
- ✅ Automated quality gates

## Breaking Changes

### API Changes

**Data Format**:
- Removed `conversation` field from evaluation data
- Now only `query` and `response` fields

**Evaluators**:
- Removed ToolCallAccuracyEvaluator (not available in cloud)
- Using built-in evaluators via registry IDs

**Output**:
- No longer creates `evaluation_results/` directory
- Results only in Azure portal

### Configuration

**Required New Settings**:
- `PROJECT_ENDPOINT` - Azure AI Foundry project
- `MODEL_ENDPOINT` - Azure AI services endpoint

**Authentication**:
- Must run `az login` or configure managed identity
- DefaultAzureCredential used for all Azure connections

## Migration Steps for Existing Users

1. **Install New Dependencies**
   ```bash
   pip install -r requirements-eval.txt
   ```

2. **Update .env File**
   ```bash
   # Add these new variables
   PROJECT_ENDPOINT=https://your-account.services.ai.azure.com/api/projects/your-project-id
   MODEL_ENDPOINT=https://your-account.services.ai.azure.com
   ```

3. **Authenticate with Azure**
   ```bash
   az login
   ```

4. **Run Setup Script** (Optional)
   ```bash
   ./setup-cloud-eval.ps1
   ```

5. **Submit First Evaluation**
   ```bash
   python evaluate.py
   ```

6. **View Results**
   - Open https://ai.azure.com
   - Navigate to your project
   - Click "Evaluation" tab

## Backward Compatibility

⚠️ **Not Backward Compatible**

The new cloud evaluation approach is not compatible with the old local evaluation:

- Different SDK packages
- Different API calls
- Different result storage
- Different evaluators

If you need local evaluation, keep the old version of `evaluate.py` or use the `azure-ai-evaluation` package separately.

## Documentation References

- **EVALUATION_CLOUD.md** - Complete cloud evaluation guide
- **setup-cloud-eval.ps1** - Automated setup script
- **README.md** - Updated with cloud evaluation quick start
- **.env.example** - Environment variable template

## Support

For issues or questions:

1. Check **EVALUATION_CLOUD.md** troubleshooting section
2. Review [Azure AI Foundry Cloud Evaluation Docs](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/cloud-evaluation)
3. Verify environment configuration with `setup-cloud-eval.ps1 -Test`

## Next Steps

1. ✅ Review EVALUATION_CLOUD.md
2. ✅ Run setup-cloud-eval.ps1
3. ✅ Configure .env file
4. ✅ Authenticate: az login
5. ✅ Submit evaluation: python evaluate.py
6. ✅ View results in Azure portal
