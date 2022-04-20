import { useState, useEffect } from 'react';
import { CancelIcon, CommitIcon } from '../components/icon';
import { useController } from '../controllers';
import { formatDate } from '../utils/datetime';

export const useViewCommit = (setInstancesFieldsData, setInstanceData) => {
    const [viewing, setViewing] = useState(false);
    const [reading, setReading] = useState(false);
    const [commits_data, setCommitsData] = useState();
	const [all_envelopes, setAllEnvelopes] = useState({});
    const [current_instances_fields_data, setCurrentInstancesFieldsData] = useState(null);
    const [current_instance_data, setCurrentInstanceData] = useState(null);
    const [participants, setParticipants] = useState(null);
    const [phases_data, setPhasesData] = useState(null);
    const [view_commits_component, setViewCommitsComponent] = useState();

    const {CommitCtlr} = useController();

    useEffect(() => {
        if (reading) {
            setViewCommitsComponent(
                <ReadCommits 
                commits_data={commits_data}
                participants={participants} 
                phases_data={phases_data}
                setViewCommits={setViewCommits}
                cancelRead={cancelRead}/>
            )
        }
        else {
            setViewCommitsComponent(null)
        }
    }, [reading])

    function setReadCommits(commits_data, instances_fields_data, instance_data, participants, phases_data){
        setReading(true);
        setCommitsData(commits_data);
        // when user view a commit, we must store current instance and current instances fields data.
        // only store these data if it's null.
        // when unsetViewCommits() is called, set the instance and instances_fields to these data.
        if (!current_instances_fields_data) setCurrentInstancesFieldsData(instances_fields_data);
        if (!current_instance_data) setCurrentInstanceData(instance_data)
        setParticipants(participants)
        setPhasesData(phases_data)
    }

    function cancelRead(e) {
        e.preventDefault();
        setReading(false);
    }

    async function setViewCommits(commit_data) {
        let converted_instances_fields_data

        // store the envelopes data in variable all_envelopes as an object with (key, value) = (hash_commit, array of envelopes).
        // if the key does not exist in all_envelopes, get envelopes from API and set the instances_fields to the converted envelopes.
        // if the key exists, set the existed converted envelopes in all_envelopes to the instances_fields.
        if (!all_envelopes[commit_data.hash_commit]) {
            let data = await CommitCtlr.get_rel_rsc(commit_data.hash_commit, 'envelopes');
            // console.log('envelopes data', data);
            converted_instances_fields_data = CommitCtlr.convertEnvelopeToContent(data, current_instances_fields_data);
            // console.log('converted instances fields', converted_instances_fields_data);
            all_envelopes[commit_data.hash_commit] = converted_instances_fields_data
            // console.log('all envelopes data', all_envelopes);
            setAllEnvelopes(all_envelopes)
            setInstancesFieldsData(converted_instances_fields_data);
        }
        else {
            setInstancesFieldsData(all_envelopes[commit_data.hash_commit])
        }

        let ins_data = Object.assign({}, current_instance_data);
        ins_data.current_phase_id = commit_data.current_phase_id;
        // console.log("instance data view commit", ins_data);
        setInstanceData(ins_data);
        setViewing(true);
        setReading(false);
    }

    function unsetViewCommits() {
        setViewing(false);
        setInstancesFieldsData(current_instances_fields_data);
        setInstanceData(current_instance_data);
        setCurrentInstancesFieldsData(null);
        setCurrentInstanceData(null);
    }

    return {
        view_commits_component,
        setReadCommits, 
        reading, 
        unsetViewCommits, 
        viewing
    }
};


function ReadCommits({
    commits_data,
    participants,
    phases_data,
    setViewCommits,
    cancelRead
}) {
    const [participants_data, setParticipants] = useState();
    const [phs_data, setPhsData] = useState();

    useEffect(() => {
        let participants_data = {}
        for (const pu of participants) {
            participants_data[pu.id] = pu;
        }
        setParticipants(participants_data);
        let phs_data = {}
        for (const p of phases_data) {
            phs_data[p.id] = p;
        }
        setPhsData(phs_data)
    }, [])
    return (
        <div className="view-commits">
            <div className="manage-buttons">
                <button onClick={cancelRead}><CancelIcon/></button>
            </div>

            <h3 className="action">View commits history</h3>
            <table>
                <thead>
                    <tr>
                        <th>Created at</th>
                        <th>Phase ID</th>
                        <th>Hash Commit</th>
                        <th>Creator</th>
                        <th>Commit message</th>
                    </tr>
                </thead>
                <tbody>
                    {commits_data.map(cd => {
                        return (
                            <tr key={cd.hash_commit}>
                                <td>{formatDate(cd.created_at)}</td>
                                {phs_data && 
                                <td>{phs_data[cd.current_phase_id].name}</td>
                                }
                                <td className="hash-commit" title='view this commit'  onClick={(e) => {
                                        e.preventDefault();
                                        setViewCommits(cd)
                                    }}>{cd.hash_commit.slice(0,16)}</td>
                                {participants_data && 
                                <td>{participants_data[cd.creator_id]?.first_name} {participants_data[cd.creator_id]?.last_name}</td>}
                                <td className="commit-message">{cd.message}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}