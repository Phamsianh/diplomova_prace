import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon, DeleteIcon } from '../components/icon';

export const useDeleteRole = (setRolesData) => {
    const [rls_data, setRlsData] = useState();
    const [delete_role_component, setDeleteRoleComponent] = useState();
    const [deleting, setDeleting] = useState(false);
    const [success_component, setSuccessComponent] = useState();
    
    const { RoleCtlr } = useController();

    function setDeleteRole(roles_data) {
        setDeleting(true);
        setRlsData(roles_data);
    }

    useEffect (() => {
        if (deleting) {
            setDeleteRoleComponent(
                <DeleteRole roles_data={rls_data} handleDelete={deleteRole} cancelDelete={cancelDelete} />
            )
        }
        else{
            setDeleteRoleComponent(null);
        }
    }, [deleting])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function deleteRole(e) {
        e.preventDefault();
        let selected_role_id = e.target.selected_role_id.value
		let data = await RoleCtlr.delete_rsc_ins(selected_role_id);
        // console.log(data);
        if (data == null) {
            setDeleting(false)
            setSuccessComponent(<DeleteRoleSuccess clearMessage={clearMessage}/>)
            setRolesData(rls_data.filter(rd => rd.id != selected_role_id))
            
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
    
    return {delete_role_component, deleting, setDeleteRole, success_component};
};

function DeleteRole({roles_data, handleDelete, cancelDelete}) {
    const [selected_role_id, setSelectedRoleId] = useState();
    useEffect(() => {
        setSelectedRoleId(roles_data[0].id)
    }, [])
    return <div className="delete-role">
        <form onSubmit={handleDelete}>
            <div className="manage-buttons">
                <button type="submit"><DeleteIcon/></button>
                <button onClick={cancelDelete}><CancelIcon/></button>
            </div>

            {selected_role_id && <select name="selected_role_id" id="selected_role_id" value={selected_role_id} onChange={ e => setSelectedRoleId(e.target.value) }>
                {roles_data.map(rd => {
                    return <option key={rd.id} value={rd.id}>{rd.name} - {rd.id}</option>
                })}
            </select>}
        </form>
    </div>
}

function DeleteRoleSuccess({clearMessage}) {
    return (
        <div>
            <h4>Role is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}