import Tab from '../../components/tab/tab';
import { useState, useEffect, useContext } from 'react';
import { useController } from '../../controllers';
import { UserContext } from '../../App';
import { Link } from 'react-router-dom';
import './main.css'

const HomePage = () => {
	const [forms_length, setFormsLength] = useState(null);
	const [instances_length, setInstancesLength] = useState(null);
	const [groups_length, setGroupsLength] = useState(null);
	const [roles_length, setRolesLength] = useState(null);
	const [positions_length, setPositionsLength] = useState(null);
	
	const {held_positions}	= useContext(UserContext);
	const [is_admin, setIsAdmin] = useState(false)

	const { FormCtlr, InstanceCtlr, GroupCtlr, RoleCtlr, PositionCtlr } = useController();

	useEffect(() => {
		if (!held_positions) return
		if(held_positions.find(hp => hp.role_id == 1)) setIsAdmin(true)
		else setIsAdmin(false)
	}, [held_positions])

	useEffect(() => {
		// get all forms, instances
		FormCtlr.get_rsc_col_lth().then((data) => {
				setFormsLength(data);
			})
		InstanceCtlr.get_rsc_col_lth().then(data => {
			setInstancesLength(data);
		})
		GroupCtlr.get_rsc_col_lth().then(data => {
			setGroupsLength(data);
		})

		RoleCtlr.get_rsc_col_lth().then( data => {
			setRolesLength(data)
		})
		PositionCtlr.get_rsc_col_lth().then(data => {
			setPositionsLength(data)
		})
	}, []);
	return (
		<div className="home-page page">
            <div className="overview-container">
                <div className="box">
                    <h2>Total forms</h2>
					<p>{forms_length && forms_length}</p>
					<Link to='/forms'>View Details</Link>
                </div>
                {is_admin && <div className="box">
					<h2>Total instances</h2>
					<p>{instances_length && instances_length}</p>
					<Link to='/instances'>View Details</Link>
                </div>}
                <div className="box">
                    <h2>Total groups</h2>
					<p>{groups_length && groups_length}</p>
					<Link to='/groups'>View Details</Link>
                </div>
                <div className="box">
                    <h2>Total roles</h2>
					<p>{roles_length && roles_length}</p>
					<Link to='/roles'>View Details</Link>
                </div>
				<div className="box">
                    <h2>Total positions</h2>
					<p>{positions_length && positions_length}</p>
					<Link to='/positions'>View Details</Link>
                </div>
            </div>
		</div>
	);
};

export default HomePage;
