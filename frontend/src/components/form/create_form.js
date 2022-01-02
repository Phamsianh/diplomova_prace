import React from 'react';
import { useState } from 'react';
import { CreateIcon } from '../icon';

const CreateForm = ({handleSubmit}) => {
	const [form_name, setForm_name] = useState('');
	return (
		<div className="create-form">
            <form onSubmit={handleSubmit}>
                <label htmlFor="name">Form Name</label>
                <input
                    type="text" 
                    required
                    placeholder="Form Name"
                    name="name"
                    value={form_name}
                    onChange={(e) => setForm_name(e.target.value)}
                />
                <button type="submit"><CreateIcon/></button>
            </form>
		</div>
	);
};

export default CreateForm;
