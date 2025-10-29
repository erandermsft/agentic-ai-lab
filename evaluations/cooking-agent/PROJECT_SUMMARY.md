# 🍳 Cooking AI Agent - Complete Project Summary

## Overview

This is a complete AI agent application built with Microsoft Agent Framework and GitHub Models, featuring:
- **Interactive cooking assistant** with recipe search and ingredient extraction
- **Comprehensive evaluation framework** to measure agent performance
- **Production-ready structure** with proper documentation and best practices

## Project Structure

```
cooking-agent/
├── cooking_agent.py          # Main agent application
├── evaluate.py                # Evaluation script
├── run_agent.py               # Agent runner for collecting responses
├── requirements.txt           # Agent dependencies (use --pre flag!)
├── requirements-eval.txt      # Evaluation dependencies
├── setup-eval.ps1             # Quick setup script for evaluation
│
├── README.md                  # Agent documentation
├── EVALUATION.md              # Evaluation framework guide
├── PROJECT_SUMMARY.md         # This file
│
├── test_queries.json          # 10 test queries
├── test_responses.json        # Sample responses with conversation histories
│
├── .env.example               # Environment variables template
└── .gitignore                 # Git exclusions
```

## Quick Start Guide

### 1. Run the Cooking Agent

```bash
# Install dependencies (note: --pre flag is REQUIRED!)
pip install -r requirements.txt --pre

# Set your GitHub token
$env:GITHUB_TOKEN = "your-github-token-here"

# Run the agent
python cooking_agent.py
```

**Try these commands:**
- "Find pasta recipes"
- "What ingredients do I need for carbonara?"
- "Suggest quick recipes"

### 2. Evaluate the Agent

```bash
# Quick setup (installs dependencies and checks token)
.\setup-eval.ps1

# Or manual setup
pip install -r requirements-eval.txt

# Run evaluation
python evaluate.py
```

**Results location:** `evaluation_results/`
- `evaluation_results.json` - Detailed row-level scores
- `metrics.json` - Aggregate metrics summary

## Technology Stack

### AI Agent Framework
- **SDK**: Microsoft Agent Framework (Python)
- **Model**: gpt-4.1-mini via GitHub Models
- **Host**: GitHub Models (free tier)
- **Features**: 
  - Tool/function calling
  - Multi-turn conversation with threads
  - Async/await for performance

### Evaluation Framework
- **SDK**: Azure AI Evaluation
- **Evaluators**:
  - ToolCallAccuracyEvaluator (code-based)
  - RelevanceEvaluator (AI-assisted)
  - CoherenceEvaluator (AI-assisted)
- **Model for Evaluation**: gpt-4.1-mini via GitHub Models

### Agent Tools (Functions)
1. **search_recipes** - Search recipe database by keyword
2. **extract_ingredients** - Get detailed ingredient lists
3. **get_recipe_suggestions** - Provide dietary recommendations

## Key Features

### Agent Capabilities
✅ Natural language recipe search
✅ Ingredient extraction with instructions
✅ Dietary preference suggestions (quick, vegetarian, meat, dessert)
✅ Multi-turn conversations with context
✅ Friendly, enthusiastic cooking assistant personality

### Evaluation Capabilities
✅ Automated performance measurement
✅ Three comprehensive metrics (tool accuracy, relevance, coherence)
✅ Row-level and aggregate scoring
✅ Sample test dataset included
✅ Easy integration with CI/CD pipelines

## Evaluation Metrics Explained

| Metric | Type | Range | What It Measures |
|--------|------|-------|------------------|
| **Tool Call Accuracy** | Code-based | 0-1 | Correct tool selection with valid parameters |
| **Relevance** | AI-assisted | 1-5 | Response relevance to cooking queries |
| **Coherence** | AI-assisted | 1-5 | Clear, logical communication |

### Sample Results

```json
{
  "tool_call_accuracy.score": 1.0,     // Perfect tool selection
  "relevance.score": 4.8,               // Highly relevant responses
  "coherence.score": 4.9                // Very clear communication
}
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Input                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Cooking Agent (Microsoft Agent Framework)           │
│              Model: gpt-4.1-mini (GitHub Models)             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Tool Selection & Execution                  │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │search_recipes │  │extract_        │  │get_recipe_    │  │
│  │               │  │ingredients     │  │suggestions    │  │
│  └───────────────┘  └────────────────┘  └───────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Response Generation                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                     User Output                              │
└─────────────────────────────────────────────────────────────┘
```

## Why These Choices?

### Model: gpt-4.1-mini
- ✅ Free tier available on GitHub Models
- ✅ Excellent balance of quality and cost
- ✅ Fast response times for interactive apps
- ✅ Strong function calling capabilities
- ✅ Good instruction following

