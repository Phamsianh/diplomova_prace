import { useEffect, useState } from 'react';
import { useController } from '../../controllers'
import { formatDate } from '../../utils/datetime';

export const ReadTransition = ({ transition_data }) => {
	const [to_phase_data, setToPhaseData] = useState();
	const { TransitionCtlr } = useController()

	useEffect(() => {
		TransitionCtlr.get_rel_rsc(transition_data.id, 'to_phase').then(
			(data) => {
				setToPhaseData(data);
			}
		);
	}, []);

	return (
		<div className="read-transition">
			<h2 className="name">
				{transition_data.name
					? transition_data.name
					: 'Transition Name'}
			</h2>
			{to_phase_data && (
				<details>
					<summary>Transition details</summary>
					<p className="to-phase-name">
						To: {to_phase_data.name}
					</p>
					<p className="to-phase-id">
						ID: {transition_data.to_phase_id}
					</p>
					<p className="created-at" title={transition_data.created_at}>
						Created at: {formatDate(transition_data.created_at)}
					</p>
				</details>
			)}

		</div>
	);
};
