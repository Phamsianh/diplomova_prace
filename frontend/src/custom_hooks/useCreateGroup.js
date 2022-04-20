import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';
import { convert_groups, displayGroups } from '../utils/cy';
import { toTitleCase } from '../utils/to_title_case';

export const useCreateGroup = (setGroupsData) => {
    const [creating, setCreating] = useState(false);
    const [grps_data, setGrpsData] = useState();
    const [create_group_component, setCreateGroupComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();
    const [error_component, setErrorComponent] = useState();

    const {GroupCtlr} = useController();

    function setCreateGroup(groups_data) {
        setCreating(true);
        setGrpsData(groups_data);
    }

    useEffect(() => {
        if (creating) {
            setCreateGroupComponent(
                <CreateGroup groups_data={grps_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreateGroupComponent(null);
        }
    }, [creating])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    useEffect(() => {
        if(!error_component) return
        setTimeout(() => {
            setErrorComponent(null);
        }, 3000)
    }, [error_component])

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
			name: e.target.name.value,
			address: e.target.address.value,
			phone: e.target.phone.value? e.target.phone.value: null,
			superior_group_id: e.target.superior_group_id.value != 0? e.target.superior_group_id.value: null,
		};
        try {
            const data = await GroupCtlr.post_rsc(req_bod);
            setSuccessComponent(<CreateGroupSuccess clearMessage={clearMessage}/>)
            const new_groups_data = [...grps_data, data]
            setGroupsData(new_groups_data)
            setCreating(false);
        } catch (error) {
            setCreating(false);
            // Find way to handle the error
            setErrorComponent(<CreateGroupError detail="Fail to create group" clearMessage={clearErrorMessage}/>)
        }

    }

    function cancelSubmit(e) {
        e.preventDefault();
        setCreating(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    function clearErrorMessage(e) {
        e.preventDefault();
        setErrorComponent(null)
    }

  return {create_group_component, setCreateGroup, creating, success_component, error_component};
};


const CreateGroup = ({groups_data, handleSubmit, cancelSubmit}) => {
    const [name, setName] = useState('New Group');
	const [address, setAddress] = useState('');
    const [phone, setPhone] = useState('');
    const [superior_group_id, setSuperiorGroupId] = useState();
	return (
        <div className="create-group">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h4>{name?name:'New Group'}</h4>

                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <label htmlFor="address">Address</label>
                <input
                    type="text"
                    id="address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                />
                <label htmlFor="phone">Phone</label>
                <input
                    type="number"
                    id="phone"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                />
                <label htmlFor="superior_group_id">Superior group</label>
                <select name="superior_group_id" id="superior_group_id" value={superior_group_id} onChange={e => setSuperiorGroupId(e.target.value)}>
                    <option value="0">None</option>
                    {groups_data && groups_data.map(gd => {
                        return <option key={gd.id} value={gd.id}>{gd.name}</option>
                    })}
                </select>
                
            </form>
        </div>
	);
}

function CreateGroupSuccess({clearMessage}) {
    return (
        <div>
            <h4>Group is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

function CreateGroupError({detail, clearMessage}) {
    return (
        <div>
            <h4>{toTitleCase(detail)}</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}