import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const get_threads = async () => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        const resposne = await axios.get(fastApiUrl + "thread/get", { headers: headers })
            .then(response => {
                return response.data["data"]
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [];
    }
};

export const select_proxy_thread = async (thread_id) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
            "api-key": apiKey,
        };
        let url = fastApiUrl + "agent/proxy/thread/" + thread_id;
        const resposne = await axios.post(url, {}, { headers: headers })
            .then(response => {
                return response.data
            });
        return resposne;
    } catch (error) {
        console.error('Error fetching thread data:', error);
        return [];
    }
};