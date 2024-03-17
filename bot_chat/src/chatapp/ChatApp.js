import React, { useState } from 'react';
import Message from './Message';
// import NetworkBox from './networkbox/NetworkBox';
// import { getMessages, sendMessage, deleteMessages } from '../api/flask/messages.js';
import { getMessages, sendMessage, deleteMessages } from '../api/fastapi/messages.js';


function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [sender, setSender] = useState('');

    useState(async () => {
        const response = await getMessages();
        setMessages(response);
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
        // response = await sendMessage(response);
        console.log("response from handleAgentResponse", response);
    };


    async function handleClearMessages() {
        setMessages([]);
        await deleteMessages();
        return;
    }

    return (
        <div className="chat-app">
            <div className={`chat box`}>
                <div className={`message-list`}>
                    {[...messages].map((message_obj, index) => (
                        <Message
                            key={index}
                            text={message_obj.content[0].text.value}
                            sender={message_obj.assistant_id ? 'agent' : 'user'}
                        />
                    ))}
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
            {/* <div className={`network box`}>
                <NetworkBox networkobject={networkEvents["proxy_network_messages"]} />
                <NetworkBox networkobject={networkEvents["assistant_network_messages"]} />
            </div> */}
        </div>
    );
}

export default ChatApp;
