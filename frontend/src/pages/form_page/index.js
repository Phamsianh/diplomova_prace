import Tab from '../../components/tab/tab';
import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
const FormIndex = () => {
	const [form_overview_data, setFormOverviewData] = useState(null);
	const {FormCtlr} = useController();
	
	useEffect(() => {
		FormCtlr.get_rsc_col().then((data) => {
			setFormOverviewData(data);
		});
	}, []);
	return (
		<div className="form-index">
			<Tab
				name="All forms"
				overview_data={form_overview_data}
				title="Form"
				rsc_name="forms"
			></Tab>
		</div>
	);
};

export default FormIndex;
