import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import Tab from '../../components/tab/tab';

export const MyInstancesPage = () => {
    const [instances_data, setInstancesData] = useState(null);
	const {UserCtlr} = useController();
	
	useEffect(() => {
		UserCtlr.get_rel_rsc('me', 'created_instances').then((data) => {
			console.log('created instances data', data);
			setInstancesData(data);
		});
	}, []);

    return (
        <div className='my-instances-page page'>
            {instances_data && 
				<Tab
					name="My created instances"
					overview_data={instances_data}
					title="Instance"
					rsc_name="instances"
				></Tab>}
        </div>
    )
};
