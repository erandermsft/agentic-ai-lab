"""
Evaluation script for the Cooking AI Agent
Runs cloud-based evaluation using Azure AI Foundry SDK
"""

import os
import json
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    Evaluation,
    InputDataset,
    EvaluatorConfiguration,
)
from dotenv import load_dotenv

load_dotenv()


def get_tool_definitions() -> list:
    """
    Get the tool definitions that were available to the cooking agent.
    These definitions help the Tool Call Accuracy evaluator understand
    which tools were available and their intended use.
    
    Format matches Azure AI Foundry evaluator requirements.
    """
    return [
        {
            "id": "search_recipes",
            "name": "search_recipes",
            "description": "Search for recipes based on a query. Returns matching recipes with their basic information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for recipes (e.g., 'pasta', 'chicken', 'dessert')"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "id": "extract_ingredients",
            "name": "extract_ingredients",
            "description": "Extract and return the full list of ingredients for a specific recipe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipe_name": {
                        "type": "string",
                        "description": "The name of the recipe to extract ingredients from"
                    }
                },
                "required": ["recipe_name"]
            }
        },
        {
            "id": "get_recipe_suggestions",
            "name": "get_recipe_suggestions",
            "description": "Get recipe suggestions based on dietary preferences or meal type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dietary_preference": {
                        "type": "string",
                        "description": "Dietary preference (e.g., 'quick', 'vegetarian', 'meat', 'dessert')",
                        "default": "any"
                    }
                }
            }
        }
    ]


