"""
Cooking AI Agent with Recipe Search and Ingredient Extraction
Uses Microsoft Agent Framework with GitHub Models
"""

import asyncio
import sys
import os
from typing import Annotated

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


# Recipe database (simulated - in production, this could be a real API or database)
RECIPES_DB = {
    "pasta carbonara": {
        "name": "Pasta Carbonara",
        "ingredients": ["spaghetti", "eggs", "parmesan cheese", "pancetta", "black pepper"],
        "instructions": "Cook pasta. Fry pancetta. Mix eggs with cheese. Combine all with pasta water.",
        "prep_time": "10 min",
        "cook_time": "15 min",
        "servings": 4
    },
    "chicken stir fry": {
        "name": "Chicken Stir Fry",
        "ingredients": ["chicken breast", "soy sauce", "vegetables (bell peppers, broccoli)", "garlic", "ginger", "sesame oil"],
        "instructions": "Cut chicken and vegetables. Stir fry chicken, add vegetables, season with soy sauce and aromatics.",
        "prep_time": "15 min",
        "cook_time": "10 min",
        "servings": 4
    },
    "tomato soup": {
        "name": "Tomato Soup",
        "ingredients": ["tomatoes", "onion", "garlic", "vegetable broth", "cream", "basil"],
        "instructions": "Sauté onion and garlic. Add tomatoes and broth. Simmer and blend. Stir in cream.",
        "prep_time": "10 min",
        "cook_time": "20 min",
        "servings": 6
    },
    "chocolate chip cookies": {
        "name": "Chocolate Chip Cookies",
        "ingredients": ["flour", "butter", "sugar", "eggs", "chocolate chips", "vanilla extract", "baking soda"],
        "instructions": "Mix butter and sugar. Add eggs and vanilla. Mix in dry ingredients and chocolate chips. Bake at 375°F.",
        "prep_time": "15 min",
        "cook_time": "12 min",
        "servings": 24
    },
    "caesar salad": {
        "name": "Caesar Salad",
        "ingredients": ["romaine lettuce", "caesar dressing", "parmesan cheese", "croutons", "lemon", "anchovies"],
        "instructions": "Chop lettuce. Make dressing with anchovies, lemon, and parmesan. Toss with croutons.",
        "prep_time": "10 min",
        "cook_time": "0 min",
        "servings": 4
    },
    "beef tacos": {
        "name": "Beef Tacos",
        "ingredients": ["ground beef", "taco shells", "lettuce", "tomatoes", "cheese", "sour cream", "taco seasoning"],
        "instructions": "Brown beef with seasoning. Fill taco shells with beef and toppings.",
        "prep_time": "10 min",
        "cook_time": "15 min",
        "servings": 4
    }
}


def search_recipes(
    query: Annotated[str, "The search query for recipes (e.g., 'pasta', 'chicken', 'dessert')"],
) -> str:
    """
    Search for recipes based on a query.
    Returns matching recipes with their basic information.
    """
    query_lower = query.lower()
    matches = []
    
    for recipe_id, recipe_data in RECIPES_DB.items():
        # Search in recipe name, ingredients, or ID
        if (query_lower in recipe_id or 
            query_lower in recipe_data["name"].lower() or
            any(query_lower in ingredient.lower() for ingredient in recipe_data["ingredients"])):
            matches.append(recipe_data)
    
    if not matches:
        return f"No recipes found for '{query}'. Try searching for: pasta, chicken, soup, cookies, salad, or tacos."
    
    result = f"Found {len(matches)} recipe(s) for '{query}':\n\n"
    for recipe in matches:
        result += f"**{recipe['name']}**\n"
        result += f"  - Prep time: {recipe['prep_time']}\n"
        result += f"  - Cook time: {recipe['cook_time']}\n"
        result += f"  - Servings: {recipe['servings']}\n"
        result += f"  - Ingredients: {', '.join(recipe['ingredients'][:3])}...\n\n"
    
    return result


def extract_ingredients(
    recipe_name: Annotated[str, "The name of the recipe to extract ingredients from"],
) -> str:
    """
    Extract and return the full list of ingredients for a specific recipe.
    """
    recipe_name_lower = recipe_name.lower()
    
    # Find the recipe
    for recipe_id, recipe_data in RECIPES_DB.items():
        if recipe_name_lower in recipe_id or recipe_name_lower in recipe_data["name"].lower():
            result = f"**Ingredients for {recipe_data['name']}** (Serves {recipe_data['servings']})\n\n"
            for i, ingredient in enumerate(recipe_data["ingredients"], 1):
                result += f"{i}. {ingredient}\n"
            result += f"\n**Instructions:** {recipe_data['instructions']}\n"
            result += f"**Total time:** {recipe_data['prep_time']} prep + {recipe_data['cook_time']} cooking\n"
            return result
    
    return f"Recipe '{recipe_name}' not found. Try searching for recipes first using search_recipes."


