import React, { useState } from 'react';
import Message from './Message';
import { getMessages, sendMessage, deleteMessages } from '../api/messages.js';


function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [sender, setSender] = useState('');
    const [responseStatus, setResponseStatus] = useState('complete');

    useState(async () => {
        const response = await getMessages();
        setMessages(response["messages"]);
    }, []);

    const handleSendMessage = () => {
        if (newMessage) {
            let message = { id: null, message: newMessage, sender: sender, status: 'sent' };
            setMessages(messages => [...messages, message]);
            handleAgentResponse(message);
            setNewMessage('');
        }
    };

    const handleAgentResponse = async (response) => {
        response = await sendMessage(response);
        if ("error" in response) {
            console.error("Error in sending message:", response["error"]);
            setResponseStatus('error');
            return;
        }
        setResponseStatus('processing');
        setMessages(response["messages"]);
        loopWithDelay();
    };

    async function loopWithDelay() {
        let localResponseStatus = 'processing'; // Local variable for loop control because state is not updated immediately

        while (localResponseStatus === 'processing') {
            try {
                const response = await getMessages();
                const lastStatus = response["messages"][response["messages"].length - 1]["status"]; // Get the status of the last message in the response
                if (lastStatus === "complete") {
                    localResponseStatus = 'complete'; // Update local variable
                    setResponseStatus('complete'); // Update state
                    setMessages(response["messages"]); // Update state
                } else {
                    console.log("Waiting for response...");
                    await sleep(3000); // Sleep for 3 seconds
                }
            } catch (error) {
                console.error("Error in getting messages:", error);
                break;
            }
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function handleClearMessages() {
        setMessages([]);
        await deleteMessages();
        return;
    }

    return (
        <div className="chat-app">
            <div className={`message list`}>
                {[...messages].reverse().map((messageObject, index) => (
                    <Message key={index} text={messageObject.message} sender={messageObject.sender} />
                ))}
            </div>
            <div>
                {responseStatus === 'processing' ? <Message text="processing..." sender="agent" /> : null}
                {responseStatus === 'error' ? <Message text="error getting data..." sender="agent" /> : null}
            </div>
            <div className={`message-list-input`}>
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={newMessage}
                    onChange={(e) => {
                        setSender('user')
                        setNewMessage(e.target.value)
                    }}
                />
                <button className='message-list-input button send' onClick={handleSendMessage}>Send</button>
                <button className='message-list-input button clear' onClick={handleClearMessages}>Clear</button>
            </div>
        </div>
    );
}

export default ChatApp;
