import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreateRole = (setRolesData) => {
    const [creating, setCreating] = useState(false);
    const [rls_data, setRlsData] = useState();
    const [create_role_component, setCreateRoleComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const {RoleCtlr} = useController();

    function setCreateRole(roles_data) {
        setCreating(true);
        setRlsData(roles_data);
    }

    useEffect(() => {
        if (creating) {
            setCreateRoleComponent(
                <CreateRole handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreateRoleComponent(null);
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
			role: e.target.role.value,
		};
        const data = await RoleCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreateRoleSuccess clearMessage={clearMessage}/>)
        setRolesData([...rls_data, data])
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

  return {create_role_component, setCreateRole, creating, success_component};
};


const CreateRole = ({handleSubmit, cancelSubmit}) => {
    const [name, setName] = useState('New Role');
	const [role, setRole] = useState();
	return (
        <div className="create-role">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h4>{name?name:'New Role'}</h4>

                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <label htmlFor="role">Role</label>
                <select name="role" id="role" value={role} onChange={(e) => setRole(e.target.value)}>
                    <option value="admin">Admin</option>
                    <option value="handler">Handler</option>
                    <option value="applicant">Applicant</option>
                </select>
            </form>
        </div>
	);
}

function CreateRoleSuccess({clearMessage}) {
    return (
        <div>
            <h4>Role is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}