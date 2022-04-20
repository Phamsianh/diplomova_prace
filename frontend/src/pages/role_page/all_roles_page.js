import React, { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../App';
import { CreateIcon, DeleteIcon, OptionIcon, SortIcon, UpdateIcon } from '../../components/icon';
import { useController } from '../../controllers';
import { useCreateRole } from '../../custom_hooks/useCreateRole';
import { useDeleteRole } from '../../custom_hooks/useDeleteRole';
import { useUpdateRole } from '../../custom_hooks/useUpdateRole';
import { formatDate } from '../../utils/datetime';

export const AllRolesPage = () => {
	const [is_admin, setIsAdmin] = useState(false);
	const [roles, setRoles] = useState([]);
	const [roles_length, setRolesLength] = useState();
	const [limit, setLimit] = useState(50);
	const [number_of_pages, setNumberOfPages] = useState();
	const [current_page, setCurrentPage] = useState(1);
	const [attribute, setAttribute] = useState('name');
	const [search, setSearch] = useState('');
	const [order, setOrder] = useState('id');
	const { held_positions } = useContext(UserContext);
	const { RoleCtlr } = useController();

	useEffect(() => {
		if (!held_positions) return;
		if (held_positions.find((hp) => hp.role_id == 1)) setIsAdmin(true);
		else setIsAdmin(false);
	}, [held_positions]);

	useEffect(() => {
		if(search){
			RoleCtlr.get_rsc_col_lth(attribute, search).then(data => {
				setRolesLength(data);
			})
		}
		else{
			RoleCtlr.get_rsc_col_lth().then(data => {
				setRolesLength(data);
			})
		}
	}, [search])

	useEffect(() => {
		if (!limit || limit == 0 || !roles_length)return
		setNumberOfPages(Math.ceil(roles_length/(limit)))
		setCurrentPage(1);
	}, [limit, roles_length])

	useEffect(() => {
		if (!limit || limit == 0)return
		let offset = (current_page-1)*limit
		console.log(order);
		if(!search){
			RoleCtlr.get_rsc_col(limit, offset, null, null, order).then((data) => {
				setRoles(data);
			});
		}else{
			RoleCtlr.get_rsc_col(limit, offset, attribute, search, order).then((data) => {
				setRoles(data);
			});
		}
	}, [limit, current_page, search, order])

	const {
		create_role_component,
		creating,
		setCreateRole,
		success_component: c_r_success_component,
	} = useCreateRole(setRoles);

	const {
		update_role_component,
		updating,
		setRoleToUpdate,
		success_component: u_r_success_component,
	} = useUpdateRole(setRoles);

	const {
		delete_role_component,
		deleting,
		setDeleteRole,
		success_component: d_r_success_component
	} = useDeleteRole(setRoles)

	useEffect(() => {
		if (creating || updating || deleting) {
			document.querySelector('.modal').classList.add('show-modal');
		} else {
			document.querySelector('.modal')?.classList.remove('show-modal'); // first load, component does still not have element with classname 'modal'
		}
	}, [creating, updating, deleting]);

	useEffect(() => {
		if (c_r_success_component || u_r_success_component || d_r_success_component) {
			document.querySelector('.success')?.classList.add('show-success');
		} else {
			document
				.querySelector('.success')
				?.classList.remove('show-success');
		}
	}, [c_r_success_component, u_r_success_component, d_r_success_component]);

	return (
		<div className="roles">
			<div className="success">
				{c_r_success_component} {u_r_success_component} {d_r_success_component}
			</div>
			{is_admin && (
				<div className="manage-buttons">
					<button className="option-button">
						<OptionIcon />
					</button>
					<div className="context-menu">
						<div
							className="option"
							onClick={() => setCreateRole(roles)}
						>
							<button>
								<CreateIcon />
							</button>
							<span>Create role</span>
						</div>
						<div
							className="option"
							onClick={() => setRoleToUpdate(roles)}
						>
							<button>
								<UpdateIcon />
							</button>
							<span>Update role</span>
						</div>
						<div
							className="option"
							onClick={() => setDeleteRole(roles)}
						>
							<button>
								<DeleteIcon />
							</button>
							<span>Delete role</span>
						</div>
					</div>
				</div>
			)}
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
						<option value="role">Role</option>
						<option value="creator_id">Creator ID</option>
					</select>
					<input type="text" name="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder='Enter value...'/>
				</div>
			</div>
			<table>
				<thead>
					<tr>
						<th className='order' onClick={() => setOrder('id')}>
							ID {order === 'id'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('created_at')}>
							Created at {order === 'created_at'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('name')}>
							Name {order === 'name'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('role')}>
							Role {order === 'role'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('creator_id')}>
							Creator ID {order === 'creator_id'? <SortIcon/>: null}
						</th>
					</tr>
				</thead>
				<tbody>
					{roles &&
						roles.map((r) => {
							return (
								<tr key={r.id}>
									<td>{r.id}</td>
									<td title={r.created_at}>{formatDate(r.created_at)}</td>
									<td>{r.name}</td>
									<td>{r.role}</td>
									<td>{r.creator_id}</td>
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
				{create_role_component}
				{update_role_component}
				{delete_role_component}
			</div>
		</div>
	);
};
