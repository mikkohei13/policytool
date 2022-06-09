import axios from 'axios';

class API {

    constructor() {
        this.api = axios.create({
            baseURL: 'http://localhost:5000',
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        this.token = null;
    }

    setToken(token) {
        this.token = token
        this.api.defaults.headers['Authorization'] = `Token ${this.token}`
    }

    unsetToken() {
        this.token = null
        delete this.api.defaults.headers['Authorization']
    }

    /**
     * Calls an API endpoint using a POST request with the body as a JSON payload.
     *
     * @param path the URL path
     * @param body the object body that will be sent with the POST request as JSON
     * @returns {Promise<Object>} the response JSON
     */
    async post(path, body) {
        const response = await this.api.post(path, body);
        return response.data;
    }

    /**
     * Calls an API endpoint using a GET request.
     *
     * @param path the action to call
     * @returns {Promise<Object>} the response JSON
     */
    async get(path) {
        const response = await this.api.get(path);
        return response.data;
    }
}


export const api = new API()
