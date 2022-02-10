import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';
import { displayPhasesTransitions } from '../utils/cy';
import { formatDate } from '../utils/datetime';

export const useReadPhaseDetail = () => {
    const [reading, setReading] = useState(false);
    const [read_phase_detail_component, setReadPhaseDetailComponent] =  useState();
    const [phase_data, setPhaseData] =  useState();
    const [positions_data, setAllPositionsData] = useState();
    const [phases_data, setPhasesData] = useState();
    const [sections_data, setSectionsData] = useState();
    const [fields_data, setFieldsData] = useState();
    const [transitions_data, setTransitionsData] = useState();

    function setPhaseDetailToRead(
        phase_data, 
        phases_data,
        transitions_data, 
        sections_data,
        fields_data,
        positions_data) {
        if (reading) return;
        setReading(true);
        setPhaseData(phase_data);
        setPhasesData(phases_data);
        setTransitionsData(transitions_data);
        setSectionsData(sections_data);
        setFieldsData(fields_data)
        setAllPositionsData(positions_data);
    }

    useEffect(() => {
        if (reading) {
            setReadPhaseDetailComponent(
                <ReadPhaseDetail 
                phase_data={phase_data} 
                phases_data={phases_data}
                transitions_data={transitions_data} 
                sections_data={sections_data}
                fields_data={fields_data}
                positions_data={positions_data} 
                cancelReading={cancelReading}/>
            )
        }
        else {
			setReadPhaseDetailComponent(null);
		};
    }, [reading])

    function cancelReading (e) {
		e.preventDefault();
        setReading(false);
    }

    return {read_phase_detail_component, setPhaseDetailToRead, reading};

};

const ReadPhaseDetail = ({
    phase_data, 
    phases_data, 
    transitions_data, 
    sections_data,
    fields_data,
    positions_data, 
    cancelReading
}) => {
    const [cy, setCy] = useState()
    const [phase, setPhase] = useState()
    useEffect(() => {
        setCy(displayPhasesTransitions('cy', phases_data, transitions_data, {current_phase_id: phase_data.id}))
        let ph_data = Object.assign({}, phase_data)
        ph_data.position = positions_data.find(p => p.id == ph_data.position_id)
        ph_data.sections = []
        sections_data.forEach(s => {
            if (s.phase_id == phase_data.id) {
                s.position = positions_data.find(p => p.id == s.position_id)
                s.fields = fields_data.filter(f => f.section_id == s.id)
                ph_data.sections.push(s)
            }
        })
        ph_data.next_phases = phases_data.filter(p => {
            if (transitions_data.find(t => t.from_phase_id == phase_data.id && t.to_phase_id == p.id)) return true
            else return false
        })
        ph_data.transitions = []
        transitions_data.forEach(t => {
            if (t.from_phase_id == phase_data.id){
                t.to_phase = phases_data.find(p => p.id == t.to_phase_id)
                t.next_position = positions_data.find(p => p.id == t.to_phase.position_id)
                ph_data.transitions.push(t)
            }
        })
        setPhase(ph_data)
    }, [])

    return (
        <div className="read-phase-detail">
            <div className="manage-buttons">
                <button onClick={e => {
                    cancelReading(e);
                    cy.destroy();
                }}><CancelIcon/></button>
            </div>

            <div id="cy"></div>

            {phase && <div className="phase">
                <h3 className="phase-name">{phase.name}</h3>
                <p>Phase ID: {phase.id}</p>
                <p>Created at: {formatDate(phase.created_at)}</p>
                <p>Phase type: {phase.phase_type}</p>
                <p>Designated for: {phase.position.name}</p>
                <p>Description: {phase.description}</p>

                <div className="sections">
                    <h3 className="sections-title">Sections</h3>
                    {phase.sections.map(s => {
                        return (
                            <div className="section" key={s.id}>
                                <h3 className='section-name'>{s.name}</h3>
                                <p>Assigned for: {s.position.name}</p>

                                <div className="fields">
                                    {s.fields.map(f => {
                                        return (
                                            <div className="field" key={f.id}>
                                                <b><p className="field-name">{f.name}</p></b>
                                            </div>
                                        )
                                    })}
                                </div>
                            </div>
                        )
                    })}
                </div>

                <div className="transitions">
                    <h3 className="transitions-title">Transitions</h3>
                    {phase.transitions.map(t => {
                        return (
                            <div className="transition" key={t.id}>
                                <h3 className="transition-name">{t.name}</h3>
                                <p>Next phase: {t.to_phase.name}</p>
                                <p>Phase ID: {t.to_phase.id}</p>
                                <p>Assinged for: {t.next_position.name}</p>
                            </div>
                        )
                    })}
                </div>
            </div>}

        </div>
    )
}