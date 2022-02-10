import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';
import { displayPhasesTransitions } from '../utils/cy';

export function useReadPhasesTransitions() {
	const [instance_data, setInstanceData] = useState();
	const [phases_data, setPhasesData] = useState();
	const [transitions_data, setTransitionsData] = useState();
	const [sections_data, setSectionsData] = useState();
	const [positions_data, setPositionsData] = useState();
	const [directors_data, setDirectorsData] = useState();
	const [receivers_data, setReceiversData] = useState();
	const [participants_data, setParticipantsData] = useState();
	const [reading, setReading] = useState(false);

	const [read_phases_transitions_component, setReadPhasesTransitionsComponent] = useState();

	useEffect(() => {
		if(reading){
			setReadPhasesTransitionsComponent(
				<ReadPhasesTransitions 
				instance_data={instance_data}
				phases_data={phases_data} 
				transitions_data={transitions_data} 
				sections_data={sections_data}
				positions_data={positions_data}
				directors={directors_data}
				receivers={receivers_data}
				participants={participants_data}
				cancelReading={cancelReading} />
			)
		}
		else{
			setReadPhasesTransitionsComponent(null);
		}
	},[reading])

	function setReadPhasesTransitions(
		instance_data,
		phases_data, 
		transitions_data,
		sections_data,
		positions_data,
		directors,
		receivers, 
		participants) {
		setReading(true)
		setInstanceData(instance_data)
		setPhasesData(phases_data)
		setTransitionsData(transitions_data)
		setSectionsData(sections_data)
		setPositionsData(positions_data)
		console.log('positions', positions_data);
		setDirectorsData(directors)
		setReceiversData(receivers)
		setParticipantsData(participants)
	}

	function cancelReading(e) {
		e.preventDefault();
		setReading(false);
	}

	return {read_phases_transitions_component, setReadPhasesTransitions, reading};
}


const ReadPhasesTransitions = ({
	instance_data, 
	phases_data, 
	transitions_data, 
	sections_data,
	positions_data, 
	directors,
	receivers,
	participants,
	cancelReading}) => {

	const [cy, setCy] = useState();
	const [phs_data, setPhsData] = useState();
	

	useEffect(() => {
		setCy(displayPhasesTransitions('cy', phases_data, transitions_data, instance_data));
		let phs_d = phases_data.map(pd => {
			let position = positions_data.find(position => position.id == pd.position_id)
			let sections = sections_data.filter(sd => sd.phase_id == pd.id);
			let transitions = transitions_data.filter(td => td.from_phase_id == pd.id);
			let director = participants.find(
				participant => participant.id == directors.find(d => d.phase_id == pd.id)?.user_id
				);
			sections = sections.map(s => {
				s.receiver = participants.find(
					participant => participant.id == receivers.find(r => r.section_id == s.id)?.user_id
					);
				s.position = positions_data.find(position => position.id == s.position_id)
				return s
			})
			pd.position = position
			pd.director = director
			pd.sections = sections
			pd.transitions = transitions
			return pd
		})
		console.log('whole phases data', phs_d);
		setPhsData(phs_d);
	}, [])
	
	return (
		<div className='read-phases-transitions'>
			<div className="manage-buttons">
				<button onClick={(e) => {
					cancelReading(e);
					cy.destroy();
				}}><CancelIcon/></button>
			</div>

			<h3 className="action">{'Phases & Transitions'}</h3>

			<div id="cy">

			</div>
			<div className="phases">
				{phs_data && phs_data.map(pd => {
					return (
						<div className='phase' key={pd.id}>
							<h3 className='phase-name'>{pd.name}</h3>
							<p>Designated for: {pd.position.name}</p>
							{pd.director && <p>Current director: {`${pd.director.first_name} ${pd.director.last_name}`}</p>}
							<p>Phase type: {pd.phase_type}</p>
							<p>Order: {pd.order}</p>
							<p>Description: {pd.description}</p>
							
							<div className="sections">
								<h3 className="sections-title">Sections</h3>
								{pd.sections.map(s => {
									return (
										<div className="section" key={s.id}>
											<h3 className='section-name'>{s.name}</h3>
											<p>Assigned for: {s.position.name}</p>
											{s.receiver && <p>Current receiver: {`${s.receiver.first_name} ${s.receiver.last_name}`}</p>}
										</div>
									)
								})}
							</div>

							<div className="transitions">
								<h3 className="transitions-title">Transitions</h3>
								{pd.transitions.map(t => {
									return (
										<div className="transition" key={t.id}>
											<h3 className="transition-name">{t.name}</h3>
											<p>To: {phases_data.find(p => p.id == t.to_phase_id)?.name}</p>
										</div>
									)
								})}
							</div>
							<hr />
						</div>
					)
				})}
			</div>
		</div>
	)
}
