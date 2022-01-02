import { useState, useEffect } from 'react';
import { PositionController } from '../../controllers/PositionController';
import { SaveIcon } from '../icon';

const UpdateSection = ({ old_section_data, handleUpdateSection }) => {
	const [name, setName] = useState(old_section_data.name);
	const [position_id, setPositionId] = useState(old_section_data.position_id);
	const [order, setOrder] = useState(old_section_data.order);
	const [positions, setPositions] = useState([]);

	useEffect(() => {
		const position_ctlr = new PositionController('phamsianh97');
		position_ctlr
			.get_rsc_col()
			.then((data) => {
				setPositions(data);
			})
			.catch((e) => console.error(e));
	}, []);

	return (
		<div className="update-section">
			<form onSubmit={handleUpdateSection}>
				<label htmlFor="name">Name</label>
				<input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>

				<label htmlFor="position_id">Position</label>
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
                <button type="submit"><SaveIcon/></button>
			</form>
		</div>
	);
};

export default UpdateSection;
