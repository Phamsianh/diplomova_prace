import Tab from '../../components/tab/tab';
import { useState, useEffect } from 'react';
import { useController } from '../../controllers';

const HomePage = () => {
	const [forms, setForms] = useState(null);
	const [instances, setInstances] = useState(null);
	const [created_forms, setCreatedForms] = useState(null);
	const [created_instances, setCreatedInstances] = useState(null);
	const [participated_instances, setParticipatedInstances] = useState(null);
	const [potential_instances, setPotentialInstances] = useState(null);

	const { FormCtlr, InstanceCtlr, UserCtlr } = useController();

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
			<Tab
				name="My created forms"
				overview_data={created_forms}
				title="Form"
				rsc_name="forms"
			></Tab>
			{created_instances && <Tab
				name="My created instances"
				overview_data={created_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>}
			<Tab
				name="Participated instances"
				overview_data={participated_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>
			<Tab
				name="Potential instances"
				overview_data={potential_instances}
				title="Instance"
				rsc_name="instances"
			></Tab>
		</div>
	);
};

export default HomePage;