def prepare_evaluation_data(responses_file: str, output_jsonl: str) -> None:
    """
    Convert test responses to JSONL format required by cloud evaluation.
    
    Args:
        responses_file: Path to test_responses.json
        output_jsonl: Path to output JSONL file
    """
    print(f"📊 Preparing evaluation data from {responses_file}...")
    
    with open(responses_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        responses = data.get("responses", [])
    
    # Get tool definitions that were available to the agent
    tool_definitions = get_tool_definitions()
    
    # Convert to JSONL format with required fields
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for item in responses:
            # Create evaluation record
            eval_record = {
                "query": item.get("query", ""),
                "response": item.get("response", ""),
                "tool_calls": item.get("tool_calls", []),  # Include tool calls for agent evaluators
                "tool_definitions": tool_definitions  # Include tool definitions for Tool Call Accuracy evaluator
            }
            
            f.write(json.dumps(eval_record) + '\n')
    
    print(f"✅ Created evaluation dataset: {output_jsonl} ({len(responses)} records)")


def run_evaluation():
    """
    Run comprehensive cloud-based evaluation of the cooking agent using Azure AI Foundry.
    """
    print("=" * 70)
    print("🔬 Cooking Agent Cloud Evaluation")
    print("=" * 70)
    
    # File paths
    responses_file = "test_responses.json"
    eval_data_file = "evaluation_data.jsonl"
    dataset_name = "cooking-agent-test-data"
    # Use timestamp for unique version to avoid conflicts
    dataset_version = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Step 1: Prepare data in JSONL format
    prepare_evaluation_data(responses_file, eval_data_file)
    
    # Step 2: Get Azure AI Foundry project configuration
    print("\n🔧 Configuring Azure AI Foundry project...")
    
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_endpoint = os.getenv("MODEL_ENDPOINT")
    model_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    model_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    
    if not project_endpoint:
        print("❌ PROJECT_ENDPOINT not found. Please set it in environment variables.")
        print("   Format: https://<account>.services.ai.azure.com/api/projects/<project>")
        return None
    
    if not model_endpoint:
        print("❌ MODEL_ENDPOINT not found. Please set it in environment variables.")
        print("   Format: https://<account>.services.ai.azure.com")
        return None
    
    if not model_api_key:
        print("❌ AZURE_OPENAI_API_KEY not found. Please set it in environment variables.")
        print("   This is required for cloud evaluation evaluators.")
        return None
    
    print(f"✅ Project endpoint: {project_endpoint}")
    print(f"✅ Model deployment: {model_deployment_name}")
    
    # Step 3: Create AI Project Client
    print("\n🌐 Connecting to Azure AI Foundry project...")
    
    try:
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
        print("✅ Connected to Azure AI Foundry project")
    except Exception as e:
        print(f"❌ Failed to connect to project: {e}")
        print("Please run 'az login' and ensure you have access to the project.")
        return None
    
    # Step 4: Upload evaluation dataset
    print(f"\n� Uploading evaluation dataset...")
    
    try:
        data_upload = project_client.datasets.upload_file(
            name=dataset_name,
            version=dataset_version,
            file_path=eval_data_file,
        )
        data_id = data_upload.id
        if not data_id:
            print("❌ Dataset upload succeeded but no ID returned")
            return None
        print(f"✅ Dataset uploaded: {dataset_name} (v{dataset_version})")
        print(f"   Dataset ID: {data_id}")
    except Exception as e:
        print(f"❌ Failed to upload dataset: {e}")
        return None
    
    # Step 5: Configure evaluators
    print("\n📋 Configuring evaluators...")
    
    from azure.ai.projects.models import EvaluatorIds
    
    evaluators = {
        # Quality evaluators
        "relevance": EvaluatorConfiguration(
            id=EvaluatorIds.RELEVANCE.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
            },
        ),
        "coherence": EvaluatorConfiguration(
            id=EvaluatorIds.COHERENCE.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
            },
        ),
        "fluency": EvaluatorConfiguration(
            id=EvaluatorIds.FLUENCY.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
            },
        ),
        # Agent-specific evaluators
        "intent_resolution": EvaluatorConfiguration(
            id=EvaluatorIds.INTENT_RESOLUTION.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
            },
        ),
        "tool_call_accuracy": EvaluatorConfiguration(
            id=EvaluatorIds.TOOL_CALL_ACCURACY.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
                "tool_calls": "${data.tool_calls}",  # Map tool_calls from data
                "tool_definitions": "${data.tool_definitions}",  # Map tool definitions from data
            },
        ),
        "task_adherence": EvaluatorConfiguration(
            id=EvaluatorIds.TASK_ADHERENCE.value,
            init_params={"deployment_name": model_deployment_name},
            data_mapping={
                "query": "${data.query}",
                "response": "${data.response}",
            },
        ),
    }
    
    print(f"✅ Configured {len(evaluators)} evaluators:")
    print("   Quality Evaluators:")
    print("   - relevance")
    print("   - coherence")
    print("   - fluency")
    print("   Agent Evaluators:")
    print("   - intent_resolution")
    print("   - tool_call_accuracy")
    print("   - task_adherence")
    
    # Step 6: Create and submit evaluation
    print("\n🚀 Submitting cloud evaluation...")
    
    try:
        evaluation = Evaluation(
            display_name="Cooking Agent Evaluation",
            description="Evaluation of cooking agent responses for quality (relevance, coherence, fluency) and agent-specific metrics (intent resolution, tool call accuracy, task adherence)",
            data=InputDataset(id=data_id),
            evaluators=evaluators,
        )
        
        # Submit the evaluation with required headers
        evaluation_response = project_client.evaluations.create(
            evaluation,
            headers={
                "model-endpoint": model_endpoint,
                "api-key": model_api_key,
            },
        )
        
        print("✅ Evaluation submitted successfully!")
        print("=" * 70)
        print(f"📊 Evaluation Details:")
        if hasattr(evaluation_response, 'name'):
            print(f"   Name: {evaluation_response.name}")
        if hasattr(evaluation_response, 'status'):
            print(f"   Status: {evaluation_response.status}")
        if hasattr(evaluation_response, 'id'):
            print(f"   ID: {evaluation_response.id}")
        print("=" * 70)
        print("\n🎯 Next Steps:")
        print("   1. View evaluation progress in Azure AI Foundry portal")
        print("      URL: https://ai.azure.com")
        print("   2. Navigate to your project → Evaluation tab")
        print("   3. Look for evaluation: 'Cooking Agent Evaluation'")
        print(f"   4. Dataset version: {dataset_version}")
        print("\n💡 Tip: Results will be automatically logged to your Azure AI project")
        
        return evaluation_response
        
    except Exception as e:
        print(f"\n❌ Failed to submit evaluation: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PROJECT_ENDPOINT is correct")
        print("2. Ensure MODEL_ENDPOINT is correct")
        print("3. Verify model deployment exists in your Azure OpenAI resource")
        print("4. Check that storage account is connected to your project")
        print("5. Ensure you have appropriate permissions")
        raise


if __name__ == "__main__":
    try:
        result = run_evaluation()
        if result:
            print("\n🎉 Evaluation submitted! Check Azure AI Foundry portal for results.")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        exit(1)
