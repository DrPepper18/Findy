import { useState } from 'react';
import { LoginCheck } from "../../api"
import './Login.css'



const LoginScreen = () => {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');

	const handleLogin = () => {
		setError('');
		LoginCheck(email, password, setError);
	};

	return (
		<div className='LoginPanel'>
			<h1>Findy. Log in</h1>
			<input
				className='input-field'
				placeholder="E-mail"
				value={email}
				onChange={(e) => setEmail(e.target.value)}
			/>
			<br />
			<input
				type="password"
				className='input-field'
				placeholder="Password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
			/>
			<br />
			{error && <p style={{color: 'red'}}>{error}</p>}
			<input
				className='ToGoButton'
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

export { LoginScreen, LoginCheck };
