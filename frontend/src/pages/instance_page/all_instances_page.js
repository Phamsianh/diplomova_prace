import React from 'react';
import Tab from '../../components/tab/tab';
import { useState, useEffect } from 'react';
import { InstanceController } from '../../controllers/InstanceController';
import { UserController } from '../../controllers/UserController'

const AllInstancesPage = () => {
	const [instance_overview_data, setInstanceOverviewData] = useState(null);
	const [my_instance_overview_data, setMyInstanceOverviewData] = useState(null);
    
    useEffect(() => {
		const instance_ctlr = new InstanceController('phamsianh97');
		instance_ctlr
			.get_rsc_col()
			.then((data) => {
				setInstanceOverviewData(data);
			})
			.catch((e) => console.error(e));

        const user_ctlr = new UserController('phamsianh97')
        user_ctlr.get_rel_rsc('me', 'created_instances').then(data => {
            setMyInstanceOverviewData(data)
        })
        .catch((e) => console.error(e));
	}, []);

	return (
		<div>
			<Tab
				name="All instances"
				overview_data={instance_overview_data}
				title="Instance"
				rsc_name="instances"
			></Tab>
			<Tab
				name="My instances"
				overview_data={my_instance_overview_data}
				title="Instance"
				rsc_name="instances"
			></Tab>
		</div>
	);
};

export default AllInstancesPage;
