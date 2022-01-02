import { useState } from 'react';
import { CancelIcon, CreateIcon } from '../icon';

const CreateField = ({ handleCreate, cancelCreate }) => {
	const [name, setName] = useState('');
	const [order, setOrder] = useState('');
	return (
		<div className="field">
			<div className="create-field">
				<div className="manage-buttons">
					<button onClick={cancelCreate}>
						<CancelIcon />
					</button>
				</div>

				<h4>{name?name:'New Field'}</h4>
				<form onSubmit={handleCreate}>
					<label htmlFor="name">Name</label>
					<input
						type="text"
						id="name"
						value={name}
						onChange={(e) => setName(e.target.value)}
					/>
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

export default CreateField;
