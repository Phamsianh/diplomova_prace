import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useController } from '../../../controllers';
import { UserContext } from '../../../App';
import { ReadCommits } from '../../../components/commit/read_commits';
import './main.css';
import { ReadFormPhases } from '../../../components/instance/form/read_form_phases';
import { ReadInstance } from '../../../components/instance/read_instance';
import { InstanceContentContext } from '../read_instance_page';
import { Link } from 'react-router-dom';
import { ReadIcon, UpdateIcon, CommitsPageIcon } from '../../../components/icon';

export const ReadCommitPage = () => {
	const { id: instance_id, hash_commit } = useParams();
	const { InstanceCtlr, FormCtlr, CommitCtlr } = useController();
	const { user_data } = useContext(UserContext);

	const [is_participant, setIsParticipant] = useState(false);

	const [instance_data, setInstanceData] = useState();
	const [form_data, setFormData] = useState();
	const [commit_data, setCommitData] = useState();
	const [envelopes_data, setEnvelopesData] = useState();

	// Only initialize ReadCommits when:
	// 1. user is a current potential handler of current phase OR
	// 2. a participant of instance.
	useEffect(() => {
		if (user_data) {
			InstanceCtlr.get_rel_rsc(instance_id, 'participants').then(
				(data) => {
					if (
						data.find(
							(participant) => participant.id === user_data.id
						)
					) {
						setIsParticipant(true);
					}
				}
			);
		}
	}, [user_data]);
	useEffect(() => {
		if (is_participant) {
			InstanceCtlr.get_rsc_ins(instance_id).then((data) => {
				console.log('instance: ', data);
				setInstanceData(data);
				FormCtlr.get_rsc_ins(data.form_id).then((data) => {
					setFormData(data);
				});
			});

			CommitCtlr.get_rsc_ins(hash_commit).then((data) => {
				console.log('commit: ', data);
				setCommitData(data);
			});
			CommitCtlr.get_rel_rsc(hash_commit, 'envelopes').then((data) => {
				setEnvelopesData(CommitCtlr.convertEnvelopeToContent(data));
			});
		}
	}, [is_participant]);

	return (
		<div className="read-commit-page page">
			<div className="commit">
				{!is_participant ? (
					"You're not a participant of this instance"
				) : (
					<div className="instance">
						<div className="manage-buttons">
							<Link
								to={`/instances/${instance_id}/commits`}
								title="View Commits"
							>
								<CommitsPageIcon />
							</Link>
							<Link
								to={`/instances/${instance_id}/update`}
								title="Update Instance"
							>
								<UpdateIcon />
							</Link>
							<Link
								to={`/instances/${instance_id}`}
								title="View Instance"
							>
								<ReadIcon />
							</Link>
						</div>

						{commit_data && (
							<InstanceContentContext.Provider
								value={{
									instance_data,
									content_data: envelopes_data,
									page: 'read',
								}}
							>
								{instance_data && (
									<ReadInstance
										instance_data={instance_data}
									/>
								)}
								{form_data && (
									<ReadFormPhases form_data={form_data} />
								)}
							</InstanceContentContext.Provider>
						)}
					</div>
				)}
			</div>
		</div>
	);
};
