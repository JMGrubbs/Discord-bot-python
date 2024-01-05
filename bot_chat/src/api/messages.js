import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const sendMessage = async (mostRecentMessage) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };

        const response = await axios.post(apiUrl + "prompt", mostRecentMessage, { headers: headers });
        return response.data["response"];
    } catch (error) {
        console.error('Error fetching data:', error);
        return { "messages": [{ "message": "Error sending message", "sender": "agent", "status": "error" }] };
    }
};

export const getMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };

        const response = await axios.get(apiUrl + "messages", { headers: headers });

        return response.data["response"];
    } catch (error) {
        console.error('Error fetching data:', error);
        return { "status": "error", "message": "Error Getting responses from api" };
    }
}

export const deleteMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };

        const response = await axios.delete(apiUrl + "deletemessages", { headers: headers });

        return response.data["response"];
    } catch (error) {
        console.error('Error fetching data:', error);
        return { "status": "error", "message": "Error deleteing responses from api" };
    }
}