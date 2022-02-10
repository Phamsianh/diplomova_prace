import './navbar.css';
import { Link } from 'react-router-dom';
import {
	CancelIcon,
	FormPageIcon,
	HomePageIcon,
	InstancePageIcon,
	LoginPageIcon,
	MenuBarIcon,
	SubpageIcon,
} from '../icon';
import { useState, useContext, useEffect } from 'react';
import { UserContext } from '../../App';

const Navbar = () => {
	const [hide_nav, setHideNav] = useState(true)
	const {held_positions}	= useContext(UserContext);
	const [is_admin, setIsAdmin] = useState(false)

	useEffect(() => {
		if (!held_positions) return
		if(held_positions.find(hp => hp.role_id == 1)) setIsAdmin(true)
		else setIsAdmin(false)
	}, [held_positions])
	return (
		<nav className={hide_nav? 'hide-nav' : ''}>
			<button className='hide-nav-btn' onClick={() => setHideNav(!hide_nav)}>
				{hide_nav? <MenuBarIcon/> : <CancelIcon/>}
			</button>
			<div className="dropdown">
				<Link to="/">
					<span><HomePageIcon /></span>Home
				</Link>
			</div>
			<div className="dropdown">
				<button className="show-dropdown-btn">
					<span><FormPageIcon /></span>Forms
				</button>
				<div className="submenu">
					{
						<>
						<Link to="/forms">
							<span><SubpageIcon /></span>{' '}All forms
						</Link>
						{is_admin && <Link to="/forms/create">
							<span><SubpageIcon /></span>Create form
						</Link>}
						{is_admin && <Link to="/me/forms">
							<span><SubpageIcon /></span>My forms
						</Link>}
						</>
					}
				</div>
			</div>
			<div className="dropdown">
				<button className="show-dropdown-btn">
					<span>
						<InstancePageIcon />
					</span>{' '}
					Instances
				</button>
				<div className="submenu">
					{
						<>
						<Link to="/instances/create">
							<span><SubpageIcon /></span>Create instance
						</Link>
						<Link to="me/instances">
							<span><SubpageIcon /></span>My created instances
						</Link>
						<Link to="/me/participated_instances">
							<span><SubpageIcon /></span>Participated instances
						</Link>
						<Link to="/me/pending_instances">
							<span><SubpageIcon /></span>Pending instances
						</Link>
						</>
					}
				</div>
			</div>
			<div className="dropdown">
				<Link to="/login">
					<span><LoginPageIcon /></span>Login
				</Link>
			</div>
		</nav>
	);
};

export default Navbar;
