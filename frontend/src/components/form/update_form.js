import { useState } from 'react';
import { SaveIcon } from '../icon';

export const UpdateForm = ({ old_form_data, handleSubmit}) => {
	const [form_name, setForm_name] = useState(old_form_data.name);
    const [form_public, setPublic] = useState(old_form_data.public)
    const [form_obsolete, setObsolete] = useState(old_form_data.obsolete)

    function updateFormname(e) {
        if (!old_form_data.public || !old_form_data.obsolete) {
            setForm_name(e.target.value)
        }
    }
    function publicForm(e) {
        if (!old_form_data.public) {
            setPublic(!form_public)
        }

    }
    function obsoleteForm(e) {
        if (old_form_data.public && !old_form_data.obsolete) {
            setObsolete(!form_obsolete)
        }
    }
	return (
		<div className="update-form">
            <form onSubmit={handleSubmit}>
                <label htmlFor="name">Form Name</label>
                <input
                    type="text" 
                    required
                    placeholder="Form Name"
                    name="name"
                    value={form_name}
                    onChange={updateFormname}
                />

                <label htmlFor="public">Public</label>
                <input type="checkbox" name="public" id="public" onChange={publicForm} checked={form_public}/><br />

                <label htmlFor="obsolete">Obsolete</label>
                <input type="checkbox" name="obsolete" id="obsolete" onChange={obsoleteForm} checked={form_obsolete}/><br />

                <button type="submit"><SaveIcon/></button>
            </form>
		</div>
	);
};

// export default UpdateForm;
