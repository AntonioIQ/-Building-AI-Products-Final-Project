let messageHistory = [];

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (message !== '') {
        appendMessage('user', message);
        userInput.value = '';

        messageHistory.push({ role: 'user', content: message });

        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ history: messageHistory })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('assistant', data.response);
            messageHistory.push({ role: 'assistant', content: data.response });
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('assistant', 'Error al procesar la solicitud');
        });
    }
}

function appendMessage(role, content) {
    const chatHistory = document.getElementById('chatHistory');
    const messageElement = document.createElement('div');
    messageElement.classList.add(role === 'user' ? 'userMessage' : 'assistantMessage');
    messageElement.classList.add('indie-flower-regular'); 
    messageElement.innerText = content;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

document.getElementById('newChatButton').addEventListener('click', function() {
    messageHistory = [];
    document.getElementById('chatHistory').innerHTML = '';
    document.getElementById('userInput').value = '';
});

document.addEventListener('DOMContentLoaded', (event) => {
    fetch('http://127.0.0.1:5000/welcome')
        .then(response => response.json())
        .then(data => {
            const chatHistory = document.getElementById('chatHistory');
            const message = document.createElement('div');
            message.className = 'assistantMessage';
            message.classList.add('indie-flower-regular');
            message.innerText = data.response;
            chatHistory.appendChild(message);
        })
        .catch(error => console.error('Error fetching welcome message:', error));
});
