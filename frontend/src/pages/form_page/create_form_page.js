import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {useController} from '../../controllers'

const CreateFormPage = () => {
	const [form_name, setForm_name] = useState('Form Name');
    const navigate = useNavigate();
    const {FormCtlr} = useController();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const req_bod = {"name": form_name}
        let data = await FormCtlr.post_rsc(req_bod)
		// console.log("form data from api", data);
        navigate(`/forms/${data.id}/update`)
    }
    
	return (
		<div className="create-form">
            <form onSubmit={handleSubmit}>
                <label htmlFor="name">Form Name</label>
                <input
                    type="text" 
                    required
                    placeholder="Name"
                    name="name"
                    value={form_name}
                    onChange={(e) => setForm_name(e.target.value)}
                />
                <input type="submit" value="Create Form" />
            </form>
		</div>
	);
};

export default CreateFormPage;
