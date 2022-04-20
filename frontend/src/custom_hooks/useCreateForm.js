import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreateForm = (setFormsData) => {
    const [creating, setCreating] = useState(false);
    const [fds_data, setFdsData] = useState();
    const [create_form_component, setCreateFormComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const {FormCtlr} = useController();

    function setCreateForm( forms_data) {
        setCreating(true);
        setFdsData(forms_data);
    }

    useEffect(() => {
        if (creating) {
            setCreateFormComponent(
                <CreateForm handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreateFormComponent(null);
        }
    }, [creating])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
			name: e.target.name.value,
		};
        const data = await FormCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreateFormSuccess clearMessage={clearMessage}/>)
        setFormsData([...fds_data, data])
        setCreating(false);
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setCreating(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

  return {create_form_component, setCreateForm, creating, success_component};
};


const CreateForm = ({handleSubmit, cancelSubmit}) => {
    const [name, setName] = useState('New Form');
	return (
        <div className="create-form">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h4>{name?name:'New Form'}</h4>

                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </form>
        </div>
	);
}

function CreateFormSuccess({clearMessage}) {
    return (
        <div>
            <h4>Form is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}