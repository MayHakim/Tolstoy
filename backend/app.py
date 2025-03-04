from flask import Flask, request, jsonify
import json
import os
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set OpenAI API key
openai.api_key = "insert API key here"

# Load product data
with open('product_data.json', 'r') as f:
    product_data = json.load(f)

# User profiles storage (in-memory for simplicity, would be a database in production)
user_profiles = {}


def initialize_user_profile(user_id):
    """Initialize a new user profile with default values."""
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            "price_range": {"min": 0, "max": 2000},
            "preferred_brands": [],
            "preferred_categories": [],
            "style_preferences": [],
            "color_preferences": [],
            "conversation_history": []
        }
    return user_profiles[user_id]


def update_user_profile(user_id, message, assistant_response):
    """Update user profile based on the conversation."""
    profile = user_profiles[user_id]
    # Add to conversation history
    profile["conversation_history"].append({
        "user": message,
        "assistant": assistant_response
    })

    # Use OpenAI to extract preferences from the conversation
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are a preference extraction system. 
                Extract user preferences from their message for online shopping. 
                Return a JSON object with these fields:
                Note, users may not specify these preferences explicitly, so you may need to infer them from the message.
                They can also mention a domain instead of a specific brand or category (e.g., 'Electronics').
                For example, when a user mentions a product, you can infer the category preferences.
                - price_range: {min: number, max: number} (only if specific amounts mentioned, if only min or max is mentioned, set the other one to default (min=0, max=2000))
                - preferred_brands: [string] (list of mentioned brands)
                - preferred_categories: [string] (list of categories mentioned or implied from the message)
                - style_preferences: [string] (descriptive style terms like 'casual', 'professional')
                - color_preferences: [string] (list of colors mentioned)
                Return an empty object if none detected."""},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"}
        )

        extracted_preferences = json.loads(response.choices[0].message.content)
        print(f"extracted_preferences: {extracted_preferences}") # for debugging

        # Update profile with new information
        if "price_range" in extracted_preferences:
            profile["price_range"] = extracted_preferences["price_range"]
            # print(f"price_range: {profile['price_range']}") # for debugging
        if "preferred_brands" in extracted_preferences:
            profile["preferred_brands"].extend(extracted_preferences["preferred_brands"])
            profile["preferred_brands"] = list(set(profile["preferred_brands"]))
            # print(f"preferred_brands: {profile['preferred_brands']}") # for debugging
        if "preferred_categories" in extracted_preferences:
            profile["preferred_categories"].extend(extracted_preferences["preferred_categories"])
            profile["preferred_categories"] = list(set(profile["preferred_categories"]))
            # print(f"preferred_categories: {profile['preferred_categories']}") # for debugging
        if "style_preferences" in extracted_preferences:
            profile["style_preferences"].extend(extracted_preferences["style_preferences"])
            profile["style_preferences"] = list(set(profile["style_preferences"]))
            # print(f"style_preferences: {profile['style_preferences']}") # for debugging
        if "color_preferences" in extracted_preferences:
            profile["color_preferences"].extend(extracted_preferences["color_preferences"])
            profile["color_preferences"] = list(set(profile["color_preferences"]))
            # print(f"color_preferences: {profile['color_preferences']}") # for debugging


    except Exception as e:
        print(f"Error updating user profile: {e}")

    return profile


def gpt_rank_products(user_message, user_profile, products):
    """Use GPT to rank products based on user message and profile."""

    products_str = json.dumps([{
        "id": p["id"],
        "name": p["name"],
        "category": p["category"],
        "subcategory": p["subcategory"],
        "price": p["price"],
        "brand": p["brand"],
        "color": p["color"],
        "description": p["description"],
        "tags": p["tags"]
    } for p in products])

    profile_str = json.dumps(user_profile)
    # print(f"products_str: {products_str}") # for debugging
    # print(f"profile_str: {profile_str}") # for debugging

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are a product recommendation system.
                Rank the provided products based on how well they match the user's current request and profile.

                If the user is looking for something specific that doesn't exactly match our inventory, recommend the most relevant alternatives:
                1. Similar type products (e.g., if no running shoes, suggest sneakers)
                2. Related products in the same category (e.g., if looking for running shoes, suggest sports clothes)
                3. Products that match the request in some way (e.g., category, style, color)

                Return a JSON array in this format:
                [{{
                    "product_id": number,
                    "relevance_score": number (0-100),
                    "reasoning": "brief explanation of why this product matches"
                }}]

                Sort by relevance_score in descending order. 
                Return at most 3 products with json named 'products'.
                If no products match, try to suggest the closest 3 alternatives with json named "alternatives". 
                User profile: {profile_str}
                Available products: {products_str}"""},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"}
        )

        rankings_raw = json.loads(response.choices[0].message.content)
        print(f"response: {response.choices[0].message.content}") # for debugging
        rankings = rankings_raw['products']
        print(f"rankings: {rankings}") # for debugging
        return rankings

    except Exception as e:
        print(f"Error in GPT ranking: {e}")
        return rankings_raw['alternatives']


