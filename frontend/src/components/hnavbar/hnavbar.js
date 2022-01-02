import { Link } from 'react-router-dom';
import { UserPageIcon } from '../icon';
import { useContext } from 'react'
import { UserContext } from '../../App'
import './main.css';

export const Hnavbar = () => {
    const { user_data } = useContext(UserContext)

    function showSubmenu(e) {
		e.target.nextSibling.classList.toggle('show-submenu');
	}
	return (
		<div className="hnavbar">
			<div className="left Breadcrum"></div>

			<div className="right">
				<div className="dropdown">
					<button className="item" onClick={showSubmenu}>
						<span>
							<UserPageIcon />
						</span>{' '}
						Hi, {user_data && `${user_data.first_name}`}
					</button>
					<div className="submenu">
						<Link to="/user">Profile</Link>
						<Link to="/user">Change password</Link>
					</div>
				</div>
			</div>
		</div>
	);
};
