import React, { useState } from 'react';
import './Register.css';
import { registerUser } from "../../api";
import { calculateAge } from '../../utils/DateFucntions';


const RegScreen = () => {
    const [nickname, setNickname] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [birthdate, setBirthdate] = useState('');
    const [consent, setConsent] = useState(false);
    const PRIVACY_LINK = 
    "https://docs.google.com/document/d/11QdpZhEwXqzgPyeY6tpTM_JyKh28AqKz5OHvJetl2Gg/edit?usp=sharing";

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    const handleRegister = async () => {
        if (!consent) {
            alert("Вы должны согласиться с Политикой конфиденциальности");
            return;
        }
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
            window.location.href = '/';
        } catch (error) {
            alert(error.response.data.detail || "Произошла ошибка");
        }
    };

    return (
        <div className="reg-screen">
            <h1>Nighdee. Join us!</h1>
            <input
                type="email"
                className="reg-screen__input"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                className="reg-screen__input"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <input
                className="reg-screen__input"
                placeholder="Nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
            />
            <input
                type="date"
                className="reg-screen__input"
                placeholder="Birthdate"
                value={birthdate}
                onChange={(e) => setBirthdate(e.target.value)}
            />
            <div style={{display: 'flex'}}>
                <input
                    type="checkbox"
                    checked={consent}
                    onChange={(e) => setConsent(e.target.checked)}
                />
                <p>
                    Я соглашаюсь с <a href={PRIVACY_LINK}>Политикой и Правилами сервиса</a>
                </p>
            </div>
            <input
                className="button button--to-go"
                type="button"
                value="Register"
                onClick={handleRegister}
            />
            <input
				type="button"
				value="Log in"
				onClick={() => window.location.href = '/login'}
			/>
        </div>
    );
};

export { RegScreen };
