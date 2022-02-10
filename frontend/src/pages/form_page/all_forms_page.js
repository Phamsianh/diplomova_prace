import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import Tab from '../../components/tab/tab';

const AllFormsPage = () => {
	const [forms_data, setFormsData] = useState(null);
	const {FormCtlr} = useController();
	
	useEffect(() => {
		FormCtlr.get_rsc_col().then((data) => {
			console.log('forms data', data);
			setFormsData(data);
		});
	}, []);
	return (
		<div className="forms">
				{forms_data && 
				<Tab
					name="All forms"
					overview_data={forms_data}
					title="Form"
					rsc_name="forms"
				></Tab>}
		</div>
	);
};

export default AllFormsPage;
