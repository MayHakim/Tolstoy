# AI shopping assistant
This project implements an interactive AI shopping assistant designed to help users discover products and make more informed purchase decisions. The core objective is to create a conversational agent that can: \
Engage in natural, multi-turn dialogues \
Learn and adapt to user preferences \
Provide intelligent product recommendations 

## Objectives
### Multi-Turn Dialogue Management
Maintain contextual conversation flow \
Ask clarifying questions about user needs \
Provide relevant and personalized responses in natural language
### Dynamic User Profiling
Track and update user preferences in real-time \
Capture insights like price range preferences, preferred brands, product categories of interest, style and color preferences
### Intelligent Recommendation System
Use generative AI to match products to user needs \
Improve recommendations through conversation \
Provide reasoning for product suggestions

## Technical Architecture
### System Components
Frontend: HTML, CSS, JavaScript \
Backend: Python (Flask) \
AI Engine: OpenAI GPT-4o-mini \
Recommendation Logic: Dynamic profile-based matching
### Product Dataset
20 diverse products across categories stored in a JSON file. \
Attributes include: name, category, price, brand, color, description and tags.
### Key Technical Features
Conversation state tracking \
Real-time user profile updates \
AI-powered recommendation generation \
Adaptive suggestion mechanism 

## Recommendation Approach
### LLM-Based Recommendation System
With a limited product database of 20 items and no historical purchase data, traditional recommendation methods fell short. To solve this, I implemented LLM-based recommendation system using GPT. \
Large Language Models (LLMs) offer powerful capabilities for enhancing customer interactions:
1. Sentiment Analysis- LLMs can deeply analyze text data from reviews and conversations to understand the emotional context behind customer preferences and feedback.
2. Customer Intent Detection- By examining customer inquiries, the system can precisely identify the underlying intent, enabling more accurate and targeted recommendations.
3. Customer Profiling- LLMs transform text interactions into comprehensive customer profiles, capturing nuanced preferences, interests, and behavioral patterns.
4. Explainable Recommendations- The system goes beyond simple matching by:
providing structured, context-aware recommendations, 
generating personalized explanation messages,
highlighting key product benefits,
and making recommendations more appealing and transparent


The core idea was to transform user preferences and product data into a format GPT could understand and process. By providing comprehensive context - including the user's current message, preference profile, and full product dataset - the system could generate intelligent, contextually relevant recommendations. \
When a user makes a request, the system sends their preferences, message, and product data to GPT. The model is asked to:
1. Rank existing products based on the user's information
2. Provide relevance scores for each recommendation
3. Explain the reasoning behind each suggestion
4. Find alternative or complementary items if exact matches aren't available

### Preference Extraction Methods
Users often communicate product preferences using ambiguous or imprecise language. For instance, "I want AirForce" implicitly means seeking Nike shoes, while "Something professional for work" requires style interpretation. \
To address this, I leveraged GPT's natural language understanding to systematically extract and interpret user preferences. The extraction focuses on five key attributes: price range, brands, product categories, style and color. \
The system also preserves conversation history, using the full interaction context to continuously refine understanding and improve recommendation accuracy.

## How to Use
1. Clone the git repo
2. Run the code
3. Insert your project path + "frontend/index.html" in your browser
4. Get your shopping assistance!

### Optional Tests
1. Multi-Turn Context and Preference Building \
Purpose: Evaluate context retention and preference learning \
User: "I'm looking for some new headphones" \
User: "I prefer wireless ones that are good for travel" \
User: "I'd like to spend less than $150 if possible" \
User: "That looks good. What about something for my home office too?" \
User: "I need a good desk setup for working from home" \
User: "I'd be willing to spend more on quality items for my office"
2. Brand and Style Preference Recognition \
Purpose: Test if the assistant remembers brand and style preferences \
User: "I like minimalist design products" \
User: "Show me some kitchen appliances with clean, simple designs" \
User: "I really like CookCraft products" \
User: "Let's look at some home decor items now" \
(Check if recommendation still favors minimalist designs)  
3. Price Range Adaptation and Category Switching \
Purpose: Test dynamic price range understanding and category transitions \
User: "I need some budget-friendly home items under $50" \
User: "Those look good. Actually, I just got a bonus at work. Show me some premium options now" \
User: "What high-end electronics do you recommend?" \
User: "Now I'm looking for something for my bathroom" \
(Check if recommendations include both budget and premium options based on demonstrated flexibility) 
4. Negative Preference Handling \
Purpose: Test tracking of dislikes and negative preferences \
User: "I don't like bright colorful products" \
User: "I prefer items in neutral colors like black, white, or gray" \
User: "What bags do you have?" \
(Check if recommendations avoid bright colors) \
User: "I don't want anything from UrbanTrek" \
(Check if brand is excluded from future recommendations) 
5. Handling Edge Cases 
Purpose: Test response to challenging or unusual requests \
User: "I want the absolute best quality headphones under $50" \
User: "Do you have anything like a smart refrigerator that also walks my dog?" \
User: "I need something... nice" \
(Intentionally vague to test clarification abilities)



![image](https://github.com/user-attachments/assets/0c6cbfb8-cd3f-4b9a-a33b-cf2a7a3a616b)



