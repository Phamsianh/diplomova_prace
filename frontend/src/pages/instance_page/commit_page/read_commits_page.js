import { useContext, useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import { useController } from "../../../controllers"
import { UserContext } from "../../../App"
import { ReadCommits } from "../../../components/commit/read_commits"
import './main.css'
import { ReadIcon, UpdateIcon } from "../../../components/icon"


export const ReadCommitsPage = () => {
    const { id: instance_id } = useParams();
	const { InstanceCtlr } = useController();
	const { user_data } = useContext(UserContext);

	const [is_participant, setIsParticipant] = useState(false);

	const [instance_data, setInstanceData] = useState();
	const [form_data, setFormData] = useState();
	const [commits_data, setCommitsData] = useState();

	// Only initialize ReadCommits when:
	// 1. user is a current potential handler of current phase OR
	// 2. a participant of instance.
	useEffect(() => {
		if (user_data) {
			InstanceCtlr.get_rel_rsc(instance_id, 'participants').then((data) => {
				if (data.find((participant) => participant.id === user_data.id)) {
					setIsParticipant(true);
				}
			});
		}
	}, [user_data]);
	useEffect(() => {
		if (is_participant) {
			InstanceCtlr.get_rsc_ins(instance_id).then((data) => {
				console.log('instance: ', data);
				setInstanceData(data);
			});

			InstanceCtlr.get_rel_rsc(instance_id, 'commits').then(
				(data) => {
					console.log('commits: ', data);
					setCommitsData(data);
				}
			); 
		}
	}, [is_participant]);

    return (
        <div className='read-commits-page page'>
			<div className="manage-buttons">
				<Link to={`/instances/${instance_id}`} title="View Instance"><ReadIcon/></Link>
				<Link to={`/instances/${instance_id}/update`} title="Update Instance"><UpdateIcon/></Link>
			</div>
			<div className="commits">
                {!is_participant ? (
                    "You're not a participant of this instance"
                ) : (
                    commits_data && <ReadCommits commits_data={commits_data}/>
                )}
            </div>
		</div>
    )
}
