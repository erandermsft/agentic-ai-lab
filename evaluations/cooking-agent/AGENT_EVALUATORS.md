# 🤖 Agent-Specific Evaluators

This document explains the agent-specific evaluators used in the cooking agent evaluation framework.

## Overview

In addition to quality evaluators (Relevance, Coherence, Fluency), we use three specialized evaluators designed specifically for agentic workflows:

1. **Intent Resolution** - Understanding user requests
2. **Tool Call Accuracy** - Making correct tool selections
3. **Task Adherence** - Following instructions and staying on task

These evaluators are particularly important for AI agents that:
- Use multiple tools to complete tasks
- Need to understand complex user intents
- Must follow specific task instructions
- Engage in multi-turn conversations

## Agent Evaluators in Detail

### 1. Intent Resolution Evaluator

**Purpose**: Measures how well the system identifies and understands a user's request.

**What it evaluates**:
- ✅ Correct identification of user intent
- ✅ Ability to ask clarifying questions when needed
- ✅ Understanding of agent's scope and capabilities
- ✅ Appropriate responses when queries are out of scope

**Scoring**:
- **Range**: 1-5 (Likert scale)
- **Threshold**: 3 (Pass if score ≥ 3)
- **Higher is better**

**Example for Cooking Agent**:

**Query**: "I need something quick for dinner"

**Good Intent Resolution (Score: 5)**:
- Agent recognizes intent: "find quick meal recipes"
- Uses `get_recipe_suggestions(dietary_preference='quick')`
- Provides relevant quick recipes

**Poor Intent Resolution (Score: 2)**:
- Agent misunderstands intent
- Provides general cooking advice instead of specific recipes
- Doesn't recognize "quick" as a filter criterion

**Output Fields**:
```json
{
  "intent_resolution": 5,
  "intent_resolution_result": "pass",
  "intent_resolution_threshold": 3,
  "intent_resolution_reason": "Agent correctly identified user's need for quick dinner recipes...",
  "additional_details": {
    "conversation_has_intent": true,
    "agent_perceived_intent": "find quick recipes for dinner",
    "actual_user_intent": "get quick dinner ideas",
    "correct_intent_detected": true,
    "intent_resolved": true
  }
}
```

### 2. Tool Call Accuracy Evaluator

**Purpose**: Measures the accuracy and efficiency of tool calls made by the agent.

**What it evaluates**:
- ✅ Correct tool selection for the query
- ✅ Proper parameters passed to tools
- ✅ No missing required tool calls
- ✅ No excessive/unnecessary tool calls

**Data Requirements**:
- Tool call information is automatically captured by `run_agent.py`
- Each response includes a `tool_calls` array with tool name and arguments
- Evaluator analyzes these against the query to assess accuracy

**Scoring**:
- **Range**: 1-5 (Likert scale)
- **Threshold**: 3 (Pass if score ≥ 3)
- **Based on**: Relevance, correctness, and efficiency

**Example for Cooking Agent**:

**Query**: "What ingredients do I need for spaghetti carbonara?"

**Good Tool Call Accuracy (Score: 5)**:
```python
# Single correct tool call
extract_ingredients(recipe_name="Spaghetti Carbonara")
# ✅ Correct tool
# ✅ Correct parameter
# ✅ No missing calls
# ✅ No excessive calls
```

**Poor Tool Call Accuracy (Score: 2)**:
```python
# Incorrect approach
search_recipes(query="ingredients")  # ❌ Wrong tool
search_recipes(query="carbonara")    # ❌ Excessive call
get_recipe_suggestions("Italian")    # ❌ Irrelevant call
# Missing: extract_ingredients()
```

**Supported Tools**:
- ✅ Function Tools (user-defined) - **Used by Cooking Agent**
- ✅ File Search
- ✅ Azure AI Search
- ✅ Bing Grounding
- ✅ Code Interpreter
- ✅ OpenAPI tools
- ✅ SharePoint Grounding
- ✅ Fabric Data Agent

**Output Fields**:
```json
{
  "tool_call_accuracy": 5,
  "tool_call_accuracy_result": "pass",
  "tool_call_accuracy_threshold": 3,
  "details": {
    "tool_calls_made_by_agent": 1,
    "correct_tool_calls_made_by_agent": 1,
    "per_tool_call_details": [
      {
        "tool_name": "extract_ingredients",
        "total_calls_required": 1,
        "correct_calls_made_by_agent": 1,
        "correct_tool_percentage": 1.0,
        "tool_call_errors": 0,
        "tool_success_result": "pass"
      }
    ],
    "excess_tool_calls": {
      "total": 0,
      "details": []
    },
    "missing_tool_calls": {
      "total": 0,
      "details": []
    }
  }
}
```

### 3. Task Adherence Evaluator

