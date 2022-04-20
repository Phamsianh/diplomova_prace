import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateGroup = (setGroupsData) => {
    const [updating, setUpdating] = useState(false);
    const [grps_data, setGrpsData] = useState();
    const [update_group_component, setUpdateGroupComponent] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { GroupCtlr } = useController();

    function setGroupToUpdate(groups_data) {
        if (updating) return;
        setUpdating(true);
        setGrpsData(groups_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateGroupComponent(
                <UpdateGroup groups_data={grps_data} handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateGroupComponent(null);
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
            address: e.target.address.value,
			phone: e.target.phone.value? e.target.phone.value: null,
			superior_group_id: e.target.superior_group_id.value,
		};
		let data = await GroupCtlr.patch_rsc_ins(e.target.selected_group.value, req_bod);
		// console.log('updated group data', data);
        setSuccessComponent(<UpdateGroupSuccess clearMessage={clearMessage}/>)
        setGroupsData(grps_data.map(gd => gd.id == data.id? data: gd));
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

    return {update_group_component, setGroupToUpdate, updating, success_component};
};

const UpdateGroup = ({groups_data, handleSubmit, cancelSubmit}) => {
    const [old_group_data, setOldGroupData] = useState(groups_data[0]);
    const [name, setName] = useState();
	const [address, setAddress] = useState();
	const [phone, setPhone] = useState();
	const [superior_group_id, setSuperiorGroupId] = useState();

    useEffect(() => {
        setName(old_group_data.name);
        setAddress(old_group_data.address);
        setPhone(old_group_data.phone);
        setSuperiorGroupId(old_group_data.superior_group_id);
    }, [old_group_data])
    
    return (
        <div className="update-group">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <label htmlFor="selected_group">Select group to update</label>
                {old_group_data && <select name="selected_group" id="selected_group" value={old_group_data.id} onChange={e => setOldGroupData(groups_data.find(gd => gd.id == e.target.value))}>
                    { groups_data.map(gd => {
                        return <option key={gd.id} value={gd.id}>{gd.name} - {gd.id}</option>
                    })}
                </select>}

				<h2 className="action">Updating Group {old_group_data.name} - {old_group_data.id}</h2>

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
                    <option value={0}>None</option>
                    {groups_data && groups_data.map(gd => {
                        if(gd.id != old_group_data.id) return <option key={gd.id} value={gd.id}>{gd.name}</option>
                    })}
                </select>
            </form>
        </div>
    )
}


function UpdateGroupSuccess({clearMessage}) {
    return (
        <div>
            <h4>Group is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

