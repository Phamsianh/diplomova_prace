import { useState, useEffect } from 'react';
import ReadPhase from './read_phase';
import { useController } from '../../controllers';

import ReadSection from '../section/read_section';
import CreateSection from '../section/create_section';
import UpdateSection from '../section/update_section';
import { SectionFieldsEditor } from '../section/section_fields_editor';

import { CreateTransition } from '../transition/create_transition';
import { ReadTransition } from '../transition/read_transition';
import { UpdateTransition } from '../transition/update_transition';
import { TransitionEditor } from '../transition/transition_editor';

import { UpdateIcon, DeleteIcon, CancelIcon, CreateIcon } from '../icon';

export const PhaseSectionsTransitionsEditor = ({
	phase_data,
	handleDeletePhase,
	handleUpdatePhase,
	cancelUpdatePhase,
}) => {
	const { PhaseCtlr, SectionCtlr, TransitionCtlr } = useController();
	
	//----------------------------EDIT PHASE LOGIC-------------------------------------
	const [phase_component, setPhaseComponent] = useState(
		<ReadPhase phase_data={phase_data} />
	);
	const [current_phase_data, setCurrentPhaseData] = useState(phase_data);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);

	//----------------------------EDIT SECTIONS LOGIC----------------------------------
	const [sections_data, setSectionsData] = useState([]);
	const [toggle_section_creator, setToggleSectionCreator] = useState(false);

	useEffect(() => {
		PhaseCtlr.get_rel_rsc(phase_data.id, 'sections').then((data) => {
			setSectionsData(data);
			console.log('sectiondata', data);
		});
	}, []);

	const handleCreateSection = (e) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
			phase_id: phase_data.id,
			position_id: e.target.position_id.value,
			order: !isNaN(e.target.order.value) ? 1 : e.target.order.value,
		};
		setToggleSectionCreator(false);
		SectionCtlr.post_rsc(req_bod).then((data) => {
			setSectionsData(sections_data.concat(data));
		});
	};

	const enableSectionCreator = () => {
		setToggleSectionCreator(true);
	};
	const disableSectionCreator = () => {
		setToggleSectionCreator(false);
	};

	const handleDeleteSection = async (section_id) => {
		let data = await SectionCtlr.delete_rsc_ins(section_id);
		if (data === null) {
			setSectionsData(
				sections_data.filter((sd) => {
					return sd.id != section_id;
				})
			);
		}
	};
	const handleUpdateSection = (
		current_section_data, // state
		setSectionComponent,
		setCurrentSectionData,
		setToggleUpdateSectionButton
	) => {
		setSectionComponent(
			<UpdateSection
				old_section_data={current_section_data}
				handleUpdateSection={(e) =>
					updateSection(
						e,
						current_section_data.id,
						setSectionComponent,
						setCurrentSectionData,
						setToggleUpdateSectionButton
					)
				}
			/>
		);
	};
	const updateSection = async (
		e,
		section_id,
		setSectionComponent,
		setCurrentSectionData,
		setToggleUpdateSectionButton
	) => {
		e.preventDefault();
		const req_body = {
			name: e.target.name.value,
			position_id: e.target.position_id.value,
			order: !isNaN(e.target.order.value) ? 1 : e.target.order.value,
		};
		let data = await SectionCtlr.patch_rsc_ins(section_id, req_body);
		console.log('updated sectiondata', data);
		setCurrentSectionData(data);
		setSectionComponent(<ReadSection section_data={data} />);
		setToggleUpdateSectionButton(true);
	};
	const cancelUpdateSection = (current_section_data, setSectionComponent) => {
		setSectionComponent(
			<ReadSection section_data={current_section_data} />
		);
	};

	//----------------------------EDIT TRANSITIONS LOGIC----------------------------------
	const [transitions_data, setTransitionsData] = useState([]);
	const [toggle_transition_creator, setToggleTransitionCreator] =
		useState(false);

	useEffect(() => {
		PhaseCtlr.get_rel_rsc(phase_data.id, 'from_transitions').then(
			(data) => {
				setTransitionsData(data);
				console.log('transitiondata', data);
			}
		);
	}, []);

	const handleCreateTransition = (e) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
			from_phase_id: phase_data.id,
			to_phase_id: e.target.to_phase_id.value,
		};
		setToggleTransitionCreator(false);
		TransitionCtlr.post_rsc(req_bod).then((data) => {
			setTransitionsData(transitions_data.concat(data));
		});
	};

	const enableTransitionCreator = () => {
		setToggleTransitionCreator(true);
	};
	const disableTransitionCreator = () => {
		setToggleTransitionCreator(false);
	};

	const handleDeleteTransition = async (transition_id) => {
		let data = await TransitionCtlr.delete_rsc_ins(transition_id);
		if (data === null) {
			setTransitionsData(
				transitions_data.filter((td) => {
					return td.id != transition_id;
				})
			);
		}
	};
	const handleUpdateTransition = (
		current_transition_data, // state
		setTransitionComponent,
		setCurrentTransitionData,
		setToggleUpdateTransitionButton
	) => {
		setTransitionComponent(
			<UpdateTransition
				old_transition_data={current_transition_data}
				handleUpdateTransition={(e) =>
					updateTransition(
						e,
						current_transition_data.id,
						setTransitionComponent,
						setCurrentTransitionData,
						setToggleUpdateTransitionButton
					)
				}
				from_phase_id={current_phase_data.id}
			/>
		);
	};
	const updateTransition = async (
		e,
		transition_id,
		setTransitionComponent,
		setCurrentTransitionData,
		setToggleUpdateTransitionButton
	) => {
		e.preventDefault();
		const req_body = {
			name: e.target.name.value,
			from_phase_id: phase_data.id,
			to_phase_id: e.target.to_phase_id.value,
		};
		let data = await TransitionCtlr.patch_rsc_ins(transition_id, req_body);
		console.log('updated transitiondata', data);
		setCurrentTransitionData(data);
		setTransitionComponent(<ReadTransition transition_data={data} />);
		setToggleUpdateTransitionButton(true);
	};
	const cancelUpdateTransition = (
		current_transition_data,
		setTransitionComponent
	) => {
		setTransitionComponent(
			<ReadTransition transition_data={current_transition_data} />
		);
	};

	return (
		//----------------------------PHASE EDITOR--------------------------------
		<div className="phase">
			<div className="manage-buttons">
				{toggle_update_button && (
					<button
						onClick={() => {
							setToggleUpdateButton(false);
							handleUpdatePhase(
								current_phase_data,
								setPhaseComponent,
								setCurrentPhaseData,
								setToggleUpdateButton
							);
						}}
					>
						<UpdateIcon />
					</button>
				)}
				{toggle_update_button ? (
					''
				) : (
					<button
						onClick={() => {
							setToggleUpdateButton(true);
							cancelUpdatePhase(
								current_phase_data,
								setPhaseComponent
							);
						}}
					>
						<CancelIcon />
					</button>
				)}
				{toggle_update_button && (
					<button onClick={() => handleDeletePhase(phase_data.id)}>
						<DeleteIcon />
					</button>
				)}
			</div>
			{phase_component}

			{/*--------------------------SECTIONS EDITOR-------------------------------*/}
			<div className="sections">
				<h2>Sections</h2>
				{sections_data.map((sd) => {
					return (
						<SectionFieldsEditor
							section_data={sd}
							key={sd.id}
							handleDeleteSection={handleDeleteSection}
							handleUpdateSection={handleUpdateSection}
							cancelUpdateSection={cancelUpdateSection}
						/>
					);
				})}
				{toggle_section_creator && (
					<CreateSection
						handleCreate={handleCreateSection}
						cancelCreate={disableSectionCreator}
					/>
				)}
				{toggle_section_creator ? (
					''
				) : (
					<button onClick={enableSectionCreator} title="New Section">
						<CreateIcon />
					</button>
				)}
			</div>

			{/*---------------------------TRANSITIONS EDITOR---------------------------*/}
			<div className="transitions">
				<h2>Transitions</h2>
				{transitions_data.map((td) => {
					return (
						<TransitionEditor
							transition_data={td}
							key={td.id}
							handleDeleteTransition={handleDeleteTransition}
							handleUpdateTransition={handleUpdateTransition}
							cancelUpdateTransition={cancelUpdateTransition}
							// from_phase_id={current_phase_data.id}
						/>
					);
				})}
				{toggle_transition_creator && (
					<CreateTransition
						handleCreate={handleCreateTransition}
						cancelCreate={disableTransitionCreator}
						from_phase_id={current_phase_data.id}
					/>
				)}
				{toggle_transition_creator ? (
					''
				) : (
					<button
						onClick={enableTransitionCreator}
						title="New Transition"
					>
						<CreateIcon />
					</button>
				)}
			</div>
		</div>
	);
};
