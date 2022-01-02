import { useState } from 'react';
import './navbar.css';
import { Link } from 'react-router-dom';
import {
	FormPageIcon,
	HomePageIcon,
	InstancePageIcon,
	LoginPageIcon,
	SubpageIcon,
} from '../icon';

const Navbar = () => {
	function showSubmenu(e) {
		e.target.nextSibling.classList.toggle('show-submenu');
	}

	return (
		<nav>
			<div className="nav-bar">
				<div className="dropdown">
					<Link to="/">
						<span>
							<HomePageIcon />
						</span>
						Home
					</Link>
				</div>
				<div className="dropdown">
					<button className="item" onClick={showSubmenu}>
						<span>
							<FormPageIcon />
						</span>
						Forms
					</button>
					<div className="submenu">
						{
							<>
								<Link to="/forms">
									<span>
										<SubpageIcon />
									</span>{' '}
									Index
								</Link>
								<Link to="/forms/create">
									<span>
										<SubpageIcon />
									</span>
									Form Create
								</Link>
							</>
						}
					</div>
				</div>
				<div className="dropdown">
					<button className="item" onClick={showSubmenu}>
						<span>
							<InstancePageIcon />
						</span>{' '}
						Instances
					</button>
					<div className="submenu">
						{
							<>
								<Link to="/instances">
									<span>
										<SubpageIcon />
									</span>
									Index
								</Link>
								<Link
									to="/instances/create"
								>
									<span>
										<SubpageIcon />
									</span>
									Create Instance
								</Link>
							</>
						}
					</div>
				</div>
				<div className="dropdown">
					<Link to="/login">
						<span>
							<LoginPageIcon />
						</span>
						Login
					</Link>
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
