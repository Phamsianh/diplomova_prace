import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import domain from '../../config';

export const LoginIndex = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [login_fail, setLoginFail] = useState(false)
    const navigate = useNavigate()

	const login = async (e) => {
		e.preventDefault();
		let url = domain + '/token';
		const form_data =  new FormData;
        form_data.append('username', e.target.username.value)
        form_data.append('password', e.target.password.value)
		const res = await fetch(url, {
		    method: 'POST',
		    'content-type': 'application/x-www-form-urlencoded',
		    mode: 'cors',
		    body: form_data,
		})
		if (!res.ok && res.status === 404) {
			setLoginFail(true)
			return
		}
        const {access_token, token_type} = await res.json()
		console.log(access_token, token_type);
        localStorage.setItem('access_token', access_token)
        navigate('/', {state: 'new_login'})
	};
	return (
		<div className="login-index">
			<form onSubmit={login}>
				{login_fail && <p className='login-fail-message'>Login fail</p>}
				<label>
					User Name
					<input
						id="username"
						type="text"
						value={username}
						required
						placeholder="User Name"
						onChange={(e) => setUsername(e.target.value)}
					/>
				</label>
				<label>
					Password
					<input
						id="password"
						type="password"
						value={password}
						required
						placeholder="Password"
						onChange={(e) => setPassword(e.target.value)}
					/>
				</label>
				<button type="submit" className='login-btn'>Login</button>
			</form>
		</div>
	);
};
