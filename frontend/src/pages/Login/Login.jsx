import React, { useState } from 'react';
import { checkLogin } from "../../api"
import './Login.css'



const LoginScreen = () => {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const handleLogin = async () => {
		if (!email || !password) {
			alert("Пожалуйста, введите все данные");
			return;
		}
		try {
			await checkLogin(email, password);
			window.location.href = '/';
		} catch(error) {
			alert(error);
		}
	};

	return (
		<div className='login-panel'>
			<h1>Nighdee. Log in</h1>
			<input
				className='login-panel__input'
				placeholder="E-mail"
				value={email}
				onChange={(e) => setEmail(e.target.value)}
			/>
			<input
				type="password"
				className='login-panel__input'
				placeholder="Password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
			/>
			<input
				className='button button--to-go'
				type="button"
				value="Log in"
				onClick={handleLogin}
			/>
			<input
				type="button"
				value="Register"
				onClick={() => window.location.href = '/register'}
			/>
		</div>
	);
};

export { LoginScreen };
