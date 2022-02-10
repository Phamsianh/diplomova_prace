import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateInstanceField = (setInstancesFieldsData) => {
    const [instance_field_data, setInstanceFieldData] = useState();
    const [ifs_data, setIFsData ] = useState();
    const [update_instance_field_component, setUpdateInstanceFieldComponent ] = useState();
    const {InstanceCtlr} = useController();

    function setUpdateInstanceField(instance_field_data, instances_fields_data) {
        // setInstanceFieldData(instance_field_data);
        // setIFsData(instances_fields_data);
        setUpdateInstanceFieldComponent(
            <UpdateInstanceField old_instance_field_data={instance_field_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
        )
    }


    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
            value: e.target.value.value
        }
        const data = await InstanceCtlr.patch_rsc_ins(instance_field_data.id, req_bod);
        setInstancesFieldsData(ifs_data.map(ifsd => ifsd.id == data.id ? data: ifsd))
    }

    function cancelSubmit(e) {
        e.preventDefault();
    }

    return {update_instance_field_component, setUpdateInstanceField}
};

function UpdateInstanceField ({old_instance_field_data, instances_fields_data, setInstancesFieldsData}) {
    const [value, setValue] = useState(old_instance_field_data.value)
    const {InstanceCtlr} = useController();

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
            value: e.target.value.value
        }
        const data = await InstanceCtlr.patch_rsc_ins(old_instance_field_data.id, req_bod);
        setInstancesFieldsData(instances_fields_data.map(ifsd => ifsd.id == data.id ? data: ifsd))
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setValue(old_instance_field_data.value);
    }

    return (
        <div className="instance-field">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit" onSubmit={handleSubmit}><SaveIcon/></button>
                    <button onClick={cancelSubmit}></button>
                </div>
                <input type="text" name="value" value={value} onChange={e => {
                    setValue(e.target.value);

                }}/>
            </form>
        </div>
    )
}