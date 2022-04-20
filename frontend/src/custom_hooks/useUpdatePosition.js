import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdatePosition = (setPositionsData) => {
    const [updating, setUpdating] = useState(false);
    const [psts_data, setPstsData] = useState();
    const [groups_data, setGroupsData] = useState();
    const [roles_data, setRolesData] = useState();
    const [update_position_component, setUpdatePositionComponent] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { PositionCtlr } = useController();

    function setPositionToUpdate(positions_data, groups_data, roles_data) {
        if (updating) return;
        setUpdating(true);
        setPstsData(positions_data);
        setGroupsData(groups_data);
        setRolesData(roles_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdatePositionComponent(
                <UpdatePosition
                positions_data={psts_data} 
                groups_data={groups_data}
                roles_data={roles_data}
                handleSubmit={handleSubmit} 
                cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdatePositionComponent(null);
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
			group_id: e.target.group_id.value = 0 ? e.target.group_id.value: null,
			role_id: e.target.role_id.value,
		};
		let data = await PositionCtlr.patch_rsc_ins(e.target.selected_position.value, req_bod);
		// console.log('updated position data', data);
        setSuccessComponent(<UpdatePositionSuccess clearMessage={clearMessage}/>)
        setPositionsData(psts_data.map(pd => pd.id == data.id? data: pd));
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

    return {update_position_component, setPositionToUpdate, updating, success_component};
};

const UpdatePosition = ({
    positions_data,
    groups_data,
    roles_data,
    handleSubmit, 
    cancelSubmit
}) => {
    const [old_position_data, setOldPositionData] = useState(positions_data[0]);
    const [name, setName] = useState();
    const [group_id, setGroupId] = useState();
	const [role_id, setRoleId] = useState();

    useEffect(() => {
        setName(old_position_data.name);
        setGroupId(old_position_data.group_id);
        setRoleId(old_position_data.role_id);
    }, [old_position_data])
    
    return (
        <div className="update-position">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <label htmlFor="selected_position">Select position to update</label>
                {old_position_data && <select name="selected_position" id="selected_position" value={old_position_data.id} onChange={e => setOldPositionData(positions_data.find(gd => gd.id == e.target.value))}>
                    { positions_data.map(gd => {
                        return <option key={gd.id} value={gd.id}>{gd.name} - {gd.id}</option>
                    })}
                </select>}

				<h2 className="action">Updating Position {old_position_data.name} - {old_position_data.id}</h2>

                <label htmlFor="name">Name</label>
                {name && <input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>}

                <label htmlFor="group_id">Group</label>
                {group_id && <select name="group_id" id="group_id" value={group_id} onChange={(e) => setGroupId(e.target.value)}>
                    <option value="0">None</option>
                    {groups_data.map(gd => {
                        return <option key={gd.id} value={gd.id}>{gd.name} - {gd.id}</option>
                    })}
                </select>}

                <label htmlFor="role_id">Role</label>
                {role_id && <select name="role_id" id="role_id" value={role_id} onChange={(e) => setGroupId(e.target.value)}>
                    {roles_data.map(rd => {
                        return <option key={rd.id} value={rd.id}>{rd.name} - {rd.id}</option>
                    })}
                </select>}
            </form>
        </div>
    )
}


function UpdatePositionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Position is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

