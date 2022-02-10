import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import Tab from '../../components/tab/tab';

export const MyPendingInstancesPage = () => {
    const [instances_data, setInstancesData] = useState(null);
	const {UserCtlr} = useController();
	
	useEffect(() => {
		UserCtlr.get_rel_rsc('me', 'pending_instances').then((data) => {
			console.log('pending instances data', data);
			setInstancesData(data);
		});
	}, []);

    return (
        <div className='my-pending-instances-page page'>
            {instances_data ? 
				<Tab
					name="Pending instances"
					overview_data={instances_data}
					title="Instance"
					rsc_name="instances"
				></Tab>
            : 'No pending instances'}
        </div>
    )
};
