import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const getMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.get(fastApiUrl + "agent/proxy/messages", { headers: headers })
            .then(response => {
                return response.data["data"]
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching data using message/get:', error);
        return ["Error: API Error"];
    }
};

export const deleteMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };

        const response = await axios.delete(fastApiUrl + "deletemessages", { headers: headers });
        return response.data["response"];
    } catch (error) {
        console.error('Error fetching data using deleteMessage:', error);
        return ["Error: API Error"];
    }
}