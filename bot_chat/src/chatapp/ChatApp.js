import React, { useState } from 'react';
import Message from './Message';
// import NetworkBox from './networkbox/NetworkBox';
import { select_proxy_agent } from '../api/fastapi/agents';

function ChatApp({ messages, fetchMessageData, addMessage }) {
    const [newMessage, setNewMessage] = useState('');
    // const [localMessages, setLocalMessages] = useState([]);

    useState(async () => {
        await select_proxy_agent();
        // const messages_response = await getMessages();
        // if (messages.length !== 0) {
        //     setLocalMessages(messages);
        // }
    }, []);

    const handleSendMessage = async (event) => {
        if (newMessage) {
            let temp = event.currentTarget.getAttribute('id');
            console.log('newMessage:', newMessage, temp);
            // addMessage({ content: [{ text: { value: newMessage } }, { type: 'text' }], assistant_id: null });
            console.log(messages);

            setNewMessage(null);
        }
    };


    async function handleClearMessages() {
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
