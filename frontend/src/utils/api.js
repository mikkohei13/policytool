import axios from 'axios';

// In development, the proxy in vite.config.js will handle the requests
// In production, the base URL should be relative to work with any deployment
const BASE_URL = ''

const instance = axios.create({
    baseURL: BASE_URL,
    // Add these settings to help with debugging
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Add request interceptor for debugging
instance.interceptors.request.use(request => {
    console.log('Starting Request:', {
        url: request.url,
        method: request.method,
        data: request.data
    });
    return request;
});

// Add response interceptor for debugging
instance.interceptors.response.use(
    response => {
        console.log('Response:', {
            url: response.config.url,
            status: response.status,
            data: response.data
        });
        return response;
    },
    error => {
        console.error('API Error:', {
            url: error.config?.url,
            status: error.response?.status,
            data: error.response?.data,
            message: error.message
        });
        return Promise.reject(error);
    }
);

export const api = {
    ...instance,
    setToken(token) {
        instance.defaults.headers.common['Authorization'] = `Token ${token}`;
        console.log('Set auth token:', token);
    },
    unsetToken() {
        delete instance.defaults.headers.common['Authorization'];
        console.log('Unset auth token');
    },
    async get(url) {
        const response = await instance.get(url);
        return response.data;
    },
    async post(url, data) {
        const response = await instance.post(url, data);
        return response.data;
    },
    async put(url, data) {
        const response = await instance.put(url, data);
        return response.data;
    },
    async delete(url) {
        const response = await instance.delete(url);
        return response.data;
    }
};
