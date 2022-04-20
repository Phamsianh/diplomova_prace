import { UpdateIcon, InitInstanceIcon, CreateIcon, DeleteIcon, OptionIcon, ReadIcon, CancelIcon } from '../../components/icon';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import {useUpdateFormPage, 
	useCreatePhase, useCreateSection, useCreateField, useCreateTransition,
	useUpdateForm, useUpdatePhase, useUpdateSection, useUpdateField, useUpdateTransition,
	useDeleteForm, useDeletePhase, useDeleteSection, useDeleteField, useDeleteTransition
} from "../../custom_hooks"
import { useReadPhasesTransitions } from '../../custom_hooks/useReadPhasesTransitions';

const UpdateFormPage = () => {
  const {
		form_data,
		setFormData,
		initInstance,
		form_id,
		phases_data,
		transitions_data,
		setTransitionsData,
		sections_data,
		setSectionsData,
		fields_data,
		setFieldsData,
		positions_data,
		all_positions_data,
		setPhasesData,
	} = useUpdateFormPage();
	const navigate = useNavigate();

	const {read_phases_transitions_component, setReadPhasesTransitions, reading: reading_p_t} = useReadPhasesTransitions();

	const {update_form_component, setFormToUpdate, updating: updating_form, success_component: u_f_success_component} = useUpdateForm(setFormData);
	const {update_phase_component, setPhaseToUpdate, updating: updating_phase, success_component: u_p_success_component} = useUpdatePhase(all_positions_data, setPhasesData);
	const {update_section_component, setSectionToUpdate, updating: updating_section, success_component: u_s_success_component} = useUpdateSection(all_positions_data, setSectionsData);
	const {update_field_component, setFieldToUpdate, updating: updating_field, success_component, success_component: u_fi_success_component} = useUpdateField(setFieldsData);
	const {update_transition_component, setTransitionToUpdate, updating: updating_transition, success_component: u_t_success_component} = useUpdateTransition(setTransitionsData);

	const {create_phase_component, setCreatePhase, creating: creating_phase, success_component: c_p_success_component} = useCreatePhase(all_positions_data, setPhasesData);
	const {create_section_component, setCreateSection, creating: creating_section, success_component: c_s_success_component} = useCreateSection(all_positions_data, setSectionsData);
	const {create_field_component, setCreateField, creating: creating_field, success_component: c_f_success_component} = useCreateField(setFieldsData);
	const {create_transition_component, setTransitionToCreate, creating: creating_transition, success_component: c_t_success_component, error_component: c_t_error_component} = useCreateTransition(setTransitionsData);
	
	const {delete_form_component , setDeleteForm, deleting: deleting_form, success_component: d_f_success_component} = useDeleteForm();
	const {deletePhase, success_component: d_p_success_component} = useDeletePhase(setPhasesData);
	const {deleteSection, success_component: d_s_success_component} = useDeleteSection(setSectionsData);
	const {deleteField, success_component: d_fi_success_component} = useDeleteField(setFieldsData);
	const {deleteTransition, success_component: d_t_success_component} = useDeleteTransition(setTransitionsData);

	useEffect(() => {
		if (
			creating_phase || creating_section || creating_field || creating_transition ||
			reading_p_t ||
			updating_form || updating_phase || updating_section || updating_field || updating_transition ||
			deleting_form
			) {
			document.querySelector(".modal").classList.add("show-modal");
		}else{
			document.querySelector(".modal")?.classList.remove("show-modal");
		}

	}, [
		creating_phase, creating_section, creating_field, creating_transition,
		reading_p_t,
		updating_form, updating_phase, updating_section, updating_field, updating_transition,
		deleting_form
	])

	useEffect(() => {
		if (
			c_p_success_component || c_s_success_component || c_f_success_component || c_t_success_component ||
			u_f_success_component || u_p_success_component || u_s_success_component || u_fi_success_component || u_t_success_component ||
			d_f_success_component || d_p_success_component || d_s_success_component || d_fi_success_component || d_t_success_component
			){		
			document.querySelector(".success")?.classList.add("show-success")
		}else{
			document.querySelector(".success")?.classList.remove("show-success")
		}
	}, [
		c_p_success_component, c_s_success_component, c_f_success_component, c_t_success_component,
		u_f_success_component, u_p_success_component, u_s_success_component, u_fi_success_component, u_t_success_component,
	])

	useEffect(() => {
		if(
			c_t_error_component || 
			d_f_success_component || d_p_success_component || d_s_success_component || d_fi_success_component || d_t_success_component
			){
			document.querySelector(".error")?.classList.add("show-error")
		}else{
			document.querySelector(".error")?.classList.remove("show-error")
		}
	}, [
		c_t_error_component,
		d_f_success_component, d_p_success_component, d_s_success_component, d_fi_success_component, d_t_success_component
	])

	return (
		<div className="update-form-page">
			<div className="success">
				{c_p_success_component}
				{c_s_success_component}
				{c_f_success_component}
				{c_t_success_component}

				{u_f_success_component}
				{u_p_success_component}
				{u_s_success_component}
				{u_fi_success_component}
				{u_t_success_component}

				{/* <div>
					<h4>Phase is created successfully</h4>
					<button><CancelIcon/></button>
				</div>
				<div>
					<h4>Phase is created successfully</h4>
					<button><CancelIcon/></button>
				</div> */}
			</div>

			<div className="error">
				{c_t_error_component}

				{d_f_success_component}
				{d_p_success_component}
				{d_s_success_component}
				{d_fi_success_component}
				{d_t_success_component}
			</div>

			{form_data && <div className="form">
				<div className="manage-buttons">
					<button className="option-button"><OptionIcon/></button>
					<div className="context-menu">
						<div className="option" onClick={() => navigate(`/forms/${form_data.id}`)}>
							<button ><ReadIcon /></button>
							<span>View instance</span>
						</div>
						<div className="option" onClick={initInstance}>
							<button><InitInstanceIcon /></button>
							<span>Init instance</span>
						</div>
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
						{!form_data.obsolete && 
						<div className="option" onClick={() => setFormToUpdate(form_data)}>
							<button title="Update Form"><UpdateIcon /></button>
							<span>Update form</span>
						</div>}
						{!form_data.public && 
						<div className="option" onClick={() => setDeleteForm(form_data)} >
							<button title="Delete Form"><DeleteIcon /></button>
							<span>Delete form</span>
						</div>}
						<hr />
						{!form_data.obsolete && 
						<div className="option" onClick={()=>{setCreatePhase(form_data, phases_data)}}>
							<button><CreateIcon/></button>
							<span>Create phase</span>
						</div>}
					</div>
				</div>

				<h1 className="form-name">{form_data.name}</h1>
				<p className="form-name">
					({form_data.obsolete ? 'Obsolete' : form_data.public ? 'Public' : 'Private'})
				</p>

				<div className="phases">
				{phases_data && phases_data.map((phase_data) => {
					return (
						<div key={phase_data.id}>
							<div className="phase" >
								<div className="manage-buttons">
									<button className="option-button"><OptionIcon/></button>
									<div className="context-menu">
										{!form_data.obsolete && <div className="option" onClick={()=>{setPhaseToUpdate(phase_data, phases_data)}}>
											<button><UpdateIcon/></button>
											<span>Update Phase</span>
										</div>}
										{!form_data.public && <div className="option" onClick={() => deletePhase(phase_data, phases_data)}>
											<button><DeleteIcon/></button>
											<span>Delete Phase</span>
										</div>}
										<hr />
										{!form_data.obsolete && <div className="option" onClick={()=>{setCreateSection(phase_data, sections_data)}}>
											<button><CreateIcon/></button>
											<span>Create Section</span>
										</div>}
										<hr />
										{!form_data.obsolete && <div className="option" onClick={()=>{setTransitionToCreate(transitions_data, phase_data, phases_data)}}>
											<button><CreateIcon/></button>
											<span>Create Transition</span>
										</div>}
									</div>
								</div>

								<h3 className="phase-name">
									{phase_data.name? phase_data.name: 'Phase'} 
									- { all_positions_data && all_positions_data.find(pd => pd.id == phase_data.position_id)?.name}
								</h3>


								<div className="sections">
									<h3 className='sections-title'>Sections</h3>
									{sections_data && sections_data.filter(sd => sd.phase_id == phase_data.id).map((section_data) => {
										return (
											<div className="section" key={section_data.id}>
												<div className="manage-buttons">
													<button className="option-button" onClick={e => {
														let context_menu = e.target.nextSibling? e.target.nextSibling: e.target.closest(".option-button").nextSibling
														context_menu.classList.toggle("show-options")
													}}>
														<OptionIcon/>
													</button>
													<div className="context-menu">
														<div className="option" onClick={() => setSectionToUpdate(section_data, sections_data, phase_data)}>
															<button><UpdateIcon/></button>
															<span>Update Section</span>
														</div>
														<div className="option" onClick={() => deleteSection(section_data, sections_data)}>
															<button><DeleteIcon/></button>
															<span>Delete Section</span>
														</div>
														<hr />
														<div className="option" onClick={()=> setCreateField(section_data, fields_data)}>
															<button><CreateIcon/></button>
															<span>Create Field</span>
														</div>
													</div>
												</div>

												<h3 className="section-name">
													{section_data.name? section_data.name: 'Section Name'} 
													- { all_positions_data && all_positions_data.find(pd => pd.id == section_data.position_id)?.name}
												</h3>

												<div className="fields">
													{fields_data && fields_data.filter(fd => fd.section_id == section_data.id).map(field_data => {
														return (
															<div className="field" key={field_data.id}>
																<div className="manage-buttons">
																	<button className="option-button" onClick={e => {
																		let context_menu = e.target.nextSibling? e.target.nextSibling: e.target.closest(".option-button").nextSibling
																		context_menu.classList.toggle("show-options")
																	}}>
																		<OptionIcon/>
																	</button>
																	<div className="context-menu">
																		<div className="option" onClick={() => setFieldToUpdate(field_data, fields_data, section_data)}>
																			<button><UpdateIcon/></button>
																			<span>Update Field</span>
																		</div>
																		<div className="option" onClick={() => deleteField(field_data, fields_data)}>
																			<button><DeleteIcon/></button>
																			<span>Delete Field</span>
																		</div>
																	</div>
																</div>
																<p className='field-name'>
																	{field_data.name? field_data.name: 'Field Name'}
																</p>
															</div>
														);}
													)}
												</div>
											</div>
										);
									})}
								</div>


								<div className="transitions">
									<h3 className='transitions-title'>Transitions</h3>
									{transitions_data && transitions_data.filter(td => td.from_phase_id == phase_data.id).map(transition_data => {
										return (
										<div className="transition" key={transition_data.id}>
											<div className="manage-buttons">
												<button className="option-button" onClick={e => {
													let context_menu = e.target.nextSibling? e.target.nextSibling: e.target.closest(".option-button").nextSibling
													context_menu.classList.toggle("show-options")
												}}>
													<OptionIcon/>
												</button>
												<div className="context-menu">
													<div className="option" onClick={() => setTransitionToUpdate(transition_data, transitions_data, phase_data, phases_data)}>
														<button><UpdateIcon/></button>
														<span>Update Transition</span>
													</div>
													<div className="option" onClick={() => deleteTransition(transition_data, transitions_data)}>
														<button><DeleteIcon/></button>
														<span>Delete Transition</span>
													</div>
												</div>
											</div>
											<h3 className="transition-name" >
												{transition_data.name}
											</h3>
											<p className="to-phase">
												To: {phases_data.find(pd => pd.id == transition_data.to_phase_id).name}
											</p>
										</div>
										)
									})}
								</div>
							</div>
							<hr />
						</div>
					);
				})}
				</div>
				
				<div className="modal">
					{create_phase_component}
					{create_section_component}
					{create_field_component}
					{create_transition_component}

					{read_phases_transitions_component}

					{update_form_component}
					{update_phase_component}
					{update_section_component}
					{update_field_component}
					{update_transition_component}

					{delete_form_component}
				</div>
			</div>}

			
		</div>
	);
};

export default UpdateFormPage