# AI shopping assistant
This project implements an interactive AI shopping assistant designed to help users discover products and make more informed purchase decisions. The core objective is to create a conversational agent that can: \
Engage in natural, multi-turn dialogues \
Learn and adapt to user preferences \
Provide intelligent product recommendations 

## Objectives
#### Multi-Turn Dialogue Management: 
Maintain contextual conversation flow \
Ask clarifying questions about user needs \
Provide relevant and personalized responses in natural language
#### Dynamic User Profiling: 
Track and update user preferences in real-time \
Capture insights like price range preferences, preferred brands, product categories of interest, style and color preferences
#### Intelligent Recommendation System: 
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
### RAG-Based Recommendation System
With a limited product database of 20 items and no historical purchase data, traditional recommendation methods fell short. To solve this, I implemented a Retrieval-Augmented Generation (RAG) recommendation system using GPT. \
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
