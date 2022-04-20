import { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { CommitsPageIcon, MarkDoneIcon, OptionIcon, ReadIcon, ReceiveInstanceIcon, TransitInstanceIcon, UpdateIcon, YesIcon } from '../../components/icon';
import { useNavigate } from 'react-router-dom';
import { useUpdateInstancePage } from '../../custom_hooks/useUpdateInstancePage';
import { UpdateInstanceField } from '../../components/instance_field/update_instance_field';
import { useReadPhasesTransitions } from '../../custom_hooks/useReadPhasesTransitions';
import { useTransitInstance } from '../../custom_hooks/useTransitInstance';
import { UserContext } from '../../App';
import { useReceiveInstance } from '../../custom_hooks/useReceiveInstance';
import { useViewCommit } from '../../custom_hooks/useViewCommit';
import { useReadDirectorsReceivers } from '../../custom_hooks/useReadDirectorsReceivers';
import { useReadPhaseDetail } from '../../custom_hooks/useReadPhaseDetail';
import { useUpdateReceiver } from '../../custom_hooks/useUpdateReceivers';
import { useMarkInstaceDone } from '../../custom_hooks/useMarkInstaceDone';


export const UpdateInstancePage = () => {
	const { id: instance_id } = useParams();
	const {user_data} = useContext(UserContext);
	
	const {
		instance_data,
        setInstanceData,
        instances_fields_data,
        setInstancesFieldsData,
        form_data,
        phases_data,
        sections_data,
        fields_data,
        transitions_data,
        positions_data,
        // all_positions_data,
		commits,

        receivers,
        setReceivers,
        directors,
		participants,
		participated_users,
        // current_director,
        current_phase,
        next_phases,
        current_sections,
        current_receivers,

        can_transit,
		can_receive,
		can_mark_done,

		is_done,

        all_potential_directors,
        all_potential_receivers,
	} = useUpdateInstancePage(user_data, instance_id);
	
	const {read_phases_transitions_component, setReadPhasesTransitions, reading: reading_p_t} = useReadPhasesTransitions();
	const {read_directors_receivers_component, setReadDirectorsReceivers, reading: reading_d_r} = useReadDirectorsReceivers();
	const {transit_instance_component, setTransitInstance, transiting: transiting_instance, success_component: t_i_success_component} = useTransitInstance(setInstanceData);
	const {receive_instance_component, setReceiveInstance, receiving: receiving_instance, success_component: r_i_success_component} = useReceiveInstance(setInstanceData, setInstancesFieldsData);
	const {
		view_commits_component, 
		setReadCommits, 
		reading: reading_commits, 
        unsetViewCommits, 
		viewing: viewing_commits
	} = useViewCommit(setInstancesFieldsData, setInstanceData);
	const {read_phase_detail_component, setPhaseDetailToRead, reading: reading_phase_detail} = useReadPhaseDetail();
	const {update_receiver_component, setReceiverToUpdate, updating: updating_r, u_r_success_component} = useUpdateReceiver(setReceivers)
	const {mark_done_component, setMarkDone, marking_done, success_component: m_d_success_component} = useMarkInstaceDone(setInstanceData);

	useEffect(() => {
		if(
			reading_p_t || reading_d_r || transiting_instance || receiving_instance || reading_commits || reading_phase_detail ||
			updating_r || marking_done
			) {
			document.querySelector(".modal").classList.add("show-modal");
		}
		else {
			document.querySelector(".modal")?.classList.remove("show-modal");
		}
	}, [
		reading_p_t, reading_d_r, transiting_instance, receiving_instance, reading_commits, reading_phase_detail,
		updating_r, marking_done
	])
	
	useEffect(() => {
		if(
			t_i_success_component || r_i_success_component || u_r_success_component || m_d_success_component
			){
			document.querySelector(".success")?.classList.add("show-success")
		}else{
			document.querySelector(".success")?.classList.remove("show-success")
		}
	}, [
		t_i_success_component, r_i_success_component,
		u_r_success_component, m_d_success_component
	])
	return (
		<div className="update-instance-page">
			<div className="success">
				{t_i_success_component}
				{r_i_success_component}
				{u_r_success_component}
				{m_d_success_component}
			</div>

			{instance_data && <div className="instance">
				<div className="form">
					<div className="manage-buttons">
						<button className="option-button"><OptionIcon/></button>
						<div className="context-menu">
							<div className="option" onClick={() => setReadCommits(
								commits, 
								instances_fields_data, 
								instance_data, 
								participants, 
								phases_data
							)}>
								<button ><CommitsPageIcon/></button>
								<span>View commits</span>
							</div>
							{viewing_commits && 
							<div className="option" onClick={() => unsetViewCommits()}>
								<button ><CommitsPageIcon/></button>
								<span>View current instance</span>
							</div>}
							{!is_done && can_transit && !viewing_commits && 
							<div className="option" onClick={() => setTransitInstance(
								instance_data, 
								phases_data, 
								transitions_data, 
								sections_data, 
								positions_data,
								current_phase,
								next_phases,
								directors,
								receivers,
								all_potential_directors,
								all_potential_receivers
								)}>
								<button ><TransitInstanceIcon/></button>
								<span>Transit instance</span>
							</div>}
							{!is_done && can_receive && !viewing_commits && 
							<div className="option" onClick={() => setReceiveInstance(
								user_data,
								instance_data,
								current_sections,
								current_receivers,
								positions_data
								)}>
								<button><ReceiveInstanceIcon/></button>
								<span>Receive Instance</span>
							</div>}
							{can_mark_done && !viewing_commits && !is_done && 
							<div className="option" onClick={() => setMarkDone(instance_data)}>
								<button><MarkDoneIcon/></button>
								<span>Mark instance as done</span>
							</div>}
							<div className="option" onClick={() => setReadPhasesTransitions(
								instance_data,
								phases_data, 
								transitions_data,
								sections_data,
								positions_data,
								directors,
								receivers, 
								participants
								)}>
								<button ><ReadIcon/></button>
								<span>{"Phases & transitions"}</span>
							</div>
							<div className="option" onClick={() => setReadDirectorsReceivers(
								instance_data,
								phases_data, 
								transitions_data,
								sections_data,
								positions_data,
								directors,
								receivers, 
								participants
								)}>
								<button ><ReadIcon/></button>
								<span>{"Director & Receiver"}</span>
							</div>
							{!is_done && can_transit  && 
							<div className="option" onClick={() => setReceiverToUpdate(
								instance_data,
								current_receivers,
								current_sections,
								receivers,
								)}>
								<button ><UpdateIcon/></button>
								<span>{"Update Receivers"}</span>
							</div>}
						</div>
					</div>

					{instance_data && <h3 className="instance-id">
						Instance ID: {instance_data.id} &nbsp;
						{is_done? <YesIcon/> : ''}
					</h3>}

					{form_data && (
                    	<h1 className="form-name">{form_data.name}</h1>
					)}

					<div className="phases">
					{phases_data && phases_data.map((phase_data) => {
						return (
							<div key={phase_data.id}>
								<div className="phase">
									<div className={instance_data.current_phase_id == phase_data.id? "sections current-sections" : "sections"} >
										<div className="manage-buttons">
											<button className="option-button" onClick={e => {
												let context_menu = e.target.nextSibling? e.target.nextSibling: e.target.closest(".option-button").nextSibling
												context_menu.classList.toggle("show-options")
											}}>
												<OptionIcon/>
											</button>
											<div className="context-menu">
												{transitions_data && sections_data && positions_data && fields_data &&
												<div className="option" onClick={() => setPhaseDetailToRead(
													phase_data,
													phases_data,
													transitions_data,
													sections_data,
													fields_data,
													positions_data,
												)}>
													<button ><ReadIcon/></button>
													<span>Phase details</span>
												</div>}
											</div>
										</div>

										{sections_data && current_receivers && sections_data.filter(sd => sd.phase_id == phase_data.id).map((section_data) => {
											let can_edit = true
											if (current_receivers.find(cr => cr.section_id == section_data.id && cr.user_id == user_data.id)) {can_edit = false} // editable
											return (
												<div className="section" key={section_data.id}>
													<h3 className="section-name">
														{section_data.name? section_data.name: 'Section Name'} 
														- { positions_data && positions_data.find(pd => pd.id == section_data.position_id)?.name}
													</h3>

													<div className="fields">
														{fields_data && instances_fields_data && participated_users && fields_data.filter(fd => fd.section_id == section_data.id).map(field_data => {
															const instance_field = instances_fields_data.find(ifd => ifd.field_id == field_data.id);
															const creator = instance_field? participated_users.find(pu => pu.id == instance_field.creator_id): null;
															return (
															<div className="field" key={field_data.id} title={creator? `Editor: ${creator.first_name} ${creator.last_name}`: ''}>
																<p className='field-name'>
																	{field_data.name? field_data.name: 'Field Name'}
																</p>
																{instance_field && <UpdateInstanceField 
																	key={instance_field.id + instance_field.hash_envelope? instance_field.hash_envelope: ''}
																	readonly={is_done || can_edit || viewing_commits}
																	old_instance_field_data={instance_field} 
																	instances_fields_data={instances_fields_data} 
																	setInstancesFieldsData={setInstancesFieldsData}
																/>}
															</div>)
														})}
													</div>
												</div>
											);
										})}
									</div>
								</div>
							</div>
						);
					})}
					</div>
					<div className="modal">
						{view_commits_component}
						{transit_instance_component}
						{receive_instance_component}
						{mark_done_component}
						{read_phases_transitions_component}
						{read_directors_receivers_component}
						{read_phase_detail_component}
						{update_receiver_component}
					</div>
				</div>
			</div>}
		</div>
	);
};
