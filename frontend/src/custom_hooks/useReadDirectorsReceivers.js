import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';
import { displayPhasesTransitions } from '../utils/cy';

export function useReadDirectorsReceivers() {
	const [instance_data, setInstanceData] = useState();
	const [phases_data, setPhasesData] = useState();
	const [transitions_data, setTransitionsData] = useState();
	const [sections_data, setSectionsData] = useState();
	const [positions_data, setPositionsData] = useState();
	const [directors_data, setDirectorsData] = useState();
	const [receivers_data, setReceiversData] = useState();
	const [participants_data, setParticipantsData] = useState();
	const [reading, setReading] = useState(false);

	const [read_directors_receivers_component, setReadDirectorsReceiversComponent] = useState();

	useEffect(() => {
		if(reading){
			setReadDirectorsReceiversComponent(
				<ReadDirectorsReceivers 
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
			setReadDirectorsReceiversComponent(null);
		}
	},[reading])

	function setReadDirectorsReceivers(
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
		setDirectorsData(directors)
		setReceiversData(receivers)
		console.log('participants', participants);
		setParticipantsData(participants)
	}

	function cancelReading(e) {
		e.preventDefault();
		setReading(false);
	}

	return {read_directors_receivers_component, setReadDirectorsReceivers, reading};
}


const ReadDirectorsReceivers = ({
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
			let sections = sections_data.filter(sd => sd.phase_id == pd.id);
			let director = participants.find(
				participant => participant.id == directors.find(d => d.phase_id == pd.id)?.user_id
				);
			sections = sections.map(s => {
				s.receiver = participants.find(
					participant => participant.id == receivers.find(r => r.section_id == s.id)?.user_id
					);
				return s
			})
			pd.director = director
			pd.sections = sections
			return pd
		})
		console.log('whole phases data', phs_d);
		setPhsData(phs_d);
	}, [])
	
	return (
		<div className='read-directors-receivers'>
			<div className="manage-buttons">
				<button onClick={(e) => {
					cancelReading(e);
					cy.destroy();
				}}><CancelIcon/></button>
			</div>

			<h3 className="action">{'Directors & Receivers'}</h3>

			<div id="cy">

			</div>

            <table>
                <thead>
                    <tr>
                        <th>Phase name</th>
                        <th>Director</th>
                        <th>Sections name</th>
                        <th>Receivers</th>
                    </tr>
                </thead>
                {phs_data && phs_data.map((pd) => {
                    return (
                        <tbody key={pd.id}>
                            <tr>
                                <td rowSpan={pd.sections.length}>{pd.name}</td>
                                <td rowSpan={pd.sections.length}>{pd.director ? `${pd.director.first_name} ${pd.director.last_name}` : ''}</td>
                                <td>{pd.sections[0].name}</td>
                                <td>{pd.sections[0].receiver? `${pd.sections[0].receiver.first_name} ${pd.sections[0].receiver.last_name}` : ''}</td>
                                
                            </tr>
                            {pd.sections.filter((s ,i) => i != 0).map(s => {
                                return ( 
                                <tr key={s.id}>
                                    <td>{s.name}</td>
                                    <td>{s.receiver? `${s.receiver.first_name} ${s.receiver.last_name}` : ''}</td>
                                </tr>)
                            })}
                        </tbody>
                    )
                })}
            </table>
        </div>
	)
}
