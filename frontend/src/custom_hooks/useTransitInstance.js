import { useState, useEffect } from 'react';
import { CancelIcon, TransitInstanceIcon } from '../components/icon';
import { useController } from '../controllers';
import { displayPhasesTransitions } from '../utils/cy';
import { resizeTextarea } from '../utils/resize_textarea';

export const useTransitInstance = (setInstanceData) => {
	const [transiting, setTransiting] = useState(false);
	const [ins_data, setInsData] = useState();
    const [phases_data, setPhasesData] = useState();
	const [transitions_data, setTransitionsData] = useState();
    const [sections_data, setSectionsData] = useState();
    const [current_phase, setCurrentPhase] = useState();
    const [next_phases, setNextPhases] = useState();
    const [directors, setDirectors] = useState();
    const [receivers, setReceivers] = useState();
    const [positions_data, setPositionsData] = useState();
    const [all_potential_directors, setAllPotentialDirectors] = useState();
    const [all_potential_receivers, setAllPotentialReceivers] = useState();
	const [transit_instance_component, setTransitInstanceComponent] = useState();
    const [success_component, setSuccessComponent] = useState();


    const {InstanceCtlr} = useController();

	useEffect(() => {
		if(transiting){
			setTransitInstanceComponent(
				<TransitInstance 
                instance_data={ins_data}
                phases_data={phases_data} 
                transitions_data={transitions_data} 
                sections_data={sections_data}
                positions_data={positions_data}
                current_phase={current_phase}
                next_phases={next_phases}
                directors={directors}
                receivers={receivers}
                all_potential_directors={all_potential_directors}
                all_potential_receivers={all_potential_receivers}
                handleSubmit={handleSubmit}
                cancelTransit={cancelTransit} />
			)
		}
		else{
			setTransitInstanceComponent(null);
		}
	},[transiting])

    
	useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

	function setTransitInstance(
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
        all_potential_receivers) {
            setTransiting(true)
            setInsData(instance_data)
            setPhasesData(phases_data)
            setTransitionsData(transitions_data)
            setSectionsData(sections_data)
            setPositionsData(positions_data)
            setCurrentPhase(current_phase)
            setNextPhases(next_phases)
            setDirectors(directors)
            setReceivers(receivers)
            setAllPotentialDirectors(all_potential_directors)
            setAllPotentialReceivers(all_potential_receivers)
	}

    async function handleSubmit(e) {
        e.preventDefault();
        let next_phase_id = e.target.to_phase_id.value;
        let next_phase = phases_data.find(p => p.id == next_phase_id);
        let req_bod = {}
        let next_director = directors.find(d => d.phase_id == next_phase_id)
        // let next_director_user = all_potential_directors
        // let next_receivers_users = []
        if (next_director) {
            req_bod = {
                transit:{
                    current_phase_id: next_phase_id,
                }
            }
            // next_receivers = all_potential_receivers.filter(nr => {
            //     if (sections_data.find(s => s.phase_id == next_phase_id && s.id == nr.id)) return true
            //     else return false
            // })

        }
        else {
            req_bod = {
                transit: {
                    current_phase_id: next_phase_id,
                    receivers: {},
                    director_id: e.target.director_id.value   
                }
            };
            for (const ns of sections_data.filter(sd => sd.phase_id == next_phase_id)) {
                req_bod.transit.receivers[ns.id] = e.target[`section${ns.id}`].value;
            }
        }
        req_bod.transit.message = e.target.message.value
        console.log("transit instance req_bod", req_bod);
        const data = await InstanceCtlr.patch_rsc_ins(ins_data.id, req_bod);
        setSuccessComponent(<TransitInstanceSuccess next_phase={next_phase} clearMessage={clearMessage}/>)
        setInstanceData(data);
        setTransiting(false);
    }

	function cancelTransit(e) {
		e.preventDefault();
		setTransiting(false);
	}

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

	return {transit_instance_component, setTransitInstance, transiting, success_component};
};

