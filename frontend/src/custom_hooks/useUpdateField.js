import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateField = (setFieldsData) => {
    const [updating, setUpdating] = useState(false);
    const [field_data, setFieldData] = useState();
    const [section_data, setSectionData] = useState();  // Consider to update to another section
    const [fs_data, setFsData] = useState();
    const [update_field_component, setUpdateFieldComponent] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { FieldCtlr } = useController();

    function setFieldToUpdate(field_data, fields_data, section_data) {
        if (updating) return;
        setUpdating(true);
        setFieldData(field_data);
        setSectionData(section_data);
        setFsData(fields_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateFieldComponent(
                <UpdateField old_field_data={field_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateFieldComponent(null);
		};
    }, [updating])

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
			order: !isNaN(e.target.order.value) ? 1 : e.target.order.value,
		};
		let data = await FieldCtlr.patch_rsc_ins(field_data.id, req_bod);
		console.log('updated field data', data);
        setSuccessComponent(<UpdateFieldSuccess clearMessage={clearMessage}/>)
        setFieldsData(fs_data.map(fd => fd.id == data.id? data: fd));
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

    return {update_field_component, setFieldToUpdate, updating, success_component};
};

const UpdateField = ({old_field_data, handleSubmit, cancelSubmit}) => {
    const [name, setName] = useState(old_field_data.name);
	const [order, setOrder] = useState(old_field_data.order);
    return (
        <div className="update-field">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

				<h2 className="action">Updating Field {old_field_data.id}</h2>

                <label htmlFor="name">Name</label>
                <input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>
                <label htmlFor="order">Order</label>
                <input
					type="number"
					id="order"
					value={order}
                    min="-2147483648"
                    max="2147483648"
					onChange={(e) => setOrder(e.target.value)}
				/>
            </form>
        </div>
    )
}


function UpdateFieldSuccess({clearMessage}) {
    return (
        <div>
            <h4>Field is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

