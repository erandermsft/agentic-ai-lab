# 🍳 Cooking AI Agent

An interactive console AI agent application that helps with recipe search and ingredient extraction using GitHub Models and Microsoft Agent Framework.

## Features

- **Recipe Search**: Find recipes by name or ingredients
- **Ingredient Extraction**: Get detailed ingredient lists for specific recipes
- **Recipe Suggestions**: Get recommendations based on dietary preferences (quick, vegetarian, meat, dessert)
- **Interactive Console**: Natural conversation with context preservation
- **GitHub Models Integration**: Uses free-tier GitHub Models for AI capabilities

## Prerequisites

- Python 3.10 or higher
- GitHub Personal Access Token (PAT) with model access
- Internet connection

## Setup

### 1. Install Dependencies

**Important**: The `--pre` flag is REQUIRED while Agent Framework is in preview.

```bash
pip install -r requirements.txt --pre
```

Or install packages individually:

```bash
pip install agent-framework-azure-ai --pre
pip install openai python-dotenv
```

### 2. Get GitHub Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Cooking Agent")
4. Select appropriate scopes (no special scopes required for model access)
5. Click "Generate token" and copy it

### 3. Set Environment Variable (Optional)

You can either:

**Option A**: Set environment variable
```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN = "your-github-token-here"

# Windows (CMD)
set GITHUB_TOKEN=your-github-token-here

# Linux/macOS
export GITHUB_TOKEN=your-github-token-here
```

**Option B**: Create a `.env` file
```bash
echo "GITHUB_TOKEN=your-github-token-here" > .env
```

**Option C**: Enter token when prompted (the app will ask if not found)

## Usage

Run the cooking agent:

```bash
python cooking_agent.py
```

### Example Interactions

```
You: Find me pasta recipes
Agent: [Searches and returns pasta recipes with prep/cook times]

You: What ingredients do I need for carbonara?
Agent: [Extracts detailed ingredient list and instructions]

You: Suggest some quick recipes
Agent: [Provides recipes that can be made in 15 minutes or less]

You: I want something with chicken
Agent: [Searches for chicken-based recipes]
```

### Available Commands

- Type your cooking questions naturally
- Type `exit`, `quit`, `bye`, or `goodbye` to end the session
- Press `Ctrl+C` to interrupt

## How It Works

### AI Model

This app uses **gpt-4.1-mini** from GitHub Models because:
- ✅ Free tier available (great for getting started)
- ✅ Good balance of quality and cost
- ✅ Fast response times for interactive applications
- ✅ Strong instruction following and function calling capabilities

### Agent Framework

The app uses **Microsoft Agent Framework** which provides:
- 🤖 Flexible agent architecture
- 🔧 Built-in tool/function calling support
- 💬 Thread-based conversation management
- 🔄 Async/await support for performance
- 🎯 Multi-turn conversation context

### Tools (Functions)

The agent has three tools:

1. **search_recipes**: Searches recipe database by keyword
2. **extract_ingredients**: Gets detailed ingredient lists
3. **get_recipe_suggestions**: Provides recommendations based on preferences

## Architecture

```
User Input
    ↓
Cooking Agent (gpt-4.1-mini via GitHub Models)
    ↓
Tool Selection & Execution
    ↓
├─ search_recipes()
├─ extract_ingredients()
└─ get_recipe_suggestions()
    ↓
Response Generation
    ↓
User Output
```

## Customization

### Add More Recipes

Edit the `RECIPES_DB` dictionary in `cooking_agent.py`:

```python
RECIPES_DB = {
    "your-recipe-id": {
        "name": "Recipe Name",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": "Step by step instructions",
        "prep_time": "10 min",
        "cook_time": "20 min",
        "servings": 4
    }
}
```

### Change AI Model

Modify the `model_id` in the code:

```python
chat_client = OpenAIChatClient(
    async_client=openai_client,
    model_id="gpt-4.1"  # or other supported models
)
```

Available GitHub Models:
- `gpt-4.1-mini` (recommended for this app)
- `gpt-4.1`
- `gpt-4.1-nano`
- `gpt-4o-mini`
- `gpt-4o`
- And many more (see [GitHub Models](https://github.com/marketplace/models))

### Extend Functionality

Add new tools to the agent:

```python
def get_nutritional_info(recipe_name: str) -> str:
    """Get nutritional information for a recipe."""
    # Your implementation
    pass

agent = ChatAgent(
    # ... other settings
    tools=[search_recipes, extract_ingredients, get_recipe_suggestions, get_nutritional_info],
)
```

## Troubleshooting

### "GITHUB_TOKEN not found"
- Set the environment variable or create a `.env` file
- Or simply enter your token when prompted by the app

### "Failed to initialize agent"
- Verify your GitHub token is valid
- Check internet connection
- Ensure you have access to GitHub Models (available for all GitHub users)

### "Rate limit exceeded"
- GitHub Models free tier has rate limits
- Wait a few minutes and try again
- Consider upgrading to a paid tier for higher limits

### Import errors
- Make sure you installed with `--pre` flag: `pip install -r requirements.txt --pre`
- Verify Python version is 3.10 or higher: `python --version`

## Evaluation Framework

This project includes a comprehensive **cloud-based evaluation framework** using Azure AI Foundry SDK to assess the cooking agent's performance. See **[EVALUATION_CLOUD.md](EVALUATION_CLOUD.md)** for complete details.

### Quick Cloud Evaluation

```bash
# 1. Setup cloud evaluation environment
./setup-cloud-eval.ps1

# 2. Configure .env with Azure AI Foundry endpoints
# PROJECT_ENDPOINT, MODEL_ENDPOINT, AZURE_OPENAI_ENDPOINT

# 3. Authenticate with Azure
az login

# 4. Generate test responses
python run_agent.py

# 5. Submit cloud evaluation
python evaluate.py

# 6. View results in Azure AI Foundry portal
# Navigate to https://ai.azure.com → Your Project → Evaluation tab
```

The cloud evaluation framework measures:
- **Relevance** (1-5) - Response relevance to queries  
- **Coherence** (1-5) - Logical structure and clarity
- **Fluency** (1-5) - Grammatical correctness
- **Intent Resolution** (1-5) - Understanding of user intent (agent-specific)
- **Tool Call Accuracy** (1-5) - Accuracy of tool selections and parameters (agent-specific)
- **Task Adherence** (1-5) - Following instructions and task scope (agent-specific)

Results are automatically logged to your Azure AI Foundry project with rich visualizations and historical tracking.

**Documentation**:
- **[EVALUATION_CLOUD.md](EVALUATION_CLOUD.md)** - Complete cloud evaluation guide
- **[AGENT_EVALUATORS.md](AGENT_EVALUATORS.md)** - Detailed agent evaluator documentation

## Learning Resources

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk)
- [Azure AI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/)

## License

This project is provided as a sample application. Feel free to modify and extend it for your needs.

## Contributing

This is a sample application for educational purposes. Feel free to fork and customize for your use case!
