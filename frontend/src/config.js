const config = {
    Host_url: "http://localhost:8000/api/v1/"
};


const getApiKey = async () => {
    let response = await fetch(config.Host_url + 'yandexmap');
    let data = await response.json();
    return data.api_key || "";
}


const getCookie = async (name) => {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    return null;
}


export {config, getCookie, getApiKey};