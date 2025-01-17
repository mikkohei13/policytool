import axios from 'axios';

// Use environment variable for API URL
let BASE_URL = import.meta.env.VITE_API_URL || ''
if (import.meta.env.DEV) {
    BASE_URL = 'http://localhost:5000'
}

export const api = axios.create({
    baseURL: BASE_URL
});
