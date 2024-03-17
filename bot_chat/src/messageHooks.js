import { useState, useEffect } from 'react';
import { getMessages } from './api/fastapi/messages.js';


function useCustomHook() {
    const [messages, setMessages] = useState([]);

    useState(async () => {
        const messages_response = await getMessages();
        setMessages(messages_response);
    }, []);

    const fetchMessageData = async () => {
        const messages_response = await getMessages();
        setMessages(messages_response);
    };

    const addMessage = (message) => {
        setMessages([...messages, message]);
    };

    return { messages, fetchMessageData, addMessage };
}

export default useCustomHook;