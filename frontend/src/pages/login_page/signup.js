import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import domain from '../../config';
import Logo from './logo.png'

export const SignUp = () => {
	const [first_name, setFirstName] = useState('');
	const [last_name, setLastName] = useState('');
	const [user_name, setUserName] = useState('');
	const [password, setPassword] = useState('');
	const [email, setEmail] = useState('');
	const [phone, setPhone] = useState('');
	const [birthdate, setBirthdate] = useState('');

	const [registration_fail, setRegistrationFail] = useState(false)
    const navigate = useNavigate()

	const signup = async (e) => {
		e.preventDefault();
        const req_bod = {
            first_name,
            last_name,
            user_name,
            password,
            email,
            // phone,
            // birthdate
        }
        // console.log(req_bod);
		let url = domain + '/registration';

		const res = await fetch(url, {
		    method: 'POST',
		    // mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
		    body: JSON.stringify(req_bod),
		})
		if (!res.ok) {
			setRegistrationFail(true)
			return
		}
        const new_user_data = await res.json()
		// console.log(new_user_data);
        navigate('/login')
	};
	return (
		<div className="signup">
			<div className="signup-htm">
				<div className="logo"><img src={Logo} alt="logo" /></div>
				<form onSubmit={signup}>
					{registration_fail && <p className='login-fail-message'>Sign up fail</p>}
					<label title='First name only contains alphabet characters'>
						First Name
						<input
							id="first_name"
							type="text"
							value={first_name}
							required
							maxLength={50}
							placeholder="First Name"
							onChange={(e) => setFirstName(e.target.value)}
						/>
					</label>
					<label title='Last name only contains alphabet characters'>
						Last Name
						<input
							id="last_name"
							type="text"
							value={last_name}
							required
							maxLength={50}
							placeholder="Last Name"
							onChange={(e) => setLastName(e.target.value)}
						/>
					</label>
					<label title='User name must contain only uppercase or lowercase letter, space, number and special character -_!@#$%^&*()?{}'>
						User Name
						<input
							id="username"
							type="text"
							value={user_name}
							required
							maxLength={50}
							placeholder="User Name"
							onChange={(e) => setUserName(e.target.value)}
						/>
					</label>
					<label title='password must contain at least 8 characters, at least 1 uppercase letter, 1 lower letter, 1 number and can contain special character'>
						Password
						<input
							id="password"
							type="password"
							value={password}
							required
							minLength={8}
							maxLength={50}
							placeholder="Password"
							onChange={(e) => setPassword(e.target.value)}
						/>
					</label>
					<label>
						Email
						<input
							id="email"
							type="email"
							value={email}
							required
							placeholder="Email"
							onChange={(e) => setEmail(e.target.value)}
						/>
					</label>
					{/* <label>
						Phone
						<input
							id="phone"
							type="number"
							value={phone}
							required
							placeholder="Phone"
							onChange={(e) => setPhone(e.target.value)}
						/>
					</label>
					<label>
						Birthdate
						<input
							id="birthdate"
							type="date"
							value={birthdate}
							required
							placeholder="Birthdate"
							onChange={(e) => setBirthdate(e.target.value)}
						/>
					</label> */}
					<button type="submit" className='signup-btn'>Sign Up</button>
					<Link to='/login'>Sign In</Link>
				</form>
			</div>

		</div>
	);
};
