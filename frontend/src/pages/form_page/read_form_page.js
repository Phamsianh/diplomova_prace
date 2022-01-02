import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ReadFormPhases } from '../../components/form/read_form_phases';
// import { ReadFormPhasesTransitions } from '../../components/form/read_form_phases_transitions';
import { UpdateIcon, InitInstanceIcon } from '../../components/icon';
import { useController } from '../../controllers';

const ReadFormPage = () => {
	const { id: form_id } = useParams();
	const [formdata, setFormdata] = useState();
	const navigate = useNavigate();
	const { FormCtlr, InstanceCtlr } = useController();

	useEffect(() => {
		FormCtlr.get_rsc_ins(form_id).then((data) => {
			console.log('form data', data);
			setFormdata(data);
		});
	}, []);

	function initInstance() {
		const req_body = {
			form_id: formdata.id,
		};
		InstanceCtlr.post_rsc(req_body).then((data) => {
			navigate(`/instances/${data.id}/update`);
		});
	}

	return (
		<div className="read-form-page">
			<div className="form">
				<div className="manage-buttons">
					{formdata && (formdata.public || formdata.obsolete) ? (
						formdata.public && !formdata.obsolete ? (
							<button
								onClick={initInstance}
								title="Init Instance"
							>
								<InitInstanceIcon />
							</button>
						) : (
							''
						)
					) : (
						<button
							onClick={() => {
								navigate(`/forms/${form_id}/update`);
							}}
							title="Update Form"
						>
							<UpdateIcon />
						</button>
					)}
				</div>

				{formdata && <ReadFormPhases form_data={formdata} />}
				{/* {formdata && <ReadFormPhasesTransitions form_data={formdata} />} */}
			</div>
		</div>
	);
};

export default ReadFormPage;
