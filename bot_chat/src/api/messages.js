import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const sendMessage = async (json_package) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const response = await axios.post(apiUrl + "prompt", json_package, { headers: headers });
        console.log("Response:", response.data["response"]);
        return { "data": response.data["response"] };
    } catch (error) {
        console.error('Error fetching data:', error);
        return { "status": "error", "message": "Error Getting response from agent" };
    }
};

export const getMessages = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const response = await axios.get(apiUrl + "messages", { headers: headers });
        return { "data": response.data["messages"] };
    } catch (error) {
        console.error('Error fetching data:', error);
        return 'Error Getting response from agent';
    }
}
