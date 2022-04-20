import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon, DeleteIcon } from '../components/icon';

export const useDeleteGroup = (setGroupsData) => {
    const [grps_data, setGrpsData] = useState();
    const [delete_group_component, setDeleteGroupComponent] = useState();
    const [deleting, setDeleting] = useState(false);
    const [success_component, setSuccessComponent] = useState();
    
    const { GroupCtlr } = useController();

    function setDeleteGroup(groups_data) {
        setDeleting(true);
        setGrpsData(groups_data);
    }

    useEffect (() => {
        if (deleting) {
            setDeleteGroupComponent(
                <DeleteGroup groups_data={grps_data} handleDelete={deleteGroup} cancelDelete={cancelDelete} />
            )
        }
        else{
            setDeleteGroupComponent(null);
        }
    }, [deleting])
    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    
    async function deleteGroup(e) {
        e.preventDefault();
        let selected_group_id = e.target.selected_group_id.value
		let data = await GroupCtlr.delete_rsc_ins(selected_group_id);
        // console.log(data);
        if (data == null) {
            setDeleting(false)
            setSuccessComponent(<DeleteGroupSuccess clearMessage={clearMessage}/>)
            setGroupsData(grps_data.filter(fd => fd.id != selected_group_id))
            
        }
    }

    function cancelDelete(e) {
        e.preventDefault();
        setDeleting(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }
    
    return {delete_group_component, deleting, setDeleteGroup, success_component};
};

function DeleteGroup({groups_data, handleDelete, cancelDelete}) {
    const [selected_group_id, setSelectedGroupId] = useState();
    useEffect(() => {
        setSelectedGroupId(groups_data[0].id)
    }, [])
    return <div className="delete-group">
        <form onSubmit={handleDelete}>
            <div className="manage-buttons">
                <button type="submit"><DeleteIcon/></button>
                <button onClick={cancelDelete}><CancelIcon/></button>
            </div>

            {selected_group_id && <select name="selected_group_id" id="selected_group_id" value={selected_group_id} onChange={ e => setSelectedGroupId(e.target.value) }>
                {groups_data.map(gd => {
                    return <option value={gd.id}>{gd.name} - {gd.id}</option>
                })}
            </select>}
        </form>
    </div>
}

function DeleteGroupSuccess({clearMessage}) {
    return (
        <div>
            <h4>Group is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}