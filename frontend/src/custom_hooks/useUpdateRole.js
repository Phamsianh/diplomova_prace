import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateRole = (setRolesData) => {
    const [updating, setUpdating] = useState(false);
    const [rls_data, setRlsData] = useState();
    const [update_role_component, setUpdateRoleComponent] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { RoleCtlr } = useController();

    function setRoleToUpdate(roles_data) {
        if (updating) return;
        setUpdating(true);
        setRlsData(roles_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateRoleComponent(
                <UpdateRole roles_data={rls_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateRoleComponent(null);
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
			role: e.target.role.value,
		};
		let data = await RoleCtlr.patch_rsc_ins(e.target.selected_role.value, req_bod);
		// console.log('updated role data', data);
        setSuccessComponent(<UpdateRoleSuccess clearMessage={clearMessage}/>)
        setRolesData(rls_data.map(rd => rd.id == data.id? data: rd));
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

    return {update_role_component, setRoleToUpdate, updating, success_component};
};

const UpdateRole = ({roles_data, handleSubmit, cancelSubmit}) => {
    const [old_role_data, setOldRoleData] = useState(roles_data[0]);
    const [name, setName] = useState();
	const [role, setRole] = useState();

    useEffect(() => {
        setName(old_role_data.name);
        setRole(old_role_data.role);
    }, [old_role_data])
    
    return (
        <div className="update-role">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <label htmlFor="selected_role">Select role to update</label>
                {old_role_data && <select name="selected_role" id="selected_role" value={old_role_data.id} onChange={e => setOldRoleData(roles_data.find(gd => gd.id == e.target.value))}>
                    { roles_data.map(rd => {
                        return <option key={rd.id} value={rd.id}>{rd.name} - {rd.id}</option>
                    })}
                </select>}

				<h2 className="action">Updating Role {old_role_data.name} - {old_role_data.id}</h2>

                <label htmlFor="name">Name</label>
                {name && <input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>}

                <label htmlFor="role">Role</label>
                {role && <select name="role" id="role" value={role} onChange={e => setRole(e.target.value)}>
                    <option value="admin">Admin</option>
                    <option value="handler">Handler</option>
                    <option value="applicant">Applicant</option>
                </select>}
            </form>
        </div>
    )
}


function UpdateRoleSuccess({clearMessage}) {
    return (
        <div>
            <h4>Role is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

