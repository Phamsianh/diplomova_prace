import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import Tab from '../../components/tab/tab';

export const MyFormsPage = () => {
    const [forms_data, setFormsData] = useState(null);
	const {UserCtlr} = useController();
	
	useEffect(() => {
		UserCtlr.get_rel_rsc('me', 'created_forms').then((data) => {
			console.log('created forms data', data);
			setFormsData(data);
		});
	}, []);

    return (
        <div className='my-forms-page page'>
            {forms_data && 
				<Tab
					name="My forms"
					overview_data={forms_data}
					title="Form"
					rsc_name="forms"
				></Tab>}
        </div>
    )
};