### SDK: Microsoft Agent Framework
- ✅ Native GitHub Models support
- ✅ Built-in tool/function calling
- ✅ Thread-based conversation management
- ✅ Async/await for better performance
- ✅ Production-ready and actively maintained

### Evaluation: Azure AI Evaluation
- ✅ Built-in evaluators for common metrics
- ✅ Unified evaluate() API for batch processing
- ✅ Automatic metric aggregation
- ✅ Support for custom evaluators
- ✅ Industry-standard evaluation framework

## Customization Guide

### Add More Recipes

Edit `RECIPES_DB` in `cooking_agent.py`:

```python
RECIPES_DB = {
    "your-recipe-id": {
        "name": "Recipe Name",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": "Step by step",
        "prep_time": "10 min",
        "cook_time": "20 min",
        "servings": 4
    }
}
```

### Add New Tools

```python
def get_nutritional_info(recipe_name: str) -> str:
    """Get nutritional information."""
    # Your implementation
    pass

agent = ChatAgent(
    tools=[search_recipes, extract_ingredients, get_recipe_suggestions, get_nutritional_info]
)
```

### Add Custom Evaluators

See `EVALUATION.md` for detailed examples of:
- Code-based evaluators (objective metrics)
- Prompt-based evaluators (LLM as judge)

### Change Models

**For the agent:**
```python
chat_client = OpenAIChatClient(
    async_client=openai_client,
    model_id="gpt-4.1"  # or gpt-4o, o1-mini, etc.
)
```

**For evaluation:**
```python
model_config = OpenAIModelConfiguration(
    model="gpt-4.1",  # or any GitHub Model
    base_url="https://models.github.ai/inference",
    api_key=github_token
)
```

## Common Tasks

### Collect Fresh Responses

```bash
# Make sure agent dependencies are installed
pip install -r requirements.txt --pre

# Run the agent with test queries
python run_agent.py

# This updates test_responses.json
```

### Run Evaluation

```bash
# Install evaluation dependencies
pip install -r requirements-eval.txt

# Run evaluation
python evaluate.py

# View results
cat evaluation_results/metrics.json
```

### Continuous Evaluation

Add to your CI/CD pipeline:

```yaml
- name: Run Agent Evaluation
  run: |
    pip install -r requirements-eval.txt
    python evaluate.py
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

### Agent Issues

| Problem | Solution |
|---------|----------|
| Import errors | Install with `--pre` flag: `pip install -r requirements.txt --pre` |
| GITHUB_TOKEN not found | Set environment variable or enter when prompted |
| Rate limits | GitHub free tier has limits; wait or upgrade |

### Evaluation Issues

| Problem | Solution |
|---------|----------|
| azure-ai-evaluation not found | Run `pip install -r requirements-eval.txt` |
| No GITHUB_TOKEN | Only affects AI evaluators; ToolCallAccuracy still works |
| Invalid JSONL | Check data format; no timestamps allowed |

## Learning Path

1. **Understand the Agent** (30 min)
   - Read `README.md`
   - Run `cooking_agent.py`
   - Try different queries

2. **Explore Agent Code** (30 min)
   - Study `cooking_agent.py`
   - Understand tool implementations
   - Review conversation thread usage

3. **Learn Evaluation** (45 min)
   - Read `EVALUATION.md`
   - Run `evaluate.py`
   - Analyze results

4. **Customize** (1-2 hours)
   - Add recipes or tools
   - Create custom evaluators
   - Experiment with different models

## Production Considerations

### Before Production Deployment

- [ ] Replace sample recipe database with real data source
- [ ] Add error handling and retry logic
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Set up proper authentication
- [ ] Use Azure AI Foundry for production (higher limits)
- [ ] Add conversation history persistence
- [ ] Implement user session management
- [ ] Add input validation and sanitization
- [ ] Set up automated evaluation in CI/CD

### Scaling Recommendations

- Use Azure AI Foundry models for production
- Implement caching for common queries
- Add load balancing for multiple instances
- Monitor token usage and costs
- Set up alerting for evaluation metrics

## Resources

### Documentation
- [EVALUATION.md](EVALUATION.md) - Comprehensive evaluation guide
- [README.md](README.md) - Agent usage and setup

### External Resources
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [GitHub Models](https://github.com/marketplace/models)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk)
- [Azure AI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)

## Success Metrics

This project demonstrates:
✅ End-to-end AI agent development
✅ Production-ready evaluation framework
✅ Best practices for agent architecture
✅ Comprehensive documentation
✅ Easy setup and deployment

## Next Steps

1. **Try the agent**: `python cooking_agent.py`
2. **Run evaluation**: `python evaluate.py`
3. **Customize for your use case**: Add recipes, tools, or evaluators
4. **Integrate with CI/CD**: Automate evaluation
5. **Deploy to production**: Scale with Azure AI Foundry

---

**Built with ❤️ using Microsoft Agent Framework and GitHub Models**
