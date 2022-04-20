import { UpdateIcon, InitInstanceIcon, OptionIcon, ReadIcon } from '../../components/icon';
import { useReadFormPage } from '../../custom_hooks';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState, useContext } from 'react';
import { UserContext } from '../../App';

import "./main.css"
import { useReadPhasesTransitions } from '../../custom_hooks/useReadPhasesTransitions';
import { useController } from '../../controllers';

const ReadFormPage = () => {
	const {user_data, held_positions} = useContext(UserContext);
	const { id: form_id } = useParams();
    const {FormCtlr} = useController();
    const [full_form, setFullForm] = useState()

    useEffect(() => {
        FormCtlr.get_rel_rsc(form_id, 'full_form').then(data => {
            console.log(data);
            setFullForm(data)
        })
    }, [])
    

	const navigate = useNavigate();

	return (
		<div className="read-form-page">
			<div className="form">
				<div className="manage-buttons">
					<button className="option-button"><OptionIcon/></button>
					<div className="context-menu">
						{/* {held_positions && full_form['phases'] && held_positions.find(hp => {
							let begin_phase = full_form['phases'].find(p => p.phase_type == 'begin')
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
							</div>} */}
					</div>
				</div>

				{full_form && (
                    <h1 className="name">{full_form.name}</h1>
				)}

				<div className="phases">
					{full_form && full_form['phases'].map((phase_data) => {
                        return (
                            <div key={phase_data.id}>
                                <div className="phase" >
                                    {/* <h3 className="phase-name">
                                        {phase_data.name
                                            ? phase_data.name
                                            : 'Phase'} - { positions_data && positions_data.find(pd => pd.id == phase_data.position_id)?.name}
                                    </h3> */}

                                    <div className="sections">
                                        {phase_data['sections'].map((section_data) => {
                                                    return (
                                                        <div className="section" key={section_data.id}>
                                                            <h3 className="section-name">{section_data.name? section_data.name: 'Section Name'}</h3>
                                                            <div className="fields">
                                                                {section_data['fields'].map(field_data => {
                                                                    return (
                                                                        <div className="field" key={field_data.id}>
                                                                            <p className='field-name'>
                                                                                {field_data.name? field_data.name: 'Field Name'}
                                                                            </p>
                                                                        </div>
                                                                    );
                                                                })}
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                    </div>
                                </div>
                                <hr />
                            </div>
                        );
                    })}
				</div>

				<div className="modal">
				</div>
			</div>
		</div>
	);
};

export default ReadFormPage;
