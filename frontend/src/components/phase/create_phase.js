import { useState, useEffect } from 'react';
import { PositionController } from '../../controllers/PositionController';
import { CancelIcon, CreateIcon } from '../icon';

const CreatePhase = ({handleCreate, cancelCreate}) => {
	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [position_id, setPositionId] = useState('');
	const [phase_type, setPhaseType] = useState('transit');
	const [positions, setPositions] = useState('');

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
		<div className="phase">
			<div className='create-phase'>
				<div className="manage-buttons">
					<button onClick={cancelCreate}><CancelIcon/></button>
				</div>
				
				<h2>{name?name:'New Phase'}</h2>
				<form onSubmit={handleCreate}>
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

					<label htmlFor="position_id">Position</label><br />
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
					<button type="submit"><CreateIcon/></button>
				</form>
			</div>
		</div>
	);
};

export default CreatePhase;
