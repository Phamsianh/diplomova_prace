import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreatePosition = (setPositionsData) => {
    const [creating, setCreating] = useState(false);
    const [psts_data, setPstsData] = useState();
    const [groups_data, setGroupsData] = useState();
    const [roles_data, setRolesData] = useState();

    const [create_position_component, setCreatePositionComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const {PositionCtlr} = useController();

    function setCreatePosition(positions_data, groups_data, roles_data) {
        setCreating(true);
        setPstsData(positions_data);
        setGroupsData(groups_data);
        setRolesData(roles_data);
    }

    useEffect(() => {
        if (creating) {
            setCreatePositionComponent(
                <CreatePosition
                groups_data={groups_data}
                roles_data={roles_data}
                handleSubmit={handleSubmit}
                cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreatePositionComponent(null);
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
			group_id: e.target.group_id.value = 0 ? e.target.group_id.value: null,
			role_id: e.target.role_id.value,
		};
        const data = await PositionCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreatePositionSuccess clearMessage={clearMessage}/>)
        setPositionsData([...psts_data, data])
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

  return {create_position_component, setCreatePosition, creating, success_component};
};


const CreatePosition = ({
    groups_data,
    roles_data,
    handleSubmit, 
    cancelSubmit
}) => {
    const [name, setName] = useState('New Position');
	const [group_id, setGroupId] = useState();
	const [role_id, setRoleId] = useState();

    useEffect(() => {
        setGroupId(groups_data[0].id)
        setRoleId(roles_data[0].id)
    }, [])
	return (
        <div className="create-position">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h4>{name?name:'New Position'}</h4>

                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <label htmlFor="group_id">Group</label>
                {group_id && <select name="group_id" id="group_id" value={group_id} onChange={(e) => setGroupId(e.target.value)}>
                    <option value="0">None</option>
                    {groups_data.map(gd => {
                        return <option key={gd.id} value={gd.id}>{gd.name} - {gd.id}</option>
                    })}
                </select>}

                <label htmlFor="role_id">Group</label>
                {role_id && <select name="role_id" id="role_id" value={role_id} onChange={(e) => setGroupId(e.target.value)}>
                    {roles_data.map(rd => {
                        return <option key={rd.id} value={rd.id}>{rd.name} - {rd.id}</option>
                    })}
                </select>}

            </form>
        </div>
	);
}

function CreatePositionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Position is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}