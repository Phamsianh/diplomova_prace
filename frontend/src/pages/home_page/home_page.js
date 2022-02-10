import Tab from '../../components/tab/tab';
import { useState, useEffect, useContext } from 'react';
import { useController } from '../../controllers';
import { UserContext } from '../../App';

const HomePage = () => {
	const [forms, setForms] = useState(null);
	const [instances, setInstances] = useState(null);
	const [created_forms, setCreatedForms] = useState(null);
	const [created_instances, setCreatedInstances] = useState(null);
	const [participated_instances, setParticipatedInstances] = useState(null);
	const [potential_instances, setPotentialInstances] = useState(null);
	
	const {held_positions}	= useContext(UserContext);
	const [is_admin, setIsAdmin] = useState(false)

	const { FormCtlr, InstanceCtlr, UserCtlr } = useController();

	useEffect(() => {
		if (!held_positions) return
		if(held_positions.find(hp => hp.role_id == 1)) setIsAdmin(true)
		else setIsAdmin(false)
	}, [held_positions])

	useEffect(() => {
		// get all forms, instances
		FormCtlr.get_rsc_col()
			.then((data) => {
				setForms(data);
			})
			.catch((e) => console.error(e));

		// InstanceCtlr.get_rsc_col()
		// 	.then((data) => {
		// 		setInstances(data);
		// 	})
		// 	.catch((e) => console.error(e));

		//get my created forms, instances
		UserCtlr.get_rel_rsc('me', 'created_forms')
			.then((data) => {
				setCreatedForms(data);
			})
			.catch((e) => console.error(e));
		UserCtlr.get_rel_rsc('me', 'created_instances')
			.then((data) => {
				setCreatedInstances(data);
			})
			.catch((e) => console.error(e));
		UserCtlr.get_rel_rsc('me', 'participated_instances').then((data) => {
			setParticipatedInstances(data);
		});
		UserCtlr.get_rel_rsc('me', 'potential_instances').then((data) => {
			setPotentialInstances(data);
		});
	}, []);
	return (
		<div className="home-page page">
			{forms && <Tab
				name="All forms"
				overview_data={forms}
				title="Form"
				rsc_name="forms"
			></Tab>}
			{/* <Tab
				name="All instances"
				overview_data={instances}
				title="Instance"
				rsc_name="instances"
			></Tab> */}
			{created_forms?.length !== 0 && is_admin && <Tab
				name="My created forms"
				overview_data={created_forms}
				title="Form"
				rsc_name="forms"
			></Tab>}
			{created_instances?.length !== 0 && <Tab
				name="My created instances"
				overview_data={created_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>}
			{participated_instances?.length !== 0 && <Tab
				name="Participated instances"
				overview_data={participated_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>}
			{potential_instances?.length !== 0 && <Tab
				name="Potential instances"
				overview_data={potential_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>}
		</div>
	);
};

export default HomePage;
