# 🔬 Evaluation Framework for Cooking AI Agent

This directory contains a comprehensive evaluation framework for the Cooking AI Agent using Azure AI Evaluation SDK.

## Overview

The evaluation framework assesses three key aspects of the cooking agent's performance:

1. **Tool Call Accuracy** - Validates that the agent selects the correct tools with appropriate parameters
2. **Relevance** - Ensures responses are relevant to cooking queries
3. **Coherence** - Measures how clearly and logically the agent communicates

## Files

- **`evaluate.py`** - Main evaluation script
- **`run_agent.py`** - Agent runner to collect responses (optional if you have responses)
- **`test_queries.json`** - Test dataset with 10 cooking-related queries
- **`test_responses.json`** - Sample agent responses with conversation histories
- **`requirements-eval.txt`** - Evaluation dependencies

## Setup

### 1. Install Evaluation Dependencies

```bash
pip install -r requirements-eval.txt
```

### 2. Set GitHub Token (Required for AI Evaluators)

The RelevanceEvaluator and CoherenceEvaluator require a GitHub token to use GitHub Models:

```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN = "your-github-token-here"

# Linux/macOS
export GITHUB_TOKEN=your-github-token-here
```

## Running Evaluation

### Quick Start

Run the evaluation with the provided test data:

```bash
python evaluate.py
```

### What Happens

1. **Data Preparation**: Converts `test_responses.json` to JSONL format required by the evaluate() API
2. **Model Configuration**: Sets up gpt-4.1-mini via GitHub Models for AI-assisted evaluation
3. **Evaluator Creation**: Initializes three evaluators:
   - `ToolCallAccuracyEvaluator` (code-based)
   - `RelevanceEvaluator` (AI-assisted)
   - `CoherenceEvaluator` (AI-assisted)
4. **Evaluation Execution**: Runs all evaluators in a single unified call
5. **Results Aggregation**: Automatically computes summary metrics

### Evaluation Output

Results are saved to `evaluation_results/`:

```
evaluation_results/
├── evaluation_results.json    # Row-level scores for each query
└── metrics.json                # Aggregate metrics summary
```

### Example Output

```
📊 Evaluation Results Summary:
----------------------------------------------------------------------
  tool_call_accuracy.score: 1.0000
  relevance.score: 4.5000
  coherence.score: 4.8000
----------------------------------------------------------------------

📁 Detailed results saved to: evaluation_results/
   - evaluation_results.json: Row-level evaluation data
   - metrics.json: Aggregate metrics summary
```

## Collecting Fresh Responses

If you want to evaluate your agent with fresh responses:

### 1. Install Agent Dependencies

```bash
pip install -r requirements.txt --pre
```

Note: The `--pre` flag is required for agent-framework.

### 2. Run the Agent Runner

```bash
python run_agent.py
```

This will:
- Load queries from `test_queries.json`
- Run your cooking agent with each query
- Collect responses with full conversation histories
- Save to `test_responses.json`

### 3. Run Evaluation

```bash
python evaluate.py
```

## Evaluation Metrics Explained

### ToolCallAccuracyEvaluator

**What it measures**: Validates that the agent calls the correct tools with appropriate parameters.

**Score range**: Binary (0 or 1)
- **1.0** = Correct tool called with valid parameters
- **0.0** = Wrong tool or invalid parameters

**Example**:
- ✅ Query: "Find pasta recipes" → Calls `search_recipes(query="pasta")`
- ❌ Query: "Find pasta recipes" → Calls `extract_ingredients(recipe_name="pasta")`

### RelevanceEvaluator

**What it measures**: Ensures responses are relevant to the user's cooking queries.

**Score range**: 1-5 scale
- **5** = Highly relevant, directly addresses the query
- **4** = Mostly relevant with minor tangents
- **3** = Somewhat relevant but incomplete
- **2** = Marginally relevant
- **1** = Not relevant

**Example**:
- ✅ Query: "Suggest quick recipes" → Response lists recipes under 25 minutes (Score: 5)
- ❌ Query: "Suggest quick recipes" → Response talks about kitchen equipment (Score: 1)

### CoherenceEvaluator

**What it measures**: Assesses how clearly and logically the agent communicates recipe information.

