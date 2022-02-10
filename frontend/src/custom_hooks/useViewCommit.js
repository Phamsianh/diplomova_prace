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
    const [view_commits_component, setViewCommitsComponent] = useState();

    const {CommitCtlr} = useController();

    useEffect(() => {
        if (reading) {
            setViewCommitsComponent(
                <ReadCommits 
                commits_data={commits_data} 
                setViewCommits={setViewCommits}
                cancelRead={cancelRead}/>
            )
        }
        else {
            setViewCommitsComponent(null)
        }
    }, [reading])

    function setReadCommits(commits_data, instances_fields_data, instance_data){
        setReading(true);
        setCommitsData(commits_data);
        // only store current instances fields data if it's null
        if (!current_instances_fields_data) setCurrentInstancesFieldsData(instances_fields_data);
        if (!current_instance_data) setCurrentInstanceData(instance_data)
    }

    function cancelRead(e) {
        e.preventDefault();
        setReading(false);
    }

    async function setViewCommits(commit_data) {
        let decrypt_instances_fields
        if (!all_envelopes[commit_data.hash_commit]) {
            let data = await CommitCtlr.get_rel_rsc(commit_data.hash_commit, 'envelopes');
            console.log('envelopes data', data);
            decrypt_instances_fields = CommitCtlr.convertEnvelopeToContent(data);
            console.log('decrypt instances fields', decrypt_instances_fields);
            all_envelopes[commit_data.hash_commit] = decrypt_instances_fields
            console.log('all envelopes data', all_envelopes);
            setAllEnvelopes(all_envelopes)
            setInstancesFieldsData(decrypt_instances_fields);
        }
        else {
            setInstancesFieldsData(all_envelopes[commit_data.hash_commit])
        }

        let ins_data = Object.assign({}, current_instance_data);
        ins_data.current_phase_id = commit_data.current_phase_id;
        console.log("instance data view commit", ins_data);
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
    setViewCommits,
    cancelRead
}) {
    return (
        <div className="view-commits">
            <div className="manage-buttons">
                <button onClick={cancelRead}><CancelIcon/></button>
            </div>

            <h3 className="action">View commits</h3>
            <table>
                <thead>
                    <tr>
                        <th>Created at</th>
                        <th>Phase ID</th>
                        <th>Previous Commit</th>
                        <th>Hash Commit</th>
                        <th>Commit message</th>
                    </tr>
                </thead>
                <tbody>
                    {commits_data.map(cd => {
                        return (
                            <tr key={cd.hash_commit}>
                                <td>{formatDate(cd.created_at)}</td>
                                <td>{cd.current_phase_id}</td>
                                <td className="prev-hash">{cd.prev_hash_commit?cd.prev_hash_commit.slice(0,16): 'first commit'}</td>
                                <td className="hash-commit" title='view this commit'  onClick={(e) => {
                                        e.preventDefault();
                                        setViewCommits(cd)
                                    }}>{cd.hash_commit.slice(0,16)}</td>
                                <td className="commit-message">{cd.message}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}