import { useState, useEffect } from 'react';
import { PhaseCtlr, SectionCtlr } from '../../controllers';
import { SectionFieldsEditor } from '../section/section_fields_editor';
import ReadPhase from './read_phase';
import ReadSection from '../section/read_section';
import CreateSection from '../section/create_section';
import UpdateSection from '../section/update_section';
import { UpdateIcon, DeleteIcon, CancelIcon, CreateIcon } from '../icon';

export const PhaseSectionsEditor = ({
	phase_data,
	handleDeletePhase,
	handleUpdatePhase,
	cancelUpdatePhase,
}) => {
	const [sections_data, setSectionsData] = useState([]);
	const [toggle_section_creator, setToggleSectionCreator] = useState(false);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);
	const [current_phase_data, setCurrentPhaseData] = useState(phase_data);
	const [phase_component, setPhaseComponent] = useState(
		<ReadPhase phase_data={phase_data} />
	);

	useEffect(() => {
		PhaseCtlr.get_rel_rsc(phase_data.id, 'sections').then((data) => {
			setSectionsData(data);
			console.log('sectiondata', data);
		});
	}, []);

	const handleSubmit = (e) => {
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
		setToggleUpdateButton
	) => {
		setSectionComponent(
			<UpdateSection
				old_section_data={current_section_data}
				handleSubmit={(e) =>
					updateSection(
						e,
						current_section_data.id,
						setSectionComponent,
						setCurrentSectionData,
						setToggleUpdateButton
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
		setToggleUpdateButton
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
		setToggleUpdateButton(true);
	};
	const cancelUpdateSection = (current_section_data, setSectionComponent) => {
		setSectionComponent(
			<ReadSection section_data={current_section_data} />
		);
	};

	return (
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

			<div className="sections">
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
					<CreateSection handleCreate={handleSubmit} cancelCreate={disableSectionCreator} />
				)}
				{toggle_section_creator ? (
					''
				) : (
					<button onClick={enableSectionCreator} title='New Section'><CreateIcon/></button>
				)}
				{/* {toggle_section_creator && (
					<button onClick={disableSectionCreator}><CancelIcon/></button>
				)} */}
			</div>
		</div>
	);
};
