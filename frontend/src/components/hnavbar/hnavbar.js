import { Link, useNavigate } from 'react-router-dom';
import { UserPageIcon } from '../icon';
import { useContext } from 'react'
import { UserContext } from '../../App'
import './main.css';

export const Hnavbar = () => {
    const { user_data } = useContext(UserContext)
	const navigate = useNavigate();

	function signout() {
		localStorage.removeItem('access_token');
		navigate("/login");
	}

	return (
		<div className="hnavbar">
			<div className="left Breadcrum"></div>

			<div className="right">
				<div className="dropdown">
					<button className="show-dropdown-btn">
						<span>
							<UserPageIcon />
						</span>{' '}
						Hi, {user_data && `${user_data.first_name}`}
					</button>
					<div className="submenu">
						<Link to="/me">Profile</Link>
						<Link to="/me/change_password">Change password</Link>
						<hr />
						<button onClick={signout}>Sign out</button>
					</div>
				</div>
			</div>
		</div>
	);
};