**Purpose**: Measures how well the agent stays on track to complete assigned tasks.

**What it evaluates**:
- ✅ Following system instructions
- ✅ Staying within scope of capabilities
- ✅ Completing the specific task requested
- ✅ Not deviating to unrelated topics

**Scoring**:
- **Range**: 1-5 (Likert scale)
- **Threshold**: 3 (Pass if score ≥ 3)
- **Higher is better**

**Example for Cooking Agent**:

**System Instruction**: "You are a cooking assistant that helps with recipe search and ingredient extraction."

**Query**: "Find me pasta recipes"

**Good Task Adherence (Score: 5)**:
- Agent uses recipe search tool
- Provides relevant pasta recipes
- Stays focused on cooking assistance
- Doesn't offer unrelated advice

**Poor Task Adherence (Score: 2)**:
- Agent starts discussing nutrition science
- Provides restaurant recommendations instead of recipes
- Offers cooking equipment shopping links
- Deviates from core task of recipe assistance

**Output Fields**:
```json
{
  "task_adherence": 5,
  "task_adherence_result": "pass",
  "task_adherence_threshold": 3,
  "task_adherence_reason": "Agent correctly focused on recipe search task, used appropriate tools, and provided relevant pasta recipes without deviating from core cooking assistance mission."
}
```

## Why These Evaluators Matter for Cooking Agent

### Intent Resolution
Our cooking agent needs to understand various ways users ask for recipes:
- "I'm hungry" → Needs clarification
- "Quick dinner ideas" → Use quick filter
- "What's in carbonara?" → Extract ingredients
- "Vegetarian options" → Filter by dietary preference

### Tool Call Accuracy
The agent has 3 tools and must choose correctly:
- `search_recipes(query)` - For finding recipes by name/ingredient
- `extract_ingredients(recipe_name)` - For getting ingredient lists
- `get_recipe_suggestions(dietary_preference)` - For filtered recommendations

Wrong tool selection = poor user experience.

### Task Adherence
The agent should:
- ✅ Focus on recipe search and ingredient extraction
- ✅ Use available tools appropriately
- ❌ NOT discuss nutrition, cooking techniques, or equipment
- ❌ NOT provide information outside its scope

## How to Interpret Results

### High Scores (4-5)
- ✅ Agent working as designed
- ✅ Good understanding of user needs
- ✅ Efficient tool usage
- ✅ Stays on task

### Medium Scores (3)
- ⚠️ Acceptable but room for improvement
- ⚠️ May have minor inefficiencies
- ⚠️ Consider prompt refinement

### Low Scores (1-2)
- ❌ Significant issues
- ❌ Review system prompts
- ❌ Check tool definitions
- ❌ Consider adding examples to prompts

## Optimization Tips

### Improving Intent Resolution
1. **Add clarifying examples** to system prompts
2. **Explicitly list** what queries are in/out of scope
3. **Train agent** to ask for clarification when ambiguous
4. **Provide examples** of different intent phrasings

### Improving Tool Call Accuracy
1. **Clear tool descriptions** with specific use cases
2. **Detailed parameter descriptions** with examples
3. **Add constraints** to prevent tool misuse
4. **Test edge cases** in tool selection logic

### Improving Task Adherence
1. **Explicit system instructions** about scope
2. **Clear boundaries** on what agent can/cannot do
3. **Reinforce task focus** in prompts
4. **Add examples** of staying on task

## Viewing Detailed Results

After evaluation completes in Azure AI Foundry:

1. Go to [Azure AI Foundry](https://ai.azure.com)
2. Navigate to your project
3. Click **Evaluation** tab
4. Find "Cooking Agent Evaluation"
5. View **detailed breakdown** for each evaluator:
   - Overall scores
   - Per-query results
   - Failure reasons
   - Suggestions for improvement

## Best Practices

### 1. Run Evaluations Regularly
- After every prompt change
- When adding new tools
- During model updates
- Before production deployment

### 2. Track Trends Over Time
- Compare evaluation runs
- Monitor score changes
- Identify regressions early

### 3. Focus on Low Scores
- Investigate failures
- Update prompts based on feedback
- Add test cases for edge cases

### 4. Balance All Metrics
- Don't optimize one evaluator at expense of others
- Aim for balanced improvement across all 6 metrics

## Reference Documentation

- [Agent Evaluators Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Evaluating Azure AI Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk)
- [Cloud Evaluation Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/cloud-evaluation)

## Summary

The three agent-specific evaluators provide crucial insights into:
- **Intent Resolution**: Does the agent understand what users want?
- **Tool Call Accuracy**: Does the agent use tools correctly?
- **Task Adherence**: Does the agent stay focused on its mission?

Combined with quality evaluators (Relevance, Coherence, Fluency), you get a comprehensive view of your agent's performance across 6 dimensions.