def get_recipe_suggestions(
    dietary_preference: Annotated[str, "Dietary preference (e.g., 'quick', 'vegetarian', 'meat', 'dessert')"] = "any",
) -> str:
    """
    Get recipe suggestions based on dietary preferences or meal type.
    """
    suggestions = []
    preference_lower = dietary_preference.lower()
    
    if preference_lower in ["quick", "fast", "easy"]:
        suggestions = [r for r in RECIPES_DB.values() if int(r["cook_time"].split()[0]) <= 15]
    elif preference_lower in ["vegetarian", "veggie", "veg"]:
        veg_keywords = ["pasta", "soup", "salad", "cookies"]
        suggestions = [RECIPES_DB[k] for k in RECIPES_DB if any(vk in k for vk in veg_keywords)]
    elif preference_lower in ["meat", "protein"]:
        meat_keywords = ["chicken", "beef"]
        suggestions = [RECIPES_DB[k] for k in RECIPES_DB if any(mk in k for mk in meat_keywords)]
    elif preference_lower in ["dessert", "sweet"]:
        suggestions = [r for r in RECIPES_DB.values() if "cookie" in r["name"].lower()]
    else:
        # Return random suggestions
        suggestions = list(RECIPES_DB.values())[:3]
    
    if not suggestions:
        return "No specific suggestions found. Here are some popular recipes: Pasta Carbonara, Chicken Stir Fry, Tomato Soup."
    
    result = f"Recipe suggestions for '{dietary_preference}':\n\n"
    for recipe in suggestions:
        result += f"- **{recipe['name']}** ({recipe['prep_time']} prep, {recipe['cook_time']} cook)\n"
    
    return result


async def main():
    """
    Main function to run the cooking AI agent.
    """
    print("=" * 70)
    print("🍳 Cooking AI Agent with GitHub Models")
    print("=" * 70)
    print("\nWelcome to your personal cooking assistant!")
    print("I can help you with:")
    print("  - Recipe search (e.g., 'Find pasta recipes')")
    print("  - Ingredient extraction (e.g., 'What ingredients do I need for carbonara?')")
    print("  - Recipe suggestions (e.g., 'Suggest quick recipes')")
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("-" * 70)
    
    # Get Azure AI Foundry endpoint from environment
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not azure_endpoint:
        print("\n⚠️  AZURE_OPENAI_ENDPOINT not found in environment variables.")
        print("Please enter your Azure AI Foundry endpoint:")
        print("(Format: https://<your-resource>.openai.azure.com/)")
        azure_endpoint = input("Endpoint: ").strip()
        
        if not azure_endpoint:
            print("❌ No endpoint provided. Exiting.")
            return
    
    # Get deployment name from environment or use default
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    
    try:
        # Initialize Azure credential and token provider
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        # Initialize Azure OpenAI client
        openai_client = AsyncAzureOpenAI(
            azure_endpoint=azure_endpoint,
            azure_ad_token_provider=token_provider,
            api_version="2024-10-21"
        )
        
        # Create chat client
        chat_client = OpenAIChatClient(
            async_client=openai_client,
            model_id=deployment_name  # Using deployment from environment or default
        )
        
        # Create the cooking agent with tools
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
        
        # Create a thread for conversation continuity
        thread = agent.get_new_thread()
        
        print(f"\n✅ Connected to Azure AI Foundry")
        print(f"🤖 Agent ready! Using deployment: {deployment_name}")
        print("   Ask me anything about cooking.\n")
        
        # Interactive loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                    print("\n👋 Thanks for cooking with me! Goodbye!")
                    break
                
                # Run the agent
                print("Agent: ", end="", flush=True)
                result = await agent.run(user_input, thread=thread)
                print(result.text)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again.\n")
    
    except Exception as e:
        print(f"\n❌ Failed to initialize agent: {e}")
        print("\nTroubleshooting:")
        print("1. Verify AZURE_OPENAI_ENDPOINT is correct")
        print("2. Ensure you're authenticated (az login or managed identity)")
        print("3. Check AZURE_OPENAI_DEPLOYMENT exists in your resource")
        print("4. Verify you have appropriate RBAC permissions")
        return


if __name__ == "__main__":
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
