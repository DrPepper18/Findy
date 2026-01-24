import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('jwt');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('jwt');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);


export const registerUser = async (user) => {
    try {
        const response = await api.post('/auth/register', user);
        localStorage.setItem('jwt', response.data.token);
        window.location.href = '/';
    } catch (error) {
        console.error('Registration error:', error.response?.data || error.message);
        throw error;
    }
};


export const checkLogin = async (email, password, setError) => {
    try {
        const response = await api.post('/auth/login', { email, password });
        localStorage.setItem('jwt', response.data.token);
        window.location.href = '/';
    } catch (error) {
        const message = error.response?.status === 401 || error.response?.status === 400
            ? 'Неверные данные входа'
            : 'Произошла ошибка. Попробуйте позже.';
        setError(message);
    }
};


export const getUserInfo = async () => {
    try {
        const response = await api.get('/auth/');
        return response.data;
    } catch {
        console.error("Произошла ошибка. Попробуйте позже");
    }
}


export const updateUserInfo = async (name, age) => {
    try {
        const response = await api.patch('/auth/', {name, age});
        return response.data;
    } catch {
        console.error("Произошла ошибка. Попробуйте позже");
    }
}


export const getEvents = async () => {
    const response = await api.get('/event/', {});
    console.log(response.data);
    return response.data;
};


export const createEvent = async (eventData) => {
    try {
        await api.post('/event/', eventData);
        window.location.href = '/';
    } catch (error) {
        console.error('Event creation error:', error.response?.data || error.message);
    }
};


export const joinEvent = async (event_id) => {
    try {
        await api.post(`/book/${event_id}`);
    } catch (error) {
        const errorMessage = error.response?.data?.detail || "Произошла ошибка при записи";
        console.error('Event join error:', error.response?.data || error.message);
        alert(errorMessage);
    } 
};


export const cancelJoin = async (event_id) => {
    try {
        await api.delete(`/book/${event_id}`);
    } catch (error) {
        const errorMessage = error.response?.data?.detail || "Произошла ошибка при записи";
        console.error('Event join error:', error.response?.data || error.message);
        alert(errorMessage);
    } 
};


export const checkEventJoinStatus = async (event_id) => {
    const response = await api.get(`/book/${event_id}`);
    return response.data.joined;
}