document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const statusIndicator = document.querySelector('.status-indicator');

    // Add a message to the chat
    function addMessage(message, isUser = false) {
        // Filter out thinking content if present
        let cleanedMessage = message;
        if (!isUser) {
            // Remove any text inside <think> tags and the tags themselves
            cleanedMessage = message.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        const icon = document.createElement('i');
        icon.className = isUser ? 'fas fa-user' : 'fas fa-robot';
        avatar.appendChild(icon);
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        const messageText = document.createElement('p');
        messageText.textContent = cleanedMessage;
        messageContent.appendChild(messageText);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show typing indicator while waiting for response
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.id = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hide typing indicator when response arrives
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Clean thinking content for speech synthesis
    function cleanThinkingContent(message) {
        return message.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
    }

    // Send a message to the Groq-powered API
    async function sendMessage(message) {
        try {
            const response = await fetch('/api/v1/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message
                }),
            });

            const data = await response.json();
            
            if (data.success) {
                // Store original response for possible debugging
                const originalResponse = data.response;
                
                // Add cleaned response to chat
                addMessage(data.response);
                
                // Return the cleaned response for speech synthesis
                return cleanThinkingContent(data.response);
            } else {
                console.error('API Error:', data.error);
                addMessage("I'm sorry, I encountered an error processing your request. Please try again.");
                return null;
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage("I'm sorry, I couldn't connect to the server. Please try again later.");
            return null;
        }
    }

    // Check API status and update indicator
    async function checkApiStatus() {
        try {
            const response = await fetch('/api/v1/models');
            if (response.ok) {
                const data = await response.json();
                
                if (statusIndicator) {
                    if (data.using_groq && data.groq_api_configured) {
                        statusIndicator.innerHTML = `<span class="status-dot online"></span> Using Groq: ${data.groq_model}`;
                        statusIndicator.classList.remove('offline');
                        statusIndicator.classList.add('online');
                    } else {
                        statusIndicator.innerHTML = '<span class="status-dot offline"></span> API Not Configured';
                        statusIndicator.classList.remove('online');
                        statusIndicator.classList.add('offline');
                    }
                }
            }
        } catch (error) {
            console.error('Failed to check API status:', error);
            if (statusIndicator) {
                statusIndicator.innerHTML = '<span class="status-dot offline"></span> API Offline';
                statusIndicator.classList.remove('online');
                statusIndicator.classList.add('offline');
            }
        }
    }

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, true);
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message and get response
        await sendMessage(message);
        
        // Hide typing indicator
        hideTypingIndicator();
    });

    // Check API status on page load and periodically
    checkApiStatus();
    setInterval(checkApiStatus, 30000);
    
    // Make these functions accessible globally for voice.js
    window.addMessage = addMessage;
    window.cleanThinkingContent = cleanThinkingContent;
});