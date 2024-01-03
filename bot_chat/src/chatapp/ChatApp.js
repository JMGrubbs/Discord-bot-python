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
            let today = new Date();
            let formattedDate = (today.getMonth() + 1) + '/' + today.getDate() + '/' + today.getFullYear();
            setMessages(messages => [...messages, { id: null, timestamp: formattedDate, message: newMessage, sender: sender, status: 'sent' }]);
            handleAgentResponse(newMessage);
            setNewMessage('');
        }
    };

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function loopWithDelay() {
        getMessages().then(response => {
            setResponseStatus('complete');
            setMessages(response["data"]);
        });
        // while (responseStatus === 'processing') {
        //     getMessages().then((response) => {
        //         console.log("Response:", response["data"]["messages"])
        //         setResponseStatus('complete');
        //         setMessages(response["data"]["messages"]);
        //     });
        //     console.log("Waiting for response...")
        //     await sleep(3000); // Sleep for 1000 milliseconds (1 second)
        // }
    }

    const handleAgentResponse = async (response) => {
        let json_package = {
            "package_type": "agentprompt",
            "prompt": response,
            "assistant_id": "Some other data"
        }
        response = await sendMessage(json_package);
        if (response["status"] === "error") {
            setResponseStatus('error');
            return;
        }
        setResponseStatus('processing');
        setMessages(response["data"]["messages"]);
        loopWithDelay();
    };

    return (
        <div className="chat-app">
            <div className="message-list">
                {messages.map((messageObject, index) => (
                    <Message key={index} text={messageObject.message} sender={messageObject.sender} />
                ))}
            </div>
            <div>
                {responseStatus === 'processing' ? <Message text="processing..." sender="agent" /> : null}
                {responseStatus === 'error' ? <Message text="error getting data..." sender="agent" /> : null}
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
