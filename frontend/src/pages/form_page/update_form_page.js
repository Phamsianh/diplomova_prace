import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { FormPhasesEditor } from '../../components/form/form_phases_editor';
import { UpdateForm } from '../../components/form/update_form';
import { ReadForm } from '../../components/form/read_form';
import { useController } from '../../controllers';

const UpdateFormPage = () => {
	const [current_form_data, setCurrentFormData] = useState();
	const { id: form_id } = useParams();
	const navigate = useNavigate();
	const {FormCtlr} = useController();
	
	useEffect(() => {
		FormCtlr.get_rsc_ins(form_id).then((data) => {
			setCurrentFormData(data);
		});
	}, []);

	const handleDeleteForm = async () => {
		let data = await FormCtlr.delete_rsc_ins(current_form_data.id);
		if (data === null) {
            console.log(`form ${current_form_data.id} is deleted`);
			navigate('/forms');
		}
	};

	const handleUpdateForm = (
		current_form_data,
		setCurrentFormData,
		setFormComponent,
		setToggleUpdateButton
	) => {
		setFormComponent(
			<UpdateForm
				old_form_data={current_form_data}
				handleSubmit={(e) =>
					updateForm(
						e,
						setCurrentFormData,
						setFormComponent,
						setToggleUpdateButton
					)
				}
			/>
		);
	};

	const updateForm = async (
		e,
		setCurrentFormData,
		setFormComponent,
		setToggleUpdateButton
	) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
            public: e.target.public.checked,
            obsolete: e.target.obsolete.checked
		};
		let data = await FormCtlr.patch_rsc_ins(form_id, req_bod);
		setCurrentFormData(data);
		setFormComponent(<ReadForm form_data={data} />);
		setToggleUpdateButton(true);
	};

	const cancelUpdateForm = (current_form_data, setFormComponent) => {
		setFormComponent(<ReadForm form_data={current_form_data} />);
	};
	return (
		<div className="update-form-page">
			{current_form_data && (
				<FormPhasesEditor
					form_data={current_form_data}
					handleDeleteForm={handleDeleteForm}
					handleUpdateForm={handleUpdateForm}
                    cancelUpdateForm={cancelUpdateForm}
				/>
			)}
		</div>
	);
};

export default UpdateFormPage;
