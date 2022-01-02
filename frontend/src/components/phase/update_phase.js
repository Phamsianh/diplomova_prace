import { useState, useEffect } from 'react';
import { PositionController } from '../../controllers/PositionController';
import { SaveIcon } from '../icon';

const UpdatePhase = ({ old_phase_data, handleSubmit}) => {
	const [name, setName] = useState(old_phase_data.name);
	const [description, setDescription] = useState(old_phase_data.description);
	const [position_id, setPositionId] = useState(old_phase_data.position_id);
	const [phase_type, setPhaseType] = useState(old_phase_data.phase_type);
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
		<div className='update-phase'>
			<form onSubmit={handleSubmit}>
				<label htmlFor="name">Name</label>
				<input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>

				<label htmlFor="description">Description</label>
				<input
					type="text"
					id="description"
					value={description}
					onChange={(e) => setDescription(e.target.value)}
				/>

				<label htmlFor="position_id">Position</label>
				<select id="position_id" onChange={(e) => setPositionId(e.target.value)} value={position_id}>
					{positions
						? positions.map((p) => {
								return (
									<option
										value={p.id}
                                        key={p.id}
									>
										{p.name}
									</option>
								);
						  })
						: ''}
				</select><br />
                
				<label htmlFor="phase_type">Phase Type</label>
				<select
					id="phase_type"
					value={phase_type}
					onChange={(e) => setPhaseType(e.target.value)}
				>
					<option value="begin">Begin</option>
					<option value="transit">Transit</option>
					<option value="end">End</option>
				</select><br />
				<button type="submit"><SaveIcon/></button>
			</form>
		</div>
	);
};

export default UpdatePhase;
