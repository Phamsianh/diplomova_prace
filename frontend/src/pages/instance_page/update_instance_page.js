import { useEffect, useState, createContext, useContext } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { ReadInstance } from '../../components/instance/read_instance';
import { ReadFormPhases } from '../../components/instance/form/read_form_phases';
import { InstanceContentContext } from './read_instance_page';
import {
	CancelIcon,
	CommitsPageIcon,
	HandleInstanceIcon,
	ReadIcon,
	TransitInstanceIcon,
} from '../../components/icon';
import { useController } from '../../controllers';
import { TransitInstance } from '../../components/instance/form/transit_instance';
import { HandleInstance } from '../../components/instance/form/handle_instance';
import { UserContext } from '../../App';

export const UpdateInstancePage = () => {
	const { id: instance_id } = useParams();
	const { InstanceCtlr, FormCtlr } = useController();
	const navigate = useNavigate();
	const { user_data } = useContext(UserContext);

	const [instance_data, setInstanceData] = useState();
	const [form_data, setFormData] = useState();
	const [content_data, setContentData] = useState();

	const [is_participant, setIsParticipant] = useState(false);
	const [is_potential_handler, setIsPotentialHandler] = useState(false);

	const [can_be_handled, setCanBeHandled] = useState(false);
	const [is_handling, setIsHandling] = useState(false);
	const [can_be_transited, setCanBeTransited] = useState(false);
	const [is_transiting, setIsTransiting] = useState(false);

	// Only initialize UpdateInstancePage when:
	// 1. user is a current potential handler of current phase OR
	// 2. a participant of instance.
	useEffect(() => {
		if (user_data) {
			InstanceCtlr.get_rel_rsc(instance_id, 'participants').then((data) => {
				if (data.find((participant) => participant.id === user_data.id)) {
					setIsParticipant(true);
				}
			});
			InstanceCtlr.get_rel_rsc(instance_id, 'current_potential_handlers').then(
				(data) => {
					if (
						data.find(
							(potential_handler) =>
								potential_handler.id === user_data.id
						)
					) {
						setIsPotentialHandler(true);
					}
				}
			);
		}
	}, [user_data]);
	useEffect(() => {
		if (is_participant || is_potential_handler) {
			InstanceCtlr.get_rsc_ins(instance_id).then((data) => {
				console.log('instancedata', data);
				setInstanceData(data);

				FormCtlr.get_rsc_ins(data.form_id).then((data) => {
					console.log('formdata', data);
					setFormData(data);
				});
			});
			InstanceCtlr.get_rel_rsc(instance_id, 'instances_fields').then(
				(data) => {
					console.log('content data', data);
					setContentData(data);
				}
			);
		}
	}, [is_participant, is_potential_handler])

	// Depend on current state of instance and role of user to this instance, check if current user can:
	useEffect(() => {
		if (user_data && instance_data) {
			// 1. Handle this instance at current phase?
			if (
				['full received', 'full received & partial resolved'].includes(
					instance_data.current_state
				)
			) {
				setCanBeHandled(false);
			} else if (
				[
					'pending',
					'partial received',
					'partial received & partial resolved',
				].includes(instance_data.current_state)
			) {
				InstanceCtlr.get_rel_rsc(
					instance_data.id,
					'current_potential_handlers'
				).then((data) => {
					console.log('potential handlers', data);
					if (
						data.find((potential_handler) => {
							return potential_handler.id === user_data.id;
						})
					) {
						setCanBeHandled(true);
						console.log("i'm a potential handler");
					} else {
						setCanBeHandled(false);
						console.log("i'm not a potential handler");
					}
				});
			}
			// 2. Transit instance to next phase?
			if (instance_data.current_state === 'full resolved') {
				InstanceCtlr.get_rel_rsc(
					instance_data.id,
					'current_director'
				).then((data) => {
					console.log('current director: ', data);
					if (data && data.id === user_data.id) {
						console.log("i'm director of this phase");
						setCanBeTransited(true);
					} else {
						console.log("i'm not director of this phase");
						setCanBeTransited(false);
					}
				});
			} else setCanBeTransited(false);
		}
	}, [instance_data, user_data]);

	// Transit instance logic happens here
	const transitInstance = async (e) => {
		e.preventDefault();
		const req_bod = {
			current_phase_id: e.target.current_phase_id.value,
		};
		let data = await InstanceCtlr.patch_rsc_ins(instance_id, req_bod);
		console.log(data);
		setInstanceData(data);
		setIsTransiting(false);
	};

	// Handle instance logic's quite complex, so it happens inside HandleInstance component.

	return (
		<div className="update-instance-page">
			{!(is_potential_handler || is_participant)
				? "You're not a potential handler nor a participant of this instance"
				: instance_data &&
				  form_data &&
				  content_data && (
						<InstanceContentContext.Provider
							value={{
								instance_data,
								setInstanceData, // child component UpdateFieldContent will update instance state when it updated field
								content_data,
								setContentData, // child component HandleInstance will update content when user handle some parts of instance.
								page: 'update',
							}}
						>
							<div className="instance">
								<div className="manage-buttons">
									{/* --------TRANSIT BUTTON---------  */}
									{is_transiting ||
									is_handling ||
									!can_be_transited ? (
										''
									) : (
										<button
											title="Transiting Instance"
											onClick={() =>
												setIsTransiting(true)
											}
										>
											<TransitInstanceIcon />
										</button>
									)}
									{is_transiting && (
										<button
											title="Cancel Transiting"
											onClick={() =>
												setIsTransiting(false)
											}
										>
											<CancelIcon />
										</button>
									)}
									{/* ----------HANDLE BUTTON---------- */}
									{is_handling ||
									is_transiting ||
									!can_be_handled ? (
										''
									) : (
										<button
											title="Handle Instance"
											onClick={() => setIsHandling(true)}
										>
											<HandleInstanceIcon />
										</button>
									)}
									{is_handling && (
										<button
											title="Cancel Handle Instance"
											onClick={() => setIsHandling(false)}
										>
											<CancelIcon />
										</button>
									)}
									{/* ------------VIEW COMMITS BUTTON-------------- */}
									{is_transiting || is_handling ? (
										''
									) : (
										<Link
											title="View Commits"
											to={'/instances/' + instance_id + '/commits'}
										>
											<CommitsPageIcon />
										</Link>
									)}
									{/* ------------VIEW INSTANCE BUTTON-------------- */}
									{is_transiting || is_handling ? (
										''
									) : (
										<Link
											title="View Instance"
											to={'/instances/' + instance_id}
										>
											<ReadIcon />
										</Link>
									)}
								</div>

								{<ReadInstance instance_data={instance_data} />}

								{is_transiting && (
									<TransitInstance
										old_instance_data={instance_data}
										handleUpdateInstance={transitInstance}
									/>
								)}
								{is_handling && (
									<HandleInstance
										instance_data={instance_data}
										setInstanceData={setInstanceData}
										setIsHandling={setIsHandling}
									/>
								)}

								{<ReadFormPhases form_data={form_data} />}
							</div>
						</InstanceContentContext.Provider>
				  )}
		</div>
	);
};
