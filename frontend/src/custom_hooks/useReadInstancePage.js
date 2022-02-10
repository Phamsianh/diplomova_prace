import { useState, useEffect, useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { UserContext } from '../App';
import { useController } from '../controllers';

export const useReadInstancePage = () => {
	const { id: instance_id } = useParams();
    const [instance_data, setInstanceData] = useState();
    const [instances_fields_data, setInstancesFieldsData] = useState();
	const [form_data, setFormData] = useState();
	const [phases_data, setPhasesData] = useState();
	const [transitions_data, setTransitionsData] = useState();
	const [sections_data, setSectionsData] = useState();
	const [fields_data, setFieldsData] = useState();
	const [positions_data, setPositionsData] = useState();
	const [all_positions_data, setAllPositionsData] = useState();
	const [commits, setCommits] = useState();

    const [receivers, setReceivers] = useState();
	const [directors, setDirectors] = useState();
    const [current_phase, setCurrentPhase] = useState();
    const [current_sections, setCurrentSections] = useState();
    const [next_phases, setNextPhases] = useState();
    const [current_receivers, setCurrentReceivers] = useState();
	const [current_director, setCurrentDirector] = useState();
    const [participants, setParticipants] = useState();

    const [all_potential_directors, setAllPotentialDirectors] = useState();
    const [all_potential_receivers, setAllPotentialReceivers] = useState();

    const [can_receive, setCanReceive] = useState();
    const [can_transit, setCanTransit] = useState();

    const {user_data} = useContext(UserContext);

	
    const { FormCtlr, InstanceCtlr, PositionCtlr, PhaseCtlr, SectionCtlr } = useController();

    useEffect(() => {
        InstanceCtlr.get_rsc_ins(instance_id).then(data => {
            console.log('instance data', data);;
            setInstanceData(data);

            FormCtlr.get_rsc_ins(data.form_id).then((data) => {
                console.log('form data', data);
                setFormData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'phases').then((data) => {
                console.log('phases data', data);
                setPhasesData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'transitions').then((data) => {
                console.log('transitions data', data);
                setTransitionsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'sections').then((data) => {
                console.log('sections data', data);
                setSectionsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'fields').then((data) => {
                console.log('fields data', data);
                setFieldsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'positions').then((data) => {
                console.log('positions data', data);
                setPositionsData(data);
            });
        })
        InstanceCtlr.get_rel_rsc(instance_id, "instances_fields").then(data => {
            console.log("instances fields data", data);
            setInstancesFieldsData(data);
            // setInstancesFieldsLength(data.length);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "receivers").then(data => {
            console.log("receivers data", data);
            setReceivers(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "directors").then(data => {
            console.log("directors data", data);
            setDirectors(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "participants").then(data => {
            console.log("participants data", data);
            setParticipants(data);
        })
        PositionCtlr.get_rsc_col().then(data => {
            console.log('all positions data', data);
            setAllPositionsData(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "commits").then(data => {
            console.log("commits data", data);
            setCommits(data);
        })
    }, []);

    useEffect(() => {
		if (!phases_data) return
		setPhasesData(phases_data.sort((a, b) => a.order - b.order))
		console.log('sorted phases data', phases_data);
	}, [phases_data])

	useEffect(() => {
		if (!sections_data) return
		setSectionsData(sections_data.sort((a, b) => a.order - b.order))
		console.log('sorted sections data', sections_data);
	}, [sections_data])
	
    useEffect(() => {
		if (!fields_data) return
		setFieldsData(fields_data.sort((a, b) => a.order - b.order))
		console.log('sorted fields data', fields_data);
	}, [fields_data])

    useEffect(() => {
        if (!(instance_data?.updated_at !== undefined && phases_data && transitions_data && sections_data && directors && receivers && participants)) return
        if(current_phase && instance_data.current_phase_id == current_phase.id) return

        async function updateCurrent() {
            let directors_data = directors;
            let receivers_data = receivers;
            let participants_data = participants;

            let cur_director = directors_data.find(dd => dd.phase_id == instance_data.current_phase_id);

            if (!cur_director) {
                directors_data = await InstanceCtlr.get_rel_rsc(instance_id, 'directors')
                receivers_data = await InstanceCtlr.get_rel_rsc(instance_id, 'receivers')
                participants_data = await InstanceCtlr.get_rel_rsc(instance_id, 'participants')
                console.log("directors data", directors_data);
                console.log("receivers data", receivers_data);
                console.log("participants data", participants_data);
                setDirectors(directors_data)
                setReceivers(receivers_data)
                setParticipants(participants_data)
                cur_director = directors_data.find(dd => dd.phase_id == instance_data.current_phase_id)
            }
            console.log("current director", cur_director);
            setCurrentDirector(cur_director);

            let cur_phase = null;
            let nxt_phases = [];
            for (const p of phases_data) {
                if (p.id == instance_data.current_phase_id) {cur_phase = p}

                for (const t of transitions_data) {
                    if (t.from_phase_id == instance_data.current_phase_id && t.to_phase_id == p.id){nxt_phases.push(p)}
                }
            }            
            console.log("current phase", cur_phase);
            setCurrentPhase(cur_phase);
            console.log("next phases", nxt_phases);
            setNextPhases(nxt_phases);

            let cur_sections = [];
            let cur_receivers = [];
            for (const s of sections_data) {
                if (s.phase_id == instance_data.current_phase_id) {
                    cur_sections.push(s)
                    for (const r of receivers_data) {
                        if (r.section_id == s.id) {cur_receivers.push(r)}
                    }
                }
            }
            console.log("current sections", cur_sections);
            setCurrentSections(cur_sections);
            console.log("current receivers", cur_receivers);
            setCurrentReceivers(cur_receivers);
        }
        updateCurrent();

    }, [instance_data?.updated_at, phases_data, transitions_data, sections_data, directors, receivers, participants])

    useEffect(() => {
        if (instance_data?.updated_at === undefined) return 
        InstanceCtlr.get_rel_rsc(instance_id, "commits").then(data => {
            console.log("commits data", data);
            setCommits(data);
        })
    }, [instance_data?.updated_at])

    useEffect(() => {
        if (!current_director) return
        if (current_director.user_id == user_data.id){setCanTransit(true); console.log("can transit? ", true);}
        else {setCanTransit(false); console.log("can transit? ", false);}
    }, [current_director])

    useEffect(() => {
        if (!current_receivers) return
        if (current_receivers.find(cr => !cr.received && cr.user_id == user_data.id)){setCanReceive(true); console.log("can receive? ", true);}
        else {setCanReceive(false); console.log("can receive? ", false);}
    }, [current_receivers])

    useEffect(() => {
        if (!(instance_data && phases_data && transitions_data && sections_data)) return
        async function setDirectorsReceivers() {
            const nxt_phases = phases_data.filter(pd => {
                if (transitions_data.find(td => td.from_phase_id == instance_data.current_phase_id && td.to_phase_id == pd.id)) return true
                else return false
            })
            let apd = {}
            let apr = {}
            for (const np of nxt_phases) {
                apd[np.id] = await PhaseCtlr.get_rel_rsc(np.id, 'potential_directors')

                let next_sections = sections_data.filter(sd => np.id == sd.phase_id)
                for (const ns of next_sections) {
                    apr[ns.id] = await SectionCtlr.get_rel_rsc(ns.id, 'potential_receivers')
                }
            }
            console.log("all potential directors data", apd);
            setAllPotentialDirectors(apd);
            console.log("all potential receivers data", apr);
            setAllPotentialReceivers(apr);
        }
        setDirectorsReceivers();
    }, [instance_data?.updated_at, phases_data, transitions_data, sections_data])

    return {
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
        all_positions_data,
        commits,

        receivers,
        directors,
        participants,
        current_director,
        current_phase,
        next_phases,
        current_sections,
        current_receivers,

        can_transit,
        can_receive,

        all_potential_directors,
        all_potential_receivers
    } ;
};
