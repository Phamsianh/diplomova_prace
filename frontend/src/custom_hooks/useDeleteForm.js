import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { CancelIcon, CreateIcon, NoIcon, YesIcon } from '../components/icon';
import { useController } from '../controllers';

export const useDeleteForm = () => {
    const [deleting, setDeleting] = useState(false);
    const [delete_form_component, setDeleteFormComponent] =  useState();
    const [form_data, setFormData] = useState();
    const [success_component, setSuccessComponent] = useState();

    const {FormCtlr} = useController();
    const navigate = useNavigate()

    function setDeleteForm(form_data) {
        setDeleting(true);
        setFormData(form_data)
    }

    useEffect(() => {
        if (deleting) {
            setDeleteFormComponent(
                <DeleteForm handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} form_data={form_data} />
            )
        }
        else {
            setDeleteFormComponent(null);
        }
    }, [deleting])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])


    async function handleSubmit(e) {
        e.preventDefault();
        const data = await FormCtlr.delete_rsc_ins(form_data.id);
        if (!data) {
            setSuccessComponent(<DeleteFormSuccess clearMessage={clearMessage}/>)
            setTimeout(() => {
                navigate("/forms")
            }, 4000)
        }
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setDeleting(false);
    }

        
    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

  return {delete_form_component , setDeleteForm, deleting, success_component};
};

const DeleteForm = ({handleSubmit, cancelSubmit}) => {
    return (
        <div className="delete-form">
            <form onSubmit={handleSubmit}>
                <h2>Do you want to delete this form</h2>
                <div>
                    <button className='delete-option-button' onSubmit={handleSubmit}><YesIcon/></button> Yes
                </div>
                <div>
                    <button className='delete-option-button' onClick={cancelSubmit}><NoIcon/></button> No
                </div>
            </form>
        </div>
    )
}


function DeleteFormSuccess({clearMessage}) {
    return (
        <div>
            <h4>Form is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}