const TransitInstance = ({
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
    all_potential_receivers,
    handleSubmit,
    cancelTransit}) => {

    const [cy, setCy] = useState();
    const [next_phase, setNextPhase] = useState(next_phases[0]);
    const [next_sections, setNextSections] = useState();
    const [next_directors, setNextDirectors] = useState();
    const [next_receivers, setNextReceivers] = useState();
    const [disabled_specified, setDisabledSpecified] = useState(false);

    const [message, setMessage] = useState();

	useEffect(() => {
		setCy(displayPhasesTransitions('cy', phases_data, transitions_data, instance_data));
	}, [])

    useEffect(() => {
        if(!next_phase)return
        let nxt_sections = sections_data.filter(sd => next_phase.id == sd.phase_id)
        setNextSections(nxt_sections)

        // if director has been already specified for next phase, 
        //      set next director and next receivers to specified director and specified receivers
        // else set next director and next receivers to potential directors and potential receivers
        let specified_director = directors.find(d => d.phase_id == next_phase.id)
        if(specified_director) {
            let nxt_director = all_potential_directors[`${next_phase.id}`].filter(pd => pd.id == specified_director.user_id)
            console.log('next director', nxt_director);
            setNextDirectors(nxt_director)

            let nxt_receivers = {}
            for (const ns of nxt_sections) {
                let specified_receiver = receivers.find(r => r.section_id == ns.id)
                nxt_receivers[ns.id] = all_potential_receivers[`${ns.id}`].filter(pr => pr.id == specified_receiver.user_id)
            }
            console.log('next receivers', nxt_receivers);
            setNextReceivers(nxt_receivers)
            setDisabledSpecified(true)
        }
        else{
            let nxt_director = all_potential_directors[`${next_phase.id}`]
            setNextDirectors(nxt_director)
            console.log('next director', nxt_director);
            let nxt_receivers = {}
            for (const ns of nxt_sections) {
                nxt_receivers[ns.id] = all_potential_receivers[`${ns.id}`]
            }
            console.log('next receivers', nxt_receivers);
            setNextReceivers(nxt_receivers)
            setDisabledSpecified(false);
        }
    }, [next_phase])

    function handleSeclectPhase(e) {
        e.preventDefault();
        let next_phase_id = e.target.value;
        setNextPhase(next_phases.find(np => np.id == next_phase_id));
    }
	
	return (
        <div className='transit-instance'>
            <div className="manage-buttons">
                <button onClick={(e) => {
                    cy.destroy();
                    cancelTransit(e);
                }}><CancelIcon/></button>
            </div>
            
            <form onSubmit={handleSubmit}>
                <h2 className='action'>Transit Instance</h2>

                <h4 className="action">Select next phase and director</h4>
                <p><b>Current phase: {current_phase.name} - {positions_data.find(pd => pd.id == current_phase.position_id).name}</b></p>
                <label>
                    Transit to phase:
                    <select name="to_phase_id" id="to_phase_id"
                    //  className='to-phase-id' 
                     onChange={handleSeclectPhase}>
                        {next_phases && next_phases.map(np => {
                            return <option value={np.id} key={np.id}>{np.name} - {positions_data.find(pd => pd.id == np.position_id).name}</option>
                        })}
                    </select>
                </label>
            
                {next_phase && next_sections &&
                <>
                <label>
                    Select director:
                    {<select name="director_id" id="director_id" disabled={disabled_specified}>
                            {next_directors && next_directors.map(nd => {
                                return <option value={nd.id} key={nd.id}>{nd.first_name} {nd.last_name}</option>
                            })}
                    </select>}
                </label>
                <h4 className='action'>{'Select receiver(s) for section(s)'}</h4>
                {next_sections.map(nsd => {
                    return (
                        <label key={nsd.id}>
                            {nsd.name} {`(Section ID: ${nsd.id})`} - {positions_data.find(pd => pd.id == nsd.position_id).name}
                            {<select name={`section${nsd.id}`} id={`section${nsd.id}`} disabled={disabled_specified}>
                                {next_receivers && next_receivers[`${nsd.id}`].map(nr => {
                                    return <option value={nr.id} key={nr.id}>{nr.first_name} {nr.last_name}</option>
                                })}
                            </select>}
                        </label>
                    )
                })}

                <label>
                    Message
                    <textarea name="message" value={message} className='message'
                        onChange={e => {
                        setMessage(e.target.value);
                        resizeTextarea(e.target);
                    }}/>
                </label>
                <button type="submit" className='transit-instance-btn'><TransitInstanceIcon/> Transit</button>
                </>
                }
            </form>

            <div id="cy"></div>
        </div>
	)
}

function TransitInstanceSuccess({
    next_phase,
    next_director,
    next_receivers, 
    clearMessage
}) {
    return (
        <div>
            <h4>Instance is transited successfully to {next_phase.name}</h4>
            {/* <p>Next director: {next_director.first_name + " " + next_director.last_name}</p>
            <p>Next reicevers: {next_receivers.map((nr, i) => {
                if (i !== next_receivers.length) return nr.first_name + " " + nr.last_name + ", "
                else return nr.first_name + " " + nr.last_name
            })}</p> */}
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}