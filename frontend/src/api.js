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
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const response = await api.get('/auth/refresh', { withCredentials: true });

                const newAccessToken = response.data.token;
                localStorage.setItem('jwt', newAccessToken);
                originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

                return api(originalRequest);
                
            } catch (refreshError) {
                localStorage.removeItem('jwt');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);


export const registerUser = async (user) => {
    try {
        const response = await api.post('/auth/register', user, { withCredentials: true });
        localStorage.setItem('jwt', response.data.token);
    } catch (error) {
        console.error('Registration error:', error.response?.data || error.message);
        throw error;
    }
};


export const checkLogin = async (email, password) => {
    try {
        const response = await api.post('/auth/login', { email, password }, { withCredentials: true });
        localStorage.setItem('jwt', response.data.token);
    } catch (error) {
        let message = null;
        switch(error.response.status) {
            case 401:
                message = "Неправильные данные для входа";
                break;
            case 404:
                message = "Не найден такой пользователь";
                break;
            default:
                message = "Неизвестная ошибка. Повторите позже";
        }
        throw message;
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


export const updateUserInfo = async (name, birthdate) => {
    try {
        const response = await api.patch('/auth/', {name, birthdate});
        return response.data;
    } catch {
        console.error("Произошла ошибка. Попробуйте позже");
    }
}


export const deleteUser = async () => {
    try {
        const response = await api.delete('/auth/', { withCredentials: true });
        localStorage.clear();
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