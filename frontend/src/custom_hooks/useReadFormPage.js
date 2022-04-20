import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useController } from '../controllers';

export const useReadFormPage = () => {
	const { id: form_id } = useParams();
	const [form_data, setFormData] = useState();
	const [phases_data, setPhasesData] = useState();
	const [transitions_data, setTransitionsData] = useState();
	const [sections_data, setSectionsData] = useState();
	const [fields_data, setFieldsData] = useState();
	const [positions_data, setPositionsData] = useState();
	const { FormCtlr, InstanceCtlr } = useController();
	const navigate = useNavigate();

	useEffect(() => {
		FormCtlr.get_rsc_ins(form_id).then((data) => {
			// console.log('form data', data);
			setFormData(data);
		});
		FormCtlr.get_rel_rsc(form_id, 'phases').then((data) => {
			// console.log('phases data', data);
			setPhasesData(data);
		});
		FormCtlr.get_rel_rsc(form_id, 'transitions').then((data) => {
			// console.log('transitions data', data);
			setTransitionsData(data);
		});
		FormCtlr.get_rel_rsc(form_id, 'sections').then((data) => {
			// console.log('sections data', data);
			setSectionsData(data);
		});
		FormCtlr.get_rel_rsc(form_id, 'fields').then((data) => {
			// console.log('fields data', data);
			setFieldsData(data);
		});
		FormCtlr.get_rel_rsc(form_id, 'positions').then((data) => {
			// console.log('positions data', data);
			setPositionsData(data);
		});
	}, []);

	useEffect(() => {
		if (!phases_data) return
		setPhasesData(phases_data.sort((a, b) => a.order - b.order))
		// console.log('sorted phases data', phases_data);
	}, [phases_data])

	useEffect(() => {
		if (!sections_data) return
		setSectionsData(sections_data.sort((a, b) => a.order - b.order))
		// console.log('sorted sections data', sections_data);
	}, [sections_data])

	useEffect(() => {
		if (!fields_data) return
		setFieldsData(fields_data.sort((a, b) => a.order - b.order))
		// console.log('sorted fields data', fields_data);
	}, [fields_data])

	function initInstance() {
		const req_body = {
			form_id: form_data.id,
		};
		InstanceCtlr.post_rsc(req_body).then((data) => {
			navigate(`/instances/${data.id}`);
		});
	}

	return {
		form_data,
		initInstance,
		form_id,
		phases_data,
		transitions_data,
		sections_data,
		fields_data,
		positions_data
	};
};
