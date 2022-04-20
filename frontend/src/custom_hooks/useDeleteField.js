import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';

export const useDeleteField = (setFieldsData) => {
    const [success_component, setSuccessComponent] = useState();
    
    const { FieldCtlr } = useController();

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])
    
    async function deleteField(field_data, fields_data) {
		let data = await FieldCtlr.delete_rsc_ins(field_data.id);
        // console.log(data);
        if (data == null) {
            // console.log(fields_data.filter(fd => fd.id != field_data.id));
            setSuccessComponent(<DeleteFieldSuccess clearMessage={clearMessage}/>)
            setFieldsData(fields_data.filter(fd => fd.id != field_data.id))    
        }
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }
    
    return {deleteField, success_component};
};

function DeleteFieldSuccess({clearMessage}) {
    return (
        <div>
            <h4>Field is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}