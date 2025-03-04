// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const recommendationsContainer = document.getElementById('recommendations');

// User ID - In a real app, this would be handled by authentication
const userId = 'user_' + Math.random().toString(36).substring(2, 9);

// API URL
const API_URL = 'http://localhost:5000/api';

// Event Listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Function to add a message to the chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;

    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message to the API
async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, true);

    // Clear input
    userInput.value = '';

    // Show loading indicator
    const loadingMessageDiv = document.createElement('div');
    loadingMessageDiv.className = 'message bot';
    loadingMessageDiv.innerHTML = '<div class="message-content"><div class="typing-indicator"><span></span><span></span><span></span></div></div>';
    chatMessages.appendChild(loadingMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        // Call API
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();

        // Remove loading message
        chatMessages.removeChild(chatMessages.lastChild);

        // Add bot response to chat
        addMessage(data.response);

        // Update recommendations
        updateRecommendations(data.recommendations);

    } catch (error) {
        console.error('Error:', error);

        // Remove loading message
        chatMessages.removeChild(chatMessages.lastChild);

        // Add error message
        addMessage('Sorry, something went wrong. Please try again later.');
    }
}

// Function to update product recommendations
function updateRecommendations(products) {
    // Clear current recommendations
    recommendationsContainer.innerHTML = '';

    if (!products || products.length === 0) {
        recommendationsContainer.innerHTML = '<p>No recommendations available at the moment.</p>';
        return;
    }

    // Add each product as a card
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';

        // Relevance badge
        let relevanceBadge = '';
        if (product.relevance_score) {
            const relevanceClass = product.relevance_score > 75 ? 'high-relevance' :
                                  product.relevance_score > 50 ? 'medium-relevance' : 'low-relevance';
            relevanceBadge = `<div class="relevance-badge ${relevanceClass}">${product.relevance_score}% match</div>`;
        }

        // Reasoning section
        let reasoningSection = '';
        if (product.reasoning) {
            reasoningSection = `<div class="product-reasoning">${product.reasoning}</div>`;
        }

        productCard.innerHTML = `
            <div class="product-image">
                <div class="product-image-placeholder">[Image: ${product.name}]</div>
            </div>
            ${relevanceBadge}
            <div class="product-name">${product.name}</div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <div class="product-description">${product.description}</div>
            ${reasoningSection}
            <div class="product-meta">
                <span>${product.brand}</span>
                <span>Rating: ${product.rating}/5</span>
            </div>
        `;

        recommendationsContainer.appendChild(productCard);
    });
}

// Add a welcome message when the page loads
window.addEventListener('DOMContentLoaded', () => {
    addMessage('Hello! I\'m your AI shopping assistant. I can help you find products that match your preferences. What are you looking for today?');
});