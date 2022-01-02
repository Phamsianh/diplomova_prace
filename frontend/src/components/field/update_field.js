import { useState } from 'react';
import { SaveIcon } from '../icon';

const UpdateField = ({old_field_data, handleSubmit}) => {
	const [name, setName] = useState(old_field_data.name);
	const [order, setOrder] = useState(old_field_data.setOrder);
    return (
        <div className="update-field">
            <form onSubmit={handleSubmit}>
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
				<button type='submit'><SaveIcon/></button>
            </form>
        </div>
    )
}

export default UpdateField
