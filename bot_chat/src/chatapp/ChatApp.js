import React, { useState } from 'react';
import Message from './Message';
import { getMessages, sendMessage } from '../api/messages.js';


function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [sender, setSender] = useState('');
    const [responseStatus, setResponseStatus] = useState('complete');

    const handleSendMessage = () => {
        if (newMessage) {
            setMessages(messages => [...messages, { text: newMessage, sender: sender }]);
            handleAgentResponse(newMessage);
            setNewMessage('');
        }
    };

    const handleAgentResponse = async (response) => {
        let json_package = {
            "package_type": "agentprompt",
            "prompt": response,
            "assistant_id": "Some other data"
        }
        response = await sendMessage(json_package);
        setResponseStatus(response["status"]);
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
