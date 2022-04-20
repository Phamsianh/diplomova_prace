import { useState, useEffect, createContext, useContext } from 'react';
import { ReadInstance } from '../../components/instance/read_instance';
import { useParams } from 'react-router-dom';
import { ReadFormPhases } from '../../components/instance/form/read_form_phases';
import { Link } from 'react-router-dom';
import { CommitsPageIcon, UpdateIcon } from '../../components/icon';
import { useController } from '../../controllers';
import { UserContext } from '../../App';

export const InstanceContentContext = createContext();

export const ReadInstancePage = () => {
	const { id: instance_id } = useParams();
	const { FormCtlr, InstanceCtlr } = useController();
	const { user_data } = useContext(UserContext);

	const [is_participant, setIsParticipant] = useState(false);
	const [is_potential_handler, setIsPotentialHandler] = useState(false);

	const [instance_data, setInstanceData] = useState();
	const [form_data, setFormData] = useState();
	const [content_data, setContentData] = useState();

	// Only initialize ReadInstancePage when:
	// 1. user is a current potential handler of current phase OR
	// 2. a participant of instance.
	useEffect(() => {
		if (user_data) {
			InstanceCtlr.get_rel_rsc(instance_id, 'participants').then((data) => {
				if (data.find((participant) => participant.id === user_data.id)) {
					setIsParticipant(true);
				}
			});
	
			InstanceCtlr.get_rel_rsc(
				instance_id,
				'current_potential_handlers'
			).then((data) => {
				if (
					data.find(
						(potential_handler) => potential_handler.id === user_data.id
					)
				) {
					setIsPotentialHandler(true);
				}
			});
		}
	}, [user_data]);
	useEffect(() => {
		if (is_participant || is_potential_handler) {
			InstanceCtlr.get_rsc_ins(instance_id).then((data) => {
				// console.log('instancedata', data);
				setInstanceData(data);

				FormCtlr.get_rsc_ins(data.form_id).then((data) => {
					// console.log('formdata', data);
					setFormData(data);
				});
			});

			InstanceCtlr.get_rel_rsc(instance_id, 'instances_fields').then(
				(data) => {
					// console.log('content data', data);
					setContentData(data);
				}
			);
		}
	}, [is_participant, is_potential_handler]);

	return (
		<div className="read-instance-page">
			{!(is_participant || is_potential_handler) ? (
				"You're not a potential handler nor a participant of this instance"
			) : (
				<div className="instance">
					<div className="manage-buttons">
						<Link to={`/instances/${instance_id}/commits`} title='View Commit'>
							<CommitsPageIcon/>
						</Link>
						<Link to={`/instances/${instance_id}/update`} title="Update Instance">
							<UpdateIcon />
						</Link>
					</div>

					{content_data && (
						<InstanceContentContext.Provider
							value={{
								instance_data,
								content_data,
								page: 'read',
							}}
						>
							{instance_data && (
								<ReadInstance instance_data={instance_data} />
							)}
							{form_data && (
								<ReadFormPhases form_data={form_data} />
							)}
						</InstanceContentContext.Provider>
					)}
				</div>
			)}
		</div>
	);
};
