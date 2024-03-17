import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const get_agents = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.get(fastApiUrl + "agent/get", { headers: headers })
            .then(response => {
                return response.data
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [{ "Error": "Network Error" }];
    }
};

export const select_proxy_agent = async (agent_id) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.post(fastApiUrl + "agent/proxy/agent/" + agent_id, { headers: headers })
            .then(response => {
                return response.data
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [{ "Error": "Network Error" }];
    }
};