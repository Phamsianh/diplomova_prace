import { useState, useEffect } from 'react';
import { CreateIcon, CancelIcon } from '../icon';
import {useController} from '../../controllers/'
const CreateSection = ({ handleCreate, cancelCreate }) => {
	const [name, setName] = useState('');
	const [position_id, setPositionId] = useState(1);
	const [order, setOrder] = useState('');
	const [positions, setPositions] = useState([]);
	const {PositionCtlr} = useController();

	useEffect(() => {
		PositionCtlr.get_rsc_col()
			.then((data) => {
				setPositions(data);
			})
			.catch((e) => console.error(e));
	}, []);

	return (
		<div className="section">
			<div className="create-section">
				<div className="manage-buttons">
					<button onClick={cancelCreate}>
						<CancelIcon />
					</button>
				</div>

				<h3>{name?name:'New Section'}</h3>
				<form onSubmit={handleCreate}>
					<label htmlFor="name">Name</label>
					<input
						type="text"
						id="name"
						value={name}
						onChange={(e) => setName(e.target.value)}
					/>

					<label htmlFor="position_id">Position</label>
					<br />
					<select
						id="position_id"
						onChange={(e) => setPositionId(e.target.value)}
						value={position_id}
					>
						{positions
							? positions.map((p) => {
									return (
										<option value={p.id} key={p.id}>
											{p.name}
										</option>
									);
							  })
							: ''}
					</select>
					<br />

					<label htmlFor="order">Order</label>
					<input
						type="text"
						id="order"
						value={order}
						onChange={(e) => setOrder(e.target.value)}
					/>
					<button type="submit">
						<CreateIcon />
					</button>
				</form>
			</div>
		</div>
	);
};

export default CreateSection;
