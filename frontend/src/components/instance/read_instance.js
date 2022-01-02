import { formatDate } from '../../utils/datetime';

export const ReadInstance = ({ instance_data }) => {
	return (
		<div className="read-instance">
			<h1 className="instance-id">Instance ID: {instance_data.id}</h1>
			<details>
				<summary></summary>
				<p className="created-at" title={instance_data.created_at}>
					Created at: {formatDate(instance_data.created_at)}
				</p>
				<p className="current-phase-id">
					Current Phase ID: {instance_data.current_phase_id}
				</p>
				<p className="creator-id">
					Creator ID: {instance_data.creator_id}
				</p>
				<p className="current-state">
					Current state: {instance_data.current_state}
				</p>
			</details>
		</div>
	);
};
