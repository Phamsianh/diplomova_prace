import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import CreatePhase from '../phase/create_phase';
import UpdatePhase from '../phase/update_phase';
import ReadPhase from '../phase/read_phase';
import { ReadForm } from './read_form';
import { PhaseSectionsTransitionsEditor } from '../phase/phase_sections_transitions_editor';
import { useNavigate } from 'react-router-dom';
import {
	CancelIcon,
	CreateIcon,
	DeleteIcon,
	ReadIcon,
	UpdateIcon,
} from '../icon';
import { PhasesData } from './read_form_phases';

export const FormPhasesEditor = ({
	form_data,
	handleDeleteForm,
	handleUpdateForm,
	cancelUpdateForm,
}) => {
	const [current_form_data, setCurrentFormData] = useState(form_data);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);
	const [form_component, setFormComponent] = useState(
		<ReadForm form_data={form_data} />
	);
	const [phases_data, setPhasesData] = useState([]);
	const [toggle_phase_creator, setTogglePhaseCreator] = useState(false);
	const navigate = useNavigate();
	const {FormCtlr, PhaseCtlr} = useController()

	useEffect(() => {
		FormCtlr.get_rel_rsc(form_data.id, 'phases').then((data) => {
			console.log('phasedata', data);
			setPhasesData(data);
		});
	}, []);

	const createPhase = (e) => {
		e.preventDefault();
		const req_bod = {
			form_id: form_data.id,
			name: e.target.name.value,
			description: e.target.description.value,
			position_id: e.target.position_id.value,
			phase_type: e.target.phase_type.value,
		};
		setTogglePhaseCreator(false);
		PhaseCtlr.post_rsc(req_bod).then((data) => {
			setPhasesData(phases_data.concat(data));
		});
	};

	const enablePhaseCreator = () => {
		setTogglePhaseCreator(true);
	};
	const disablePhaseCreator = () => {
		setTogglePhaseCreator(false);
	};

	const handleDeletePhase = (phase_id) => {
		PhaseCtlr.delete_rsc_ins(phase_id).then((data) => {
			if (data === null) {
				setPhasesData(
					phases_data.filter((pd) => {
						return pd.id != phase_id;
					})
				);
			}
		});
	};

	const handleUpdatePhase = (
		current_phase_data,
		setPhaseComponent,
		setCurrentPhaseData,
		setToggleUpdateButton
	) => {
		setPhaseComponent(
			<UpdatePhase
				old_phase_data={current_phase_data}
				handleSubmit={(e) =>
					updatePhase(
						e,
						current_phase_data.id,
						setPhaseComponent,
						setCurrentPhaseData,
						setToggleUpdateButton
					)
				}
			/>
		);
	};

	const updatePhase = async (
		e,
		phase_id,
		setPhaseComponent,
		setCurrentPhaseData,
		setToggleUpdateButton
	) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
			description: e.target.description.value,
			position_id: e.target.position_id.value,
			phase_type: e.target.phase_type.value,
		};
		let data = await PhaseCtlr.patch_rsc_ins(phase_id, req_bod);
		console.log('updated phase data', data);
		setPhaseComponent(<ReadPhase phase_data={data} />);
		setCurrentPhaseData(data);
		setToggleUpdateButton(true);

		setPhasesData(phases_data.map(pd => {
			return pd.id === data.id? data : pd
		}))
	};

	const cancelUpdatePhase = (current_phase_data, setPhaseComponent) => {
		setPhaseComponent(<ReadPhase phase_data={current_phase_data} />);
	};

	return (
		<div className="form">
			<div className="manage-buttons">
				{/* Read button */}
				{toggle_update_button && (
					<button onClick={() => navigate('/forms/' + form_data.id)}>
						<ReadIcon />
					</button>
				)}
				{/* Update button */}
				{toggle_update_button && (
					<button
						onClick={() => {
							handleUpdateForm(
								current_form_data,
								setCurrentFormData,
								setFormComponent,
								setToggleUpdateButton
							);
							setToggleUpdateButton(false);
						}}
					>
						<UpdateIcon />
					</button>
				)}
				{/* Cancel Update button */}
				{toggle_update_button ? (
					''
				) : (
					<button
						onClick={() => {
							cancelUpdateForm(
								current_form_data,
								setFormComponent
							);
							setToggleUpdateButton(true);
						}}
					>
						<CancelIcon />
					</button>
				)}
				{/* Delete Button */}
				{toggle_update_button && (
					<button onClick={handleDeleteForm}>
						<DeleteIcon />
					</button>
				)}
			</div>

			{form_component}
			<PhasesData.Provider value={phases_data} >
				<div className="phases">
					{phases_data.map((pd) => {
						return (
							<PhaseSectionsTransitionsEditor
								key={pd.id}
								phase_data={pd}
								handleDeletePhase={handleDeletePhase}
								handleUpdatePhase={handleUpdatePhase}
								cancelUpdatePhase={cancelUpdatePhase}
							/>
						);
					})}
					{toggle_phase_creator && (
						<CreatePhase
							handleCreate={createPhase}
							cancelCreate={disablePhaseCreator}
						/>
					)}
					{toggle_phase_creator ? (
						''
					) : (
						<button onClick={enablePhaseCreator} title="New Phase">
							<CreateIcon />
						</button>
					)}
				</div>
			</PhasesData.Provider>
		</div>
	);
};
