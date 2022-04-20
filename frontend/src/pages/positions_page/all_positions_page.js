import React, { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../App';
import { CreateIcon, ReadIcon, DeleteIcon, OptionIcon, UpdateIcon, SortIcon } from '../../components/icon';
import { useController } from '../../controllers';
import { useCreatePosition } from '../../custom_hooks/useCreatePosition';
import { useUpdatePosition } from '../../custom_hooks/useUpdatePosition';
import { useDeletePosition } from '../../custom_hooks/useDeletePosition';
import { formatDate } from '../../utils/datetime';
import { useAssignPosition } from '../../custom_hooks/useAssignPosition';
import { useViewPositionHolders } from '../../custom_hooks/useViewPositionHolders';

export const AllPositionsPage = () => {
	const [positions, setPositions] = useState([]);
	const [groups, setGroups] = useState([]);
	const [groups_data, setGroupsData] = useState();
	const [roles, setRoles] = useState([]);
	const [roles_data, setRolesData] = useState();
	const [is_admin, setIsAdmin] = useState(false);
	const [attribute, setAttribute] = useState('name');
	const [search, setSearch] = useState('');
	const [order, setOrder] = useState('id');

	const [positions_length, setPositionsLength] = useState();
	const [limit, setLimit] = useState(50);
	const [number_of_pages, setNumberOfPages] = useState();
	const [current_page, setCurrentPage] = useState(1);

	const { held_positions } = useContext(UserContext);
	const { PositionCtlr, GroupCtlr, RoleCtlr } = useController();

	useEffect(() => {
		if (!held_positions) return;
		if (held_positions.find((hp) => hp.role_id == 1)) setIsAdmin(true);
		else {
			setIsAdmin(false); 
			// console.log("not an admin")
		}
	}, [held_positions]);

	useEffect(() => {
        GroupCtlr.get_rsc_col().then((data) => {
			setGroups(data);
            let groups_data = {}
            for (const group of data) {
                groups_data[group.id] = group;
            }
            // console.log("groups data", groups_data);
            setGroupsData(groups_data);
		});
        RoleCtlr.get_rsc_col().then((data) => {
			setRoles(data);
            let roles_data = {}
            for (const role of data) {
                roles_data[role.id] = role;
            }
            // console.log("roles data", roles_data);
            setRolesData(roles_data);
		});
	}, []);

	useEffect(() => {
		if (search){
			PositionCtlr.get_rsc_col_lth(attribute, search).then((data) => {
				setPositionsLength(data);
			});
		}else{
			PositionCtlr.get_rsc_col_lth().then((data) => {
				setPositionsLength(data);
			});
		}
	}, [search])

	useEffect(() => {
		if (!limit || limit == 0 || !positions_length)return
		setNumberOfPages(Math.ceil(positions_length/(limit)))
		setCurrentPage(1);
	}, [limit, positions_length])

	useEffect(() => {
		if (!limit || limit == 0)return
		let offset = (current_page-1)*limit
		if (search){
			PositionCtlr.get_rsc_col(limit, offset, attribute, search, order).then((data) => {
				setPositions(data);
			});	
		}
		else{
			PositionCtlr.get_rsc_col(limit, offset, null, null, order).then((data) => {
				setPositions(data);
			});
		}
	}, [limit, current_page, search, order])

	const {
		create_position_component,
		creating,
		setCreatePosition,
		success_component: c_r_success_component,
	} = useCreatePosition(setPositions);

	const {
		update_position_component,
		updating,
		setPositionToUpdate,
		success_component: u_r_success_component,
	} = useUpdatePosition(setPositions);

	const {
		delete_position_component,
		deleting,
		setDeletePosition,
		success_component: d_r_success_component
	} = useDeletePosition(setPositions)

	const {
		assign_position_component, 
		assigning, 
		setAssignPosition, 
		success_component: a_p_success_component
	} = useAssignPosition()

	const {
		view_position_holder_component,
		viewing,
		setViewPositionHolder,
	} = useViewPositionHolders();

	useEffect(() => {
		if (creating || updating || deleting || assigning || viewing
             ) {
			document.querySelector('.modal').classList.add('show-modal');
		} else {
			document.querySelector('.modal')?.classList.remove('show-modal'); // first load, component does still not have element with classname 'modal'
		}
	}, [creating, 
        updating, 
        deleting,
		assigning,
		viewing
    ]);

	useEffect(() => {
		if (c_r_success_component || u_r_success_component || d_r_success_component || a_p_success_component) {
			document.querySelector('.success')?.classList.add('show-success');
		} else {
			document
				.querySelector('.success')
				?.classList.remove('show-success');
		}
	}, [c_r_success_component,
         u_r_success_component,
         d_r_success_component,
		 a_p_success_component
        ]);

	return (
		<div className="positions">
			<div className="success">
				{c_r_success_component} 
                {u_r_success_component}
                {d_r_success_component}
				{a_p_success_component}
			</div>
			
			<div className="manage-buttons">
				<button className="option-button">
					<OptionIcon />
				</button>
				<div className="context-menu">
					{is_admin && <div
						className="option"
						onClick={() => setAssignPosition(positions)}
					>
						<button>
							<CreateIcon />
						</button>
						<span>Assign position</span>
					</div>}
					{is_admin && <div
						className="option"
						onClick={() => setCreatePosition(positions, groups, roles)}
					>
						<button>
							<CreateIcon />
						</button>
						<span>Create position</span>
					</div>}
					{is_admin && <div
						className="option"
						onClick={() => setPositionToUpdate(positions, groups, roles)}
					>
						<button>
							<UpdateIcon />
						</button>
						<span>Update position</span>
					</div>}
					{is_admin && <div
						className="option"
						onClick={() => setDeletePosition(positions)}
					>
						<button>
							<DeleteIcon />
						</button>
						<span>Delete position</span>
					</div>}
					<div
						className="option"
						onClick={() => setViewPositionHolder(positions)}
					>
						<button>
							<ReadIcon />
						</button>
						<span>Position's holders</span>
					</div>
				</div>
			</div>
			<div className="pagination">
				<div className="limit">
					<span>Limit</span>
					<input type="number" name="limit" id="limit" min='1' max='100' value={limit} onChange={(e) => setLimit(e.target.value)}/>
				</div>
				<div className="search">
					<span>Search by</span>
					<select name="attribute" id="attribute" value={attribute} onChange={e => setAttribute(e.target.value)}>
						<option value="id">ID</option>
						<option value="name">Name</option>
						<option value="created_at">Time created</option>
						<option value="role_id">Role ID</option>
						<option value="group_id">Group ID</option>
						<option value="creator_id">Creator ID</option>
					</select>
					<input type="text" name="search" id="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder='Enter value...'/>
				</div>
			</div>
			<table>
				<thead>
					<tr>
						<th className='order' onClick={() => setOrder('id')}>
							ID {order === 'id'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('created_at')} >
							Created at {order === 'created_at'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('name')}>
							Name {order === 'name'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('role_id')} >
							Group {order === 'role_id'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('group_id')}>
							Role {order === 'group_id'? <SortIcon/>: null}
						</th>
					</tr>
				</thead>
				<tbody>
					{positions &&
						positions.map((p) => {
							return (
								<tr key={p.id}>
									<td>{p.id}</td>
									<td title={p.created_at}>{formatDate(p.created_at)}</td>
									<td>{p.name}</td>
									<td title={'Role ID: ' + p.role_id}>{roles_data && roles_data[p.role_id]?.name}</td>
									<td title={'Group ID' + p.group_id}>{groups_data && groups_data[p.group_id]?.name}</td>
								</tr>
							);
						})}
				</tbody>
			</table>
			<div className="pagination">
				<div className="page_numbers">
					{number_of_pages && [...Array(number_of_pages).keys()].map(page => {
						return <button key={page} className={current_page==page+1?'current_page page_number':'page_number'} onClick={()=> setCurrentPage(page+1)}>{page+1}</button>
					})}
				</div>
			</div>
			<div className="modal">
				{create_position_component} 
                {update_position_component} 
                {delete_position_component}
				{assign_position_component}
				{view_position_holder_component}
			</div>
		</div>
	);
};
