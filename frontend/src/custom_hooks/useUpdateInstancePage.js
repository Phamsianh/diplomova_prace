import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext } from '../App';
import { useController } from '../controllers';

export const useUpdateInstancePage = () => {
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
    const [participated_users, setParticipatedUsers] = useState();

    const [all_potential_directors, setAllPotentialDirectors] = useState();
    const [all_potential_receivers, setAllPotentialReceivers] = useState();

    const [can_receive, setCanReceive] = useState();
    const [can_transit, setCanTransit] = useState();
    const [can_mark_done, setCanMarkDone] = useState();

    const [is_done, setIsDone] = useState();

    const {user_data} = useContext(UserContext);

	
    const { FormCtlr, InstanceCtlr, PositionCtlr, PhaseCtlr, SectionCtlr } = useController();

    useEffect(() => {
        InstanceCtlr.get_rsc_ins(instance_id).then(data => {
            // console.log('instance data', data);;
            setInstanceData(data);

            FormCtlr.get_rsc_ins(data.form_id).then((data) => {
                // console.log('form data', data);
                setFormData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'phases').then((data) => {
                // console.log('phases data', data);
                setPhasesData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'transitions').then((data) => {
                // console.log('transitions data', data);
                setTransitionsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'sections').then((data) => {
                // console.log('sections data', data);
                setSectionsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'fields').then((data) => {
                // console.log('fields data', data);
                setFieldsData(data);
            });
            FormCtlr.get_rel_rsc(data.form_id, 'positions').then((data) => {
                // console.log('positions data', data);
                setPositionsData(data);
            });
        })
        InstanceCtlr.get_rel_rsc(instance_id, "instances_fields").then(data => {
            // console.log("instances fields data", data);
            setInstancesFieldsData(data);
        })
        PositionCtlr.get_rsc_col().then(data => {
            // console.log('all positions data', data);
            setAllPositionsData(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "commits").then(data => {
            // console.log("commits data", data);
            setCommits(data);
        })
    }, []);

    useEffect(() => {
        if(instance_data?.done === undefined) return;
        if (instance_data.done) setIsDone(true);
        else setIsDone(false);
    }, [instance_data?.done])

    useEffect(() => {
		if (!phases_data) return
		setPhasesData(phases_data.sort((a, b) => a.order - b.order))
		// console.log('sorted phases data', phases_data);
	}, [phases_data])

	useEffect(() => {
		if (!sections_data) return
		setSectionsData(sections_data.sort((a, b) => a.order - b.order))
		// console.log('sorted sections data', sections_data);
	}, [sections_data])
	
    useEffect(() => {
		if (!fields_data) return
		setFieldsData(fields_data.sort((a, b) => a.order - b.order))
		// console.log('sorted fields data', fields_data);
	}, [fields_data])

    useEffect(() => {
        if (!instance_data?.current_phase_id || !phases_data) return
        setCurrentPhase(phases_data.find(pd => pd.id == instance_data.current_phase_id))
    }, [instance_data?.current_phase_id, phases_data])

    useEffect(() => {
        if (!current_phase || !phases_data || !transitions_data) return
        setNextPhases(phases_data.filter(pd => {
            if (transitions_data.find(td => td.from_phase_id == current_phase.id && td.to_phase_id == pd.id)) return true
            else return false
        }))
    }, [current_phase, phases_data, transitions_data])

    useEffect(() => {
        if (!current_phase || !sections_data) return
        setCurrentSections(sections_data.filter(sd => sd.phase_id == current_phase.id))
    }, [current_phase, sections_data])

    useEffect(() => {
        if (instance_data?.updated_at === undefined) return // instance_data.updated_at may be null, so compare with undefined is a must
        InstanceCtlr.get_rel_rsc(instance_id, "receivers").then(data => {
            // console.log("receivers data", data);
            setReceivers(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "directors").then(data => {
            // console.log("directors data", data);
            setDirectors(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "current_director").then(data => {
            // console.log("current director data", data);
            setCurrentDirector(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "commits").then(data => {
            // console.log("commits data", data);
            setCommits(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "participated_users").then(data => {
            // console.log("participated users data", data);
            setParticipatedUsers(data);
        })
    }, [instance_data?.updated_at])

    useEffect(() => {
        // only update the participants and the current receivers when:
        // * the receiver is changed either because of transition of the instance or director change the receiver
        // * the receiver receives the instance (cause the change in length of instance field)
        if (!receivers || !instances_fields_data?.length) return
        InstanceCtlr.get_rel_rsc(instance_id, "participants").then(data => {
            // console.log("participants data", data);
            setParticipants(data);
        })
        InstanceCtlr.get_rel_rsc(instance_id, "current_receivers").then(data => {
            // console.log("current receivers data", data);
            setCurrentReceivers(data);
        })
    }, [receivers, instances_fields_data?.length])

    useEffect(() => {
        if (!current_director) return
        if (current_director.user_id == user_data.id){
            setCanTransit(true); 
            // console.log("can transit? ", true);
        }
        else {
            setCanTransit(false); 
            // console.log("can transit? ", false);
        }
    }, [current_director])

    useEffect(() => {
        if (!current_receivers) return
        if (current_receivers.find(cr => !cr.received && cr.user_id == user_data.id)){
            setCanReceive(true); 
            // console.log("can receive? ", true);
        }
        else {
            setCanReceive(false); 
            // console.log("can receive? ", false);
        }
    }, [current_receivers])

    useEffect(() => {
        if (!current_director || !phases_data) return
        let current_phase = phases_data.find(pd => pd.id == current_director.phase_id);
        if (current_phase.phase_type !== "end"){
            setCanMarkDone(false);
        }
        else {
            if (current_director.user_id == user_data.id){
                setCanMarkDone(true); 
                // console.log("can mark done? ", true);
            }
            else {
                setCanMarkDone(false); 
                // console.log("can mark done? ", false);
            }
        }
    }, [current_director, phases_data])

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
            // console.log("all potential directors data", apd);
            setAllPotentialDirectors(apd);
            // console.log("all potential receivers data", apr);
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
        setReceivers,
        directors,
        participants,
        participated_users,
        current_director,
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
        // all_current_potential_receivers,
    } ;
};
