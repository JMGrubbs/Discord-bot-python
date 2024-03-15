import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const sendMessage = async (mostRecentMessage) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.post(fastApiUrl + "message/sendmessage", mostRecentMessage, { headers: headers })
            .then(response => { return response.data["response"] });
        return resposne;
    } catch (error) {
        console.error('Error fetching data using sendMessage:', error);
        return { "messages": [], "file": {}, "network_box": { "proxy_network_messages": [{ "agent": "NONE", "task": "GetMessages", "message": "Error: Network Error" }], "assistant_network_messages": [{ "agent": "NONE", "task": "GetMessages", "message": "Error: Network Error" }] } };
    }
};

export const getMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.get(fastApiUrl + "message/getmessages", { headers: headers })
            .then(response => {
                return response.data["response"]
            });
        console.log("response from getMessages", resposne);
        return resposne;
    } catch (error) {
        console.error('Error fetching data using getMessages:', error);
        return { "messages": [], "file": {}, "network_box": { "proxy_network_messages": [{ "agent": "NONE", "task": "GetMessages", "message": "Error: Network Error" }], "assistant_network_messages": [{ "agent": "NONE", "task": "GetMessages", "message": "Error: Network Error" }] } };
    }
}

export const deleteMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };

        const response = await axios.delete(fastApiUrl + "deletemessages", { headers: headers });
        console.log("response from deleteMessages", response);
        return response.data["response"];
    } catch (error) {
        console.error('Error fetching data using deleteMessage:', error);
        return { "status": "error", "message": "Error deleteing responses from api" };
    }
}