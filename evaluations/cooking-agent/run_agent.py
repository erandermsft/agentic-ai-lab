"""
Agent Runner for Collecting Responses from Cooking Agent
This script runs the cooking agent with test queries and collects responses for evaluation.
"""

import asyncio
import json
import os
import sys
from typing import Any

# Enable debug mode to inspect message structure
DEBUG_MODE = len(sys.argv) > 1 and sys.argv[1] == "--debug"

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()
# Import tools from the main cooking agent
sys.path.insert(0, os.path.dirname(__file__))
from cooking_agent import search_recipes, extract_ingredients, get_recipe_suggestions


async def run_agent_with_queries(queries_file: str, output_file: str) -> None:
    """
    Run the cooking agent with test queries and collect responses.
    
    Args:
        queries_file: Path to JSON file containing test queries
        output_file: Path to save collected responses
    """
    print("=" * 70)
    print("🏃 Running Cooking Agent to Collect Responses")
    print("=" * 70)
    
    # Load test queries
    print(f"\n📂 Loading queries from: {queries_file}")
    with open(queries_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        queries = data.get("queries", [])
    
    print(f"✅ Loaded {len(queries)} test queries")
    
    # Get Azure configuration
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    
    if not azure_endpoint:
        print("❌ AZURE_OPENAI_ENDPOINT not found. Please set it in environment variables.")
        return
    
    # Initialize the agent
    print("\n🤖 Initializing cooking agent...")
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    openai_client = AsyncAzureOpenAI(
        azure_endpoint=azure_endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21"
    )
    
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id=deployment_name
    )
    
    agent = ChatAgent(
        chat_client=chat_client,
        name="CookingAgent",
        instructions="""You are a helpful cooking assistant AI agent. You help users find recipes, 
        extract ingredient lists, and provide cooking suggestions. 
        
        When users ask about recipes:
        - Use search_recipes to find recipes based on their query
        - Use extract_ingredients to get detailed ingredient lists for specific recipes
        - Use get_recipe_suggestions to provide recommendations based on preferences
        
        Always be friendly, enthusiastic about cooking, and provide clear, actionable information.
        If users ask for recipes not in the database, politely suggest alternatives.""",
        tools=[search_recipes, extract_ingredients, get_recipe_suggestions],
    )
    
    print("✅ Agent initialized successfully")
    
    # Collect responses
    print("\n📊 Running agent with test queries...\n")
    results = []
    
    for i, query_item in enumerate(queries, 1):
        query_id = query_item.get("id", f"q{i}")
        query_text = query_item.get("query", "")
        
        print(f"[{i}/{len(queries)}] Processing: {query_text}")
        
        try:
            # Create a new thread for each query (isolated evaluation)
            thread = agent.get_new_thread()
            
            # Run the agent
            response = await agent.run(query_text, thread=thread)
            
            # Extract data from AgentRunResponse
            final_response = response.text
            
            # Debug mode: inspect message structure
            if DEBUG_MODE and hasattr(response, 'messages') and response.messages:
                print("\n=== DEBUG: Message Structure ===")
                for i, msg in enumerate(response.messages[:3]):  # First 3 messages
                    print(f"\nMessage {i}:")
                    print(f"  Type: {type(msg)}")
                    print(f"  Dir: {[attr for attr in dir(msg) if not attr.startswith('_')]}")
                    if hasattr(msg, 'role'):
                        print(f"  Role: {msg.role}")
                    if hasattr(msg, 'text'):
                        print(f"  Text: {msg.text[:100] if msg.text else None}...")
                    
                    # Inspect contents attribute
                    if hasattr(msg, 'contents'):
                        print(f"  Contents type: {type(msg.contents)}")
                        if msg.contents:
                            print(f"  Contents length: {len(msg.contents)}")
                            for j, content in enumerate(msg.contents[:2]):
                                print(f"    Content {j}: {type(content)}")
                                print(f"      Dir: {[attr for attr in dir(content) if not attr.startswith('_')][:10]}")
                                # Check if it's a tool call content
                                if hasattr(content, 'tool_call_id'):
                                    print(f"      TOOL CALL ID: {content.tool_call_id}")
                                if hasattr(content, 'name'):
                                    print(f"      NAME: {content.name}")
                    
                    # Inspect raw_representation
                    if hasattr(msg, 'raw_representation'):
                        raw = msg.raw_representation
                        print(f"  raw_representation type: {type(raw)}")
                        if raw and hasattr(raw, 'tool_calls'):
                            print(f"    raw.tool_calls: {raw.tool_calls}")
                        if raw:
                            raw_dict = raw if isinstance(raw, dict) else (raw.to_dict() if hasattr(raw, 'to_dict') else None)
                            if raw_dict and 'tool_calls' in raw_dict:
                                print(f"    raw_dict tool_calls: {raw_dict['tool_calls']}")
                print("=== END DEBUG ===\n")
            
            # Extract conversation history and tool calls
            conversation_history = []
            tool_calls = []
            
            if hasattr(response, 'messages') and response.messages:
                for msg in response.messages:
                    # Convert Role enum to string
                    role_str = str(msg.role.value) if hasattr(msg, 'role') and hasattr(msg.role, 'value') else str(msg.role) if hasattr(msg, 'role') else "unknown"
                    
                    # Extract tool calls from FunctionCallContent in contents list
                    if hasattr(msg, 'contents') and msg.contents:
                        for content in msg.contents:
                            # Check if this is a FunctionCallContent (tool call)
                            if type(content).__name__ == 'FunctionCallContent':
                                # Parse arguments from JSON string to dict
                                arguments = content.arguments if hasattr(content, 'arguments') else None
                                if arguments and isinstance(arguments, str):
                                    try:
                                        arguments = json.loads(arguments)
                                    except json.JSONDecodeError:
                                        arguments = {}
                                
                                tool_call_info = {
                                    "type": "tool_call",
                                    "tool_call_id": content.call_id if hasattr(content, 'call_id') else None,
                                    "name": content.name if hasattr(content, 'name') else None,
                                    "arguments": arguments
                                }
                                tool_calls.append(tool_call_info)
                    
                    # Try to extract text content from various possible structures
                    content_text = ""
                    
                    # Check if message has direct text attribute
                    if hasattr(msg, 'text') and msg.text:
                        content_text = msg.text
                    # Check if there's a TextContent in the contents list
                    elif hasattr(msg, 'contents') and msg.contents:
                        for content in msg.contents:
                            if type(content).__name__ == 'TextContent' and hasattr(content, 'text'):
                                content_text = content.text
                                break
                    
                    # Only add messages with actual content
                    if content_text.strip():
                        conversation_history.append({
                            "role": role_str,
                            "content": content_text
                        })
            
            # Store result
            result_item = {
                "query_id": query_id,
                "query": query_text,
                "response": final_response,
                "conversation_history": conversation_history,
                "tool_calls": tool_calls  # Include tool calls for evaluation
            }
            
            results.append(result_item)
            print(f"    ✅ Response collected ({len(final_response)} chars, {len(tool_calls)} tool calls)\n")
            
        except Exception as e:
            print(f"    ❌ Error: {e}\n")
            results.append({
                "query_id": query_id,
                "query": query_text,
                "response": f"ERROR: {str(e)}",
                "conversation_history": [],
                "tool_calls": []
            })
    
    # Save results
    print(f"\n💾 Saving responses to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "responses": results,
            "total_queries": len(queries),
            "successful_responses": len([r for r in results if not r["response"].startswith("ERROR:")])
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully saved {len(results)} responses")
    print("\n" + "=" * 70)
    print("🎉 Agent runner completed!")
    print("=" * 70)


if __name__ == "__main__":
    # Default paths
    queries_file = "test_queries.json"
    output_file = "test_responses.json"
    
    # Allow command-line overrides (skip --debug flag)
    args = [arg for arg in sys.argv[1:] if arg != "--debug"]
    if len(args) > 0:
        queries_file = args[0]
    if len(args) > 1:
        output_file = args[1]
    
    # Run the agent runner
    asyncio.run(run_agent_with_queries(queries_file, output_file))
