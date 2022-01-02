import { formatDate } from '../../utils/datetime';

const ReadPhase = ({ phase_data }) => {
	return (
		<div className="read-phase">
			<h2 className="name">
				{phase_data.name ? phase_data.name : 'Phase Name'}
			</h2>
			<details>
				<summary></summary>
				<p className="phase-id">Phase ID: {phase_data.id}</p>
				<p className="created-at" title={phase_data.created_at}>
					Created at: {formatDate(phase_data.created_at)}
				</p>
				<p className="description">
					Description: {phase_data.description}
				</p>
				<p className="position-id">
					Position ID: {phase_data.position_id}
				</p>
				<p className="phase-type">
					Phase type: {phase_data.phase_type}
				</p>
			</details>
		</div>
	);
};

export default ReadPhase;
