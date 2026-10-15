document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Function to scroll to the bottom of the chat window
    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Function to format text with bullets
    const formatText = (text) => {
        // Split text into lines
        const lines = text.split('\n');
        let html = '';
        let inList = false;
        
        lines.forEach(line => {
            const trimmedLine = line.trim();
            
            // Check if line starts with bullet markers
            if (trimmedLine.startsWith('* ') || trimmedLine.startsWith('• ') || trimmedLine.startsWith('- ')) {
                if (!inList) {
                    html += '<ul>';
                    inList = true;
                }
                // Remove the bullet marker and create list item
                const content = trimmedLine.substring(2).trim();
                html += `<li>${content}</li>`;
            } else if (trimmedLine === '') {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += '<br>';
            } else {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += `<p>${trimmedLine}</p>`;
            }
        });
        
        // Close list if still open
        if (inList) {
            html += '</ul>';
        }
        
        return html;
    };

    // Function to create and append a new message element
    const appendMessage = (text, sender, timestamp = null) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('message-avatar');
        
        const avatar = document.createElement('div');
        avatar.classList.add('avatar', `${sender}-avatar`);
        avatar.textContent = sender === 'user' ? 'U' : 'B';
        avatarDiv.appendChild(avatar);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Use innerHTML for formatted text, textContent for plain text
        if (text.includes('*') || text.includes('•') || text.includes('- ')) {
            const contentDiv = document.createElement('div');
            contentDiv.innerHTML = formatText(text);
            messageContent.appendChild(contentDiv);
        } else {
            const p = document.createElement('p');
            p.textContent = text;
            messageContent.appendChild(p);
        }
        
        const timeSpan = document.createElement('span');
        timeSpan.classList.add('message-time');
        timeSpan.textContent = timestamp || getCurrentTime();
        messageContent.appendChild(timeSpan);
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    };

    // Function to get current time in HH:MM format
    const getCurrentTime = () => {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    };

    // Function to create typing indicator
    const showTypingIndicator = () => {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        typingDiv.id = 'typing-indicator';
        
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('message-avatar');
        
        const avatar = document.createElement('div');
        avatar.classList.add('avatar', 'bot-avatar');
        avatar.textContent = 'B';
        avatarDiv.appendChild(avatar);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const typingDots = document.createElement('div');
        typingDots.classList.add('typing-dots');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingDots.appendChild(dot);
        }
        
        messageContent.appendChild(typingDots);
        typingDiv.appendChild(avatarDiv);
        typingDiv.appendChild(messageContent);
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        
        return typingDiv;
    };

    // Function to handle the chat submission
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (message === '') return;

        // 1. Display user message
        appendMessage(message, 'user');
        userInput.value = ''; // Clear input
        sendButton.disabled = true; // Disable button while waiting

        // 2. Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            // 3. Send message to the Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            // 4. Remove typing indicator
            if (typingIndicator && typingIndicator.parentNode) {
                typingIndicator.parentNode.removeChild(typingIndicator);
            }

            if (response.ok) {
                const data = await response.json();
                // 5. Display bot response
                appendMessage(data.response, 'bot');
            } else {
                const errorData = await response.json();
                appendMessage(`Error: ${errorData.response || 'Could not connect to the server.'}`, 'bot');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            // 4. Remove typing indicator if still present
            if (typingIndicator && typingIndicator.parentNode) {
                typingIndicator.parentNode.removeChild(typingIndicator);
            }
            appendMessage('A network error occurred. Please try again.', 'bot');
        } finally {
            sendButton.disabled = false; // Re-enable button
            userInput.focus(); // Focus input for next message
        }
    };

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial scroll to bottom
    scrollToBottom();
});