import { UpdateIcon, InitInstanceIcon, OptionIcon, ReadIcon } from '../../components/icon';
import { useReadFormPage } from '../../custom_hooks';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState, useContext } from 'react';
import { UserContext } from '../../App';

import "./main.css"
import { useReadPhasesTransitions } from '../../custom_hooks/useReadPhasesTransitions';

const ReadFormPage = () => {
	const {user_data, held_positions} = useContext(UserContext);

	const {
		form_data,
		initInstance,
		form_id,
		phases_data,
		transitions_data,
		sections_data,
		fields_data,
		positions_data
	} = useReadFormPage();

	const {read_phases_transitions_component, setReadPhasesTransitions, reading: reading_p_t} = useReadPhasesTransitions();

	useEffect(() => {
		if(reading_p_t ) {
			document.querySelector(".modal").classList.add("show-modal");
		}
		else {
			document.querySelector(".modal")?.classList.remove("show-modal");
		}
	}, [reading_p_t])


	const navigate = useNavigate();

	return (
		<div className="read-form-page">
			<div className="form">
				<div className="manage-buttons">
					<button className="option-button"><OptionIcon/></button>
					<div className="context-menu">
						{held_positions && phases_data && held_positions.find(hp => {
							let begin_phase = phases_data.find(p => p.phase_type == 'begin')
							return hp.id == begin_phase.position_id ? true : false
						}) &&
						<div className="option" onClick={initInstance}>
							<button title="Init Instance">
								<InitInstanceIcon />
							</button>
							<span>Initialize instance</span>
						</div>}
						{user_data && form_data && form_data.creator_id == user_data.id &&
						<div className="option" onClick={() => {navigate(`/forms/${form_id}/update`)}} title="Update Form">
							<button><UpdateIcon /></button>
							<span>Update Form</span>
						</div>}
						{phases_data && transitions_data && sections_data && positions_data &&
							<div className="option" onClick={() => setReadPhasesTransitions(
								{},
								phases_data, 
								transitions_data,
								sections_data,
								positions_data,
								[],
								[], 
								[])}>
								<button ><ReadIcon/></button>
								<span>{"Phases & transitions"}</span>
							</div>}
					</div>
				</div>

				{form_data && (
                    <h1 className="name">{form_data.name}</h1>
				)}

				<div className="phases">
					{phases_data &&
						phases_data.map((phase_data) => {
							return (
								<div key={phase_data.id}>
									<div className="phase" >
										{/* <h3 className="phase-name">
											{phase_data.name
												? phase_data.name
												: 'Phase'} - { positions_data && positions_data.find(pd => pd.id == phase_data.position_id)?.name}
										</h3> */}

										<div className="sections">
											{sections_data &&
												sections_data
													.filter(
														(sd) =>
															sd.phase_id ==
															phase_data.id
													)
													.map((section_data) => {
														return (
															<div
																className="section"
																key={
																	section_data.id
																}
															>
																<h3 className="section-name">
																	{section_data.name
																		? section_data.name
																		: 'Section Name'} - { positions_data && positions_data.find(pd => pd.id == section_data.position_id)?.name}
																</h3>

																<div className="fields">
																	{fields_data &&
																		fields_data
																			.filter(
																				(
																					fd
																				) =>
																					fd.section_id ==
																					section_data.id
																			)
																			.map(
																				(
																					field_data
																				) => {
																					return (
																						<div
																							className="field"
																							key={
																								field_data.id
																							}
																						>
																							<p className='field-name'>
																								{field_data.name
																									? field_data.name
																									: 'Field Name'}
																							</p>
																						</div>
																					);
																				}
																			)}
																</div>
															</div>
														);
													})}
										</div>

										{/* <div className="transitions">
											<h3 className='transitions-title'>Transitions</h3>
											{transitions_data && transitions_data.filter(td => td.from_phase_id == phase_data.id).map(transition_data => {
												return <div className="transition" key={transition_data.id}>
													<h3 className="transition-name">
														{transition_data.name}
													</h3>
													<p className="to-phase">
														To: {phases_data.find(pd => pd.id == transition_data.to_phase_id).name}
													</p>
												</div>
											})}
										</div> */}
									</div>
									<hr />
								</div>
							);
						})}
				</div>

				<div className="modal">
					{read_phases_transitions_component}
				</div>
			</div>
		</div>
	);
};

export default ReadFormPage;
