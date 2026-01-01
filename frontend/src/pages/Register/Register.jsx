import { useState } from 'react';
import './Register.css';
import {RegisterUser} from "../../api";

const RegScreen = () => {
    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailError, setEmailError] = useState('');

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const handleRegister = async () => {
        if (!validateEmail(email)) {
            setEmailError('Invalid email format');
            return;
        }
        setEmailError('');
        const user = {
            name: nickname,
            email: email,
            password: password,
        };

        try {
            await RegisterUser(user);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="reg-screen">
            <h1>Findy. Join us!</h1>
            <input
                className="input-field"
                placeholder="Nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
            />
            <br />
            <input
                className="input-field"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            {emailError && <p className="error-message">{emailError}</p>}
            <br />
            <input
                type="password"
                className="input-field"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <input
                className="ToGoButton"
                type="button"
                value="Register"
                onClick={handleRegister}
            />
        </div>
    );
};

export { RegScreen };
