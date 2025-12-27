// PWA Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Service Worker Registered!', reg))
            .catch(err => console.log('Service Worker registration failed', err));
    });
}

// Chatbot Logic
document.addEventListener('DOMContentLoaded', () => {
    const toggler = document.querySelector('.chatbot-toggler');
    const chatContainer = document.querySelector('.chatbot-container');
    const chatBody = document.querySelector('.chat-body');
    const chatInput = document.querySelector('.chat-input input');
    const sendBtn = document.querySelector('.chat-input button');

    // Toggle Chat
    toggler.addEventListener('click', () => {
        const isVisible = chatContainer.classList.contains('show');
        if (isVisible) {
            chatContainer.classList.remove('show');
        } else {
            chatContainer.classList.add('show');
            if (chatBody.children.length === 0) {
                addMessage('bot', 'Shoot your doubt! I am myfrnd.');
            }
        }
    });

    // Send Message
    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        chatInput.value = '';

        // Simulate typing or loading
        const loadingId = addMessage('bot', 'Typing...');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();

            // Update loading message with response
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.textContent = data.response;
            } else {
                addMessage('bot', data.response);
            }
        } catch (error) {
            console.error('Error:', error);
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) loadingMsg.textContent = "Sorry, I'm having trouble connecting right now.";
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('chat-message', sender);
        msgDiv.textContent = text;

        // Generate simple ID for updating later
        const id = 'msg-' + Date.now();
        msgDiv.id = id;

        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        return id;
    }
});
