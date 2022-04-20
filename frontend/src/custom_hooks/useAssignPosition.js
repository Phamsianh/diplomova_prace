import { useState, useEffect } from 'react';
import { useController } from '../controllers';
import { CancelIcon, CreateIcon } from '../components/icon';

export const useAssignPosition = () => {
	const [positions_data, setPositionsData] = useState();
	const [assigning, setAssigning] = useState(false);
	const [assign_position_component, setAssignPositionComponent] = useState();
	const [success_component, setSuccessComponent] = useState();
	const { UserPositionCtlr, PositionCtlr } = useController();

	useEffect(() => {
		if (assigning) {
			setAssignPositionComponent(
				<AssignPosition
					positions={positions_data}
					handleSubmit={handleSubmit}
					cancelSubmit={cancelSubmit}
				/>
			);
		} else {
			setAssignPositionComponent(null);
		}
	}, [assigning]);

	function setAssignPosition(positions) {
		setAssigning(true);
		setPositionsData(positions);
	}


	useEffect(() => {
		if (!success_component) return;
		setTimeout(() => {
			setSuccessComponent(null);
		}, 3000);
	}, [success_component]);

	async function handleSubmit(e) {
		e.preventDefault();
		const req_bod = {
			user_id: e.target.selected_user_id.value,
			position_id: e.target.selected_position_id.value
		};
		const data = await UserPositionCtlr.post_rsc(req_bod);
		// console.log(data);
		setSuccessComponent(
			<AssignPositionSuccess clearMessage={clearMessage} />
		);
		setAssigning(false);
	}

	function cancelSubmit(e) {
		e.preventDefault();
		setAssigning(false);
	}

	function clearMessage(e) {
		e.preventDefault();
		setSuccessComponent(null);
	}

	return {assign_position_component, assigning, setAssignPosition, success_component};
};

function AssignPosition({
	positions,
	handleSubmit,
	cancelSubmit
}) {
	const [users, setUsers] = useState();
	// const [selected_holders, setHolders] = useState();
	// const [all_holders_data, setAllHoldersData] = useState();
	const [selected_position_id, setSelectedPositionId] = useState(positions[0].id);
	const [selected_user_id, setSelectedUserId] = useState(1);
	const { PositionCtlr, UserCtlr } = useController();
	// useEffect(() => {
	// 	if(!selected_position_id) return;
	// 	if(all_holders_data[selected_position_id]){
	// 		setHolders(all_holders_data[selected_position_id])
	// 	}
	// 	else{
	// 		PositionCtlr.get_rsc_col(selected_position_id, "holders").then(data => {
	// 			all_holders_data[selected_position_id] = data
	// 			setAllHoldersData(all_holders_data);
	// 			setHolders(data);
	// 		})
	// 	}
	// }, [selected_position_id])

	useEffect(() => {
		UserCtlr.get_rsc_col().then((data) => {
			// console.log("users_data", data);
			setUsers(data);
		})
	}, [])

	return (
	<div className="assign-position">
		<form onSubmit={handleSubmit}>
			<div className="manage-buttons">
				<button type="submit"><CreateIcon /></button>
				<button onClick={cancelSubmit}><CancelIcon /></button>
			</div>

			<h4>Select position to assign</h4>

			<label htmlFor="name">Name</label>
			
			<label htmlFor="selected_position_id">Position</label>
			{selected_position_id && <select name="selected_position_id" id="selected_position_id" value={selected_position_id} onChange={(e) => setSelectedPositionId(e.target.value)}>
				<option value="0">None</option>
				{positions.map(p => {
					return <option key={p.id} value={p.id}>{p.name} - {p.id}</option>
				})}
			</select>}

			<label htmlFor="selected_user_id">User</label>
			{selected_user_id && <select name="selected_user_id" id="selected_user_id" value={selected_user_id} onChange={(e) => setSelectedUserId(e.target.value)}>
				{users && users.map(u => {
					return <option key={u.id} value={u.id}>{u.first_name} {u.last_name} - {u.id}</option>
				})}
			</select>}
		</form>
	</div>
	);
}

function AssignPositionSuccess({ clearMessage }) {
	return (
		<div>
			<h4>Position is created successfully</h4>
			<button onClick={clearMessage}>
				<CancelIcon />
			</button>
		</div>
	);
}
