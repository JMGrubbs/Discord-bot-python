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

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function loopWithDelay() {
        while (responseStatus === 'processing') {
            getMessages().then((response) => {
                setResponseStatus(response["status"]);
                setMessages(messages => [...messages]);
            });
            await sleep(3000); // Sleep for 1000 milliseconds (1 second)
        }
    }

    const handleAgentResponse = async (response) => {
        let json_package = {
            "package_type": "agentprompt",
            "prompt": response,
            "assistant_id": "Some other data"
        }
        response = await sendMessage(json_package);
        setResponseStatus(response["status"]);
        loopWithDelay();
    };

    return (
        <div className="chat-app">
            <div className="message-list">
                {messages.map((message, index) => (
                    <Message key={index} text={message.text} sender={message.sender} />
                ))}
            </div>
            <div>
                {responseStatus === 'processing' ? <Message text="processing..." sender="agent" /> : null}
                {responseStatus === 'error' ? <Message text="timed out" sender="agent" /> : null}
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
