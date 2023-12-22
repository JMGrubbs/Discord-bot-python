import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;
const apiKey = process.env.REACT_APP_API_KEY;

const sendAgentPrompt = async (json_package) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const response = await axios.post(apiUrl + "send_prompt", json_package, { headers: headers });
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return 'Error Getting response from agent';
    }
};

export default sendAgentPrompt;