**Score range**: 1-5 scale
- **5** = Perfectly coherent, well-structured, easy to follow
- **4** = Mostly coherent with minor issues
- **3** = Somewhat coherent but confusing in places
- **2** = Difficult to follow
- **1** = Incoherent or contradictory

**Example**:
- ✅ Clear structure: "Found 1 recipe: Pasta Carbonara (10 min prep, 15 min cook)..." (Score: 5)
- ❌ Jumbled: "Pasta cook 10 carbonara min recipes found prep 15..." (Score: 1)

## Understanding Results

### Row-Level Results

Each query gets individual scores from each evaluator:

```json
{
  "query_id": "q1",
  "query": "Find me some pasta recipes",
  "response": "Found 1 recipe...",
  "tool_call_accuracy.score": 1.0,
  "relevance.score": 5.0,
  "coherence.score": 5.0
}
```

### Aggregate Metrics

Average scores across all queries:

```json
{
  "tool_call_accuracy.score": 0.95,
  "relevance.score": 4.6,
  "coherence.score": 4.8
}
```

## Customization

### Add Custom Evaluators

You can extend the evaluation with custom evaluators:

#### Code-Based Evaluator Example

```python
class RecipeCountEvaluator:
    """Counts recipes mentioned in the response."""
    
    def __init__(self):
        pass
    
    def __call__(self, *, response: str, **kwargs):
        # Simple keyword counting
        count = response.lower().count("recipe")
        return {"recipe_count": count}

# Add to evaluators dict
evaluators["recipe_count"] = RecipeCountEvaluator()
evaluator_config["recipe_count"] = {
    "column_mapping": {
        "response": "${data.response}"
    }
}
```

#### Prompt-Based Evaluator Example

```python
from promptflow.client import load_flow

class FriendlinessEvaluator:
    """Evaluates how friendly the cooking agent sounds."""
    
    def __init__(self, model_config):
        self._flow = load_flow(
            source="friendliness.prompty",
            model={"configuration": model_config}
        )
    
    def __call__(self, *, response: str, **kwargs):
        result = self._flow(response=response)
        return json.loads(result)
```

### Change Test Data

Replace `test_queries.json` and `test_responses.json` with your own data:

**test_queries.json format**:
```json
{
  "queries": [
    {
      "id": "q1",
      "query": "Your test query here"
    }
  ]
}
```

**test_responses.json format**:
```json
{
  "responses": [
    {
      "query_id": "q1",
      "query": "Your test query",
      "response": "Agent response",
      "conversation_history": [...]
    }
  ]
}
```

### Use Different Models

Change the model configuration in `evaluate.py`:

```python
model_config = OpenAIModelConfiguration(
    type="openai",
    model="gpt-4.1",  # or "gpt-4o", "o1-mini", etc.
    base_url="https://models.github.ai/inference",
    api_key=github_token
)
```

## Troubleshooting

### "GITHUB_TOKEN not found"
- Set the environment variable before running evaluation
- Only affects AI-assisted evaluators (Relevance, Coherence)
- ToolCallAccuracyEvaluator will still work without it

### "Module not found" errors
```bash
# Install evaluation dependencies
pip install -r requirements-eval.txt

# If running the agent too
pip install -r requirements.txt --pre
```

### "Invalid JSONL format"
- Ensure no timestamps in the data
- Check that all required fields are present
- Validate JSON syntax

### Rate limits
- GitHub Models free tier has rate limits
- Consider using Azure OpenAI for production evaluations
- Add delays between evaluations if needed

## Best Practices

1. **Start with sample data** - Use the provided test data first
2. **Collect diverse queries** - Cover all agent capabilities
3. **Run regularly** - Evaluate after each agent change
4. **Track metrics over time** - Monitor improvements/regressions
5. **Set thresholds** - Define minimum acceptable scores
6. **Review failures** - Investigate low-scoring responses

## Next Steps

- **CI/CD Integration**: Add evaluation to your GitHub Actions workflow
- **Baseline Comparison**: Track scores across versions
- **A/B Testing**: Compare different agent configurations
- **Extended Metrics**: Add domain-specific evaluators
- **Human Evaluation**: Combine with human reviews for subjective metrics

## Resources

- [Azure AI Evaluation SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk)
- [GitHub Models](https://github.com/marketplace/models)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
