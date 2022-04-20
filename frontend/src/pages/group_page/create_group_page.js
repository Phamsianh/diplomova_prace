import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useController } from '../../controllers';

export const CreateGroupPage = () => {
    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [phone, setPhone] = useState('');
    const [groups, setGroups] = useState([]);
    const [superior_group_id, setSuperiorGroupId] = useState(1);

    const { GroupCtlr } = useController();
    const navigate = useNavigate();

    useEffect(() => {
        GroupCtlr.get_rsc_col().then(data => {
            setGroups(data);
        })
    }, [])

    async function createGroup(e) {
        e.preventDefault();
        const req_bod = {
            name,
            address,
            phone,
            superior_group_id
        };
        let data = await GroupCtlr.post_rsc(req_bod);
        // console.log(data);
        navigate('/groups')
    }

	return (
		<div className="create-group groups">
			<form onSubmit={createGroup}>
				<label>
					Group name
					<input
						type="text"
						name="name"
						id="name"
						placeholder="Group Name"
						maxLength={100}
						value={name}
						onChange={(e) => setName(e.target.value)}
					/>
				</label>
                <label>
					Address
					<input
						type="text"
						name="address"
						id="address"
						placeholder="Address"
						maxLength={100}
						value={address}
						onChange={(e) => setAddress(e.target.value)}
					/>
				</label>
                <label>
					Phone
					<input
						type="number"
						name="phone"
						id="phone"
						placeholder="Phone"
						maxLength={20}
						value={phone}
						onChange={(e) => setPhone(e.target.value)}
					/>
				</label>
                <label>
					Superior group
					<select name="superior_group_id" id="superior_group_id" onChange={e => setSuperiorGroupId(e.target.value)}>
                        {groups && groups.map(g => {
                            return <option key={g.id} value={g.id}>{g.name}</option>
                        })}
                    </select>
				</label>

                <button type="submit">Create</button>
			</form>
		</div>
	);
};
