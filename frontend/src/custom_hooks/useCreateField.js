import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreateField = (setFieldsData) => {
    const [creating, setCreating] = useState(false);
    const [fds_data, setFdsData] = useState();
    const [section_data, setSectionData] = useState();
    const [create_field_component, setCreateFieldComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const {FieldCtlr} = useController();

    function setCreateField(section_data, fields_data) {
        setCreating(true);
        setSectionData(section_data)
        setFdsData(fields_data);
    }

    useEffect(() => {
        if (creating) {
            let fields_data = fds_data.filter(f => f.section_id == section_data.id)
            setCreateFieldComponent(
                <CreateField fields_data={fields_data} section handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreateFieldComponent(null);
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
			section_id: section_data.id,
			order: e.target.order.value,
		};
        const data = await FieldCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreateFieldSuccess clearMessage={clearMessage}/>)
        setFieldsData([...fds_data, data])
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

  return {create_field_component, setCreateField, creating, success_component};
};


const CreateField = ({fields_data, handleSubmit, cancelSubmit}) => {
    const [name, setName] = useState('New Field');
	const [order, setOrder] = useState(fields_data.length + 1);
	return (
        <div className="create-field">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h4>{name?name:'New Field'}</h4>

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
	);
}

function CreateFieldSuccess({clearMessage}) {
    return (
        <div>
            <h4>Field is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}