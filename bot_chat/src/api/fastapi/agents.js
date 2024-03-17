import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;
const defaultAgent = process.env.REACT_APP_DEFAULT_AGENT;

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
        return [];
    }
};

export const select_proxy_agent = async (agent_id = defaultAgent) => {
    try {
        const headers = {
            "api-key": apiKey,
        };
        let url = fastApiUrl + "agent/proxy/agent/" + agent_id;
        const resposne = await axios.post(url, { headers: headers })
            .then(response => {
                return response.data
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [];
    }
};

export const send_proxy_message = async (message) => {
    try {
        const headers = {
            "api-key": apiKey,
        };
        let url = fastApiUrl + "agent/message";
        const resposne = await axios.post(url, { "user-input": message }, { headers: headers })
            .then(response => {
                return response.data
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [];
    }
};
