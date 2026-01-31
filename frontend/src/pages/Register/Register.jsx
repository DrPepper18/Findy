import React, { useState } from 'react';
import './Register.css';
import { registerUser } from "../../api";
import { calculateAge } from '../../utils/DateFucntions';


const RegScreen = () => {
    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [birthdate, setBirthdate] = useState('');

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const handleRegister = async () => {
        if (!validateEmail(email)) {
            alert("Некорректный формат почты");
            return;
        }
        const age = calculateAge(birthdate);
        if (age < 18 || age > 100) {
            alert("Для регистрации в сервисе Вам должно быть больше 18 лет.");
            return;
        }
        const user = {
            name: nickname,
            email: email,
            password: password,
            birthdate: birthdate,
        };

        try {
            await registerUser(user);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="reg-screen">
            <h1>Nighdee. Join us!</h1>
            <input
                className="reg-screen__input"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <br />
            <input
                type="password"
                className="reg-screen__input"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <input
                className="reg-screen__input"
                placeholder="Nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
            />
            <br />
            <input
                type="date"
                className="reg-screen__input"
                placeholder="Birthdate"
                value={birthdate}
                onChange={(e) => setBirthdate(e.target.value)}
            />
            <br />
            <input
                className="button button--to-go"
                type="button"
                value="Register"
                onClick={handleRegister}
            />
        </div>
    );
};

export { RegScreen };
