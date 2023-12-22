import React, { useState } from 'react';
import Message from './Message';
import sendAgentPrompt from '../agentapi/tools.js';


function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [sender, setSender] = useState('');

    const handleSendMessage = () => {
        if (newMessage) {
            setMessages(messages => [...messages, { text: newMessage, sender: sender }]);
            handleAgentResponse({ "prompt": newMessage });
            setNewMessage('');
        }
    };

    const handleAgentResponse = async (response) => {
        let json_package = {
            "message": response,
            "assistant_id": "Some other data"
        }
        response = await sendAgentPrompt(json_package);
        console.log(response);
        setMessages(messages => [...messages, { text: response["response"], sender: 'agent' }]);
    };

    return (
        <div className="chat-app">
            <div className="message-list">
                {messages.map((message, index) => (
                    <Message key={index} text={message.text} sender={message.sender} />
                ))}
            </div>
            <div className="message-input">
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={newMessage}
                    onChange={(e) => {
                        setSender('user')
                        setNewMessage(e.target.value)
                    }}
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatApp;
