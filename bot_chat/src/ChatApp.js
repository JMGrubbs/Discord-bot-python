import React, { useState } from 'react';
import Message from './Message';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = () => {
        if (newMessage) {
            setMessages([...messages, { text: newMessage }]);
            setNewMessage('');
        }
    };

    return (
        <div className="chat-app">
            <div className="message-list">
                {messages.map((message, index) => (
                    <Message key={index} text={message.text} />
                ))}
            </div>
            <div className="message-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatApp;
