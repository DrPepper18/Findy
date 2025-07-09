const config = {
    Host_url: "http://localhost:8000/api/v1/"
};


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


export {config, getCookie};