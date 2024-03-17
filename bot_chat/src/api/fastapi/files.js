import axios from 'axios';

const fastApiUrl = process.env.REACT_APP_FASTAPI_URL;
const apiKey = process.env.REACT_APP_API_KEY;

export const get_creations = async () => {
    try {
        const resposne = await axios.get('/creations')
            .then(response => {
                return response.data;
            })
        return resposne;
    } catch (error) {
        console.error('Error fetching agent data:', error);
        return [];
    }
};