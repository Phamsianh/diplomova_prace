import React, { useEffect, useState } from 'react'
import { CancelIcon } from '../components/icon';
import { useController } from '../controllers';

export const useReadGroupDetail = () => {
    const [grps_data, setGrpsData] = useState();
    const [read_group_detail_component, setGroupDetailComponent] = useState();
    const [reading, setReading] = useState(false);

    function setReadGroupDetail(groups_data) {
        setReading(true)
        // console.log(groups_data);
        setGrpsData(groups_data)
    }

    useEffect(() => {
        if(reading) {
            setGroupDetailComponent(
                <ReadGroupDetail groups_data={grps_data} cancelReading={cancelReading}/>
            )
        }
        else {
            setGroupDetailComponent(null)
        }
    }, [reading])

	function cancelReading(e) {
		e.preventDefault();
		setReading(false);
	}

  return {read_group_detail_component, setReadGroupDetail, reading}
}


function ReadGroupDetail({
    groups_data,
    cancelReading
}) {
    const [selected_group, setSelectedGroup] = useState(groups_data[0])
    const [positions, setPositions] = useState()
    const [subordinate_groups, setSubordinateGroups] = useState()
    const [roles, setRoles] = useState()
    const [joiners, setJoiners] = useState()
    
    const {GroupCtlr} = useController()

    useEffect(() => {
        if (!selected_group?.id) return
        GroupCtlr.get_rel_rsc(selected_group.id, "positions").then(data => {
            // console.log("positions data", data);
            setPositions(data)
        })
        GroupCtlr.get_rel_rsc(selected_group.id, "subordinate_groups").then(data => {
            // console.log("subordinate groups data", data);
            setSubordinateGroups(data)
        })
        GroupCtlr.get_rel_rsc(selected_group.id, "roles").then(data => {
            // console.log("roles data", data);
            setRoles(data)
        })
        // GroupCtlr.get_rel_rsc(selected_group.id, "joiners").then(data => {
        //     // console.log("joiners data", data);
        //     setJoiners(data)
        // })
    }, [selected_group?.id])
    return <div className="read-group-detail">
        <div className="manage-buttons">
        <button onClick={(e) => {
					cancelReading(e);
				}}><CancelIcon/></button>
        </div>
        <h2>Select group</h2>
        <select name="selected_group" id="selected_group" value={selected_group.id} onChange={e => setSelectedGroup(groups_data.find(gd => gd.id == e.target.value))}>
            {groups_data.map(gd => {
                return <option key={gd.id} value={gd.id}>{gd.name} - {gd.id}</option>
            })}
        </select>
        
        {selected_group && <div className="group-detail">
            <p>Address: {selected_group.address}</p>
            <p>Phone: {selected_group.phone}</p>
            <p>Superior group: {groups_data.find(gd => gd.id == selected_group.superior_group_id)?.name}</p>
            
            <br /><hr /><br />
            <h3>Subordinate groups</h3>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Address</th>
                    </tr>
                </thead>
                <tbody>
                    {subordinate_groups && subordinate_groups.map(sg => {
                        return <tr key={sg.id}>
                            <td>{sg.name}</td>
                            <td>{sg.phone}</td>
                            <td>{sg.address}</td>
                        </tr>
                    })}
                </tbody>
            </table>

            <br /><hr /><br />
            <h3>Positions</h3>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Role name</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    {positions && roles && positions.map(p => {
                        return <tr key={p.id}>
                            <td>{p.name}</td>
                            <td>{roles.find(r => r.id == p.role_id)?.name}</td>
                            <td>{roles.find(r => r.id == p.role_id)?.role}</td>
                        </tr>
                    })}
                </tbody>
            </table>
        </div>}

    </div>
}