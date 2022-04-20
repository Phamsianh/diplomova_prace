import './navbar.css';
import { Link } from 'react-router-dom';
import {
	CancelIcon,
	FormPageIcon,
	HomePageIcon,
	InstancePageIcon,
	MenuBarIcon,
	SubpageIcon,
	GroupPageIcon,
	PositionPageIcon,
	RolePageIcon,
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
					<span><GroupPageIcon /></span>Groups
				</button>
				<div className="submenu">
					{
						<>
						<Link to="/groups">
							<span><SubpageIcon /></span>{' '}All groups
						</Link>
						</>
					}
				</div>
			</div>
			<div className="dropdown">
				<button className="show-dropdown-btn">
					<span><RolePageIcon /></span>Roles
				</button>
				<div className="submenu">
					{
						<>
						<Link to="/roles">
							<span><SubpageIcon /></span>{' '}All roles
						</Link>
						</>
					}
				</div>
			</div>
			<div className="dropdown">
				<button className="show-dropdown-btn">
					<span><PositionPageIcon /></span>Positions
				</button>
				<div className="submenu">
					{
						<>
						<Link to="/positions">
							<span><SubpageIcon /></span>{' '}All positions
						</Link>
						</>
					}
				</div>
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
						{is_admin && <Link to="/instances">
							<span><SubpageIcon /></span>All instances
						</Link>}
						<Link to="/instances/create">
							<span><SubpageIcon /></span>Create instance
						</Link>
						<Link to="/me/instances">
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
		</nav>
	);
};

export default Navbar;
