import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateForm = (setFormData) => {
    const [updating, setUpdating] = useState(false);
    const [update_form_component, setUpdateFormComponent] =  useState();
    const [f_data, setFData] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { FormCtlr } = useController();

    function setFormToUpdate(form_data) {
        if (updating) return
        setUpdating(true);
        setFData(form_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateFormComponent(
                <UpdateForm old_form_data={f_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateFormComponent(null);
		};
    }, [updating])

	useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit (e) {
        e.preventDefault();
        const req_bod = {
			name: e.target.name.value,
            public: e.target.public.checked,
            obsolete: e.target.obsolete.checked
		};
		let data = await FormCtlr.patch_rsc_ins(f_data.id, req_bod);
        console.log("updated form data", data);
        setSuccessComponent(<UpdateFormSuccess clearMessage={clearMessage}/>)
        setFormData(data);
        setUpdating(false);
    }

    function cancelSubmit (e) {
        e.preventDefault();
        setUpdating(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

	return {update_form_component, setFormToUpdate, updating, success_component};
};

const UpdateForm = ({ old_form_data, handleSubmit, cancelSubmit }) => {
	const [form_name, setForm_name] = useState(old_form_data.name);
	const [form_public, setPublic] = useState(old_form_data.public);
	const [form_obsolete, setObsolete] = useState(old_form_data.obsolete);
	function updateFormname(e) {
		if (!old_form_data.public || !old_form_data.obsolete) {
			setForm_name(e.target.value);
		}
	}
	function publicForm(e) {
		if (!old_form_data.public) {
			setPublic(!form_public);
		}
	}
	function obsoleteForm(e) {
		if (old_form_data.public && !old_form_data.obsolete) {
			setObsolete(!form_obsolete);
		}
	}
	return (
		<div className="update-form">
			<form onSubmit={handleSubmit}>
				<div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

				<h2 className="action">Updating Form</h2>

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
				<input
					type="checkbox"
					name="public"
					id="public"
					onChange={publicForm}
					checked={form_public}
				/>
				<br />

				<label htmlFor="obsolete">Obsolete</label>
				<input
					type="checkbox"
					name="obsolete"
					id="obsolete"
					onChange={obsoleteForm}
					checked={form_obsolete}
				/>
				<br />
			</form>
		</div>
	);
};

function UpdateFormSuccess({clearMessage}) {
    return (
        <div>
            <h4>Form is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}