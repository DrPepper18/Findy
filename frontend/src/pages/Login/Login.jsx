import React, { useState } from 'react';
import { checkLogin } from "../../api"
import './Login.css'



const LoginScreen = () => {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');

	const handleLogin = () => {
		setError('');
		checkLogin(email, password, setError);
		window.location.href = '/';
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
			<br />
			<input
				type="password"
				className='login-panel__input'
				placeholder="Password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
			/>
			<br />
			{error && <p style={{color: 'red'}}>{error}</p>}
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