def get_product_recommendations(user_id, query):
    """Get product recommendations based on user profile and current query."""
    profile = user_profiles[user_id]
    products = product_data["products"]

    # Use GPT to rank the products
    ranked_products = gpt_rank_products(query, profile, products)

    # Map the rankings back to full product details
    recommendations = []
    product_map = {p["id"]: p for p in products}

    for item in ranked_products:
        if isinstance(item, dict) and "product_id" in item:
            product_id = item["product_id"]
            if product_id in product_map:
                product = product_map[product_id].copy()
                product["relevance_score"] = item.get("relevance_score", 0)
                product["reasoning"] = item.get("reasoning", "")
                recommendations.append(product)

    return recommendations


def generate_assistant_response(user_id, message, recommendations):
    """Generate a conversational response using OpenAI."""
    profile = user_profiles[user_id]

    # Create a context from user profile
    profile_context = {
        "price_range": profile["price_range"],
        "preferred_brands": profile["preferred_brands"],
        "preferred_categories": profile["preferred_categories"],
        "style_preferences": profile["style_preferences"],
        "color_preferences": profile["color_preferences"],
    }

    # Format recommendations for the prompt
    recommendation_text = ""
    if recommendations:
        recommendation_text = "Based on the user's request, I have these product recommendations:\n"
        for i, product in enumerate(recommendations, 1):
            recommendation_text += f"{i}. {product['name']} by {product['brand']} - ${product['price']} - Relevance: {product.get('relevance_score', 0)}/100\n"
            recommendation_text += f"   Why recommended: {product.get('reasoning', 'Matches user preferences')}\n"

    try:
        # Get last few conversation turns for context
        conversation_context = ""
        if len(profile["conversation_history"]) > 0:
            last_turns = profile["conversation_history"][-3:]  # Last 3 turns
            for turn in last_turns:
                conversation_context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are a helpful and friendly shopping assistant named ShopBot. 
                Your job is to help users discover products that match their preferences.

                What I know about the user's preferences: {json.dumps(profile_context)}

                Available product recommendations: {recommendation_text}

                Recent conversation context:
                {conversation_context}

                When responding:
                1. Be conversational and friendly
                2. Ask clarifying questions if needed to better understand preferences
                3. Mention specific product recommendations if they apply to the user's query
                4. If the user is looking for something we don't have exact matches for, suggest the closest alternatives we do have
                5. Explain why you're recommending alternatives if they're not exactly what the user asked for
                6. Keep responses concise (2 paragraphs max)
                7. Don't state the recommendations ranking or scoring unless asked
                8. Don't explicitly state all the user preferences you're tracking unless asked"""},
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. How else can I help you?"


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle incoming chat messages."""
    # print(request.json) # for debugging
    data = request.json
    user_id = data.get('user_id', 'default_user')
    message = data.get('message', '')

    # Initialize or get user profile
    profile = initialize_user_profile(user_id)

    # Get product recommendations based on profile and current message
    recommendations = get_product_recommendations(user_id, message)

    # Generate assistant response
    assistant_response = generate_assistant_response(user_id, message, recommendations)

    # Update user profile based on new interaction
    update_user_profile(user_id, message, assistant_response)

    return jsonify({
        'response': assistant_response,
        'recommendations': recommendations
    })


@app.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    """Get the current user profile."""
    profile = initialize_user_profile(user_id)
    return jsonify(profile)


if __name__ == '__main__':
    app.run(debug=True, port=5000)