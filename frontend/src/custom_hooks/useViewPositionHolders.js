import { useState, useEffect } from 'react';
import { useController } from '../controllers';
import { CancelIcon, CreateIcon } from '../components/icon';

export const useViewPositionHolders = () => {
	const [positions_data, setPositionsData] = useState();
	const [viewing, setViewing] = useState(false);
	const [view_position_holder_component, setAssignPositionComponent] = useState();

	useEffect(() => {
		if (viewing) {
			setAssignPositionComponent(
				<ViewPositionHolders
					positions={positions_data}
					cancelSubmit={cancelSubmit}
				/>
			);
		} else {
			setAssignPositionComponent(null);
		}
	}, [viewing]);

	function setViewPositionHolder(positions) {
		setViewing(true);
		setPositionsData(positions);
	}




	function cancelSubmit(e) {
		e.preventDefault();
		setViewing(false);
	}

	return {
		view_position_holder_component,
		viewing,
		setViewPositionHolder,
	};
};

function ViewPositionHolders ({ positions, cancelSubmit }) {
	const [all_holders_data, setAllHoldersData] = useState({});
	const [holders, setHolders] = useState();
	const [selected_position_id, setSelectedPositionId] = useState(positions[0].id);

	const { PositionCtlr } = useController();
	useEffect(() => {
		if(!selected_position_id) return;
		if(all_holders_data[selected_position_id] !== undefined){
			setHolders(all_holders_data[selected_position_id])
		}
		else{
			PositionCtlr.get_rel_rsc(selected_position_id, "holders").then(data => {
				all_holders_data[selected_position_id] = data;
				console.log("holders", data);
				setAllHoldersData(all_holders_data);
				setHolders(data);
			})
		}
	}, [selected_position_id])

	return (
		<div className="view-position-holders">
			<div className="manage-buttons">
				<button onClick={cancelSubmit}><CancelIcon /></button>
			</div>

			<h2>Position's holders</h2>
			<p>Select position to view its holders</p>
			<select name="selected_position_id" id="selected_position_id" value={selected_position_id} onChange={e => setSelectedPositionId(e.target.value)}>
				{positions.map(p => {
					return <option key={p.id} value={p.id}>{p.name} - {p.id}</option>
				})}
			</select>
			<table>
				<thead>
					<tr>
						<th>Name</th>
						<th>Phone</th>
						<th>Address</th>
						<th>Email</th>
					</tr>
				</thead>
				<tbody>
					{holders && holders.map(h => {
						return <tr key={h.id}>
							<td>{h.first_name} {h.last_name}</td>
							<td>{h.phone}</td>
							<td>{h.address}</td>
							<td>{h.email}</td>
						</tr>
					})}
				</tbody>
			</table>
		</div>
	);
}