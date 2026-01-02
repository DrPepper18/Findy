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

export const getEvents = async () => {
    const response = await api.get('/event/', {});
    return response.data;
};

export const RegisterUser = async (user) => {
    try {
        const response = await api.post('/auth/register', user);
        localStorage.setItem('jwt', response.data.token);
        window.location.href = '/';
    } catch (error) {
        console.error('Registration error:', error.response?.data || error.message);
        throw error;
    }
};

export const LoginCheck = async (email, password, setError) => {
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

export const NewEventRequest = async (eventData) => {
    try {
        await api.post('/event/create', eventData);
        window.location.href = '/';
    } catch (error) {
        console.error('Event creation error:', error.response?.data || error.message);
    }
};

export const EventJoinRequest = async (eventID) => {
    try {
        await api.post('/event/join', {"EventID": eventID});
        alert('Вы успешно записаны!');
    } catch (error) {
        const errorMessage = error.response?.data?.detail || "Произошла ошибка при записи";
        console.error('Event join error:', error.response?.data || error.message);
        alert(errorMessage);
    } 
};

export const EventJoinCheck = async (eventID) => {
    console.log(eventID);
    const response = await api.get('/event/joincheck', {params: {"EventID": eventID}});
    return response.data.joined;
}