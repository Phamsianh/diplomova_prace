import { useState, useEffect, useContext } from 'react';
import { useController } from '../../controllers';
import Tab from '../../components/tab/tab';
import { formatDate } from '../../utils/datetime';
import { CreateIcon, OptionIcon, ReadIcon, SortIcon, UpdateIcon } from '../../components/icon';
import { Link } from 'react-router-dom';
import { useCreateForm } from '../../custom_hooks/useCreateForm';
import { UserContext } from '../../App';

const AllFormsPage = () => {
	const [forms_data, setFormsData] = useState(null);
	const [forms_length, setFormsLength] = useState();
	const [limit, setLimit] = useState(50);
	const [number_of_pages, setNumberOfPages] = useState();
	const [current_page, setCurrentPage] = useState(1);
	const [attribute, setAttribute] = useState('name');
	const [search, setSearch] = useState('');
	const [order, setOrder] = useState('id');

	const {FormCtlr} = useController();
	const {held_positions}	= useContext(UserContext);
	const [is_admin, setIsAdmin] = useState(false)

	useEffect(() => {
		if (search) {
			FormCtlr.get_rsc_col_lth(attribute, search).then((data) => {
				setFormsLength(data);
			});	
		}else {
			FormCtlr.get_rsc_col_lth().then((data) => {
				setFormsLength(data);
			});
		}
	}, [search]);

	useEffect(() => {
		if (!limit || limit == 0 || !forms_length)return
		setNumberOfPages(Math.ceil(forms_length/(limit)))
		setCurrentPage(1);
	}, [limit, forms_length])

	useEffect(() => {
		if (!limit || limit == 0)return
		let offset = (current_page-1)*limit
		if (search){
			FormCtlr.get_rsc_col(limit, offset, attribute, search, order).then((data) => {
				setFormsData(data);
			});	
		}else {
			FormCtlr.get_rsc_col(limit, offset, null, null, order).then((data) => {
				setFormsData(data);
			});
		}
	}, [limit, current_page, search, order])

	useEffect(() => {
		if (!held_positions) return
		if(held_positions.find(hp => hp.role_id == 1)) setIsAdmin(true)
		else setIsAdmin(false)
	}, [held_positions])

	const {create_form_component, setCreateForm, creating, success_component} = useCreateForm(setFormsData);

	useEffect(() => {
		if(creating) {
			document.querySelector(".modal").classList.add("show-modal");
		}
		else {
			document.querySelector(".modal")?.classList.remove("show-modal");
		}
	}, [creating])

	useEffect(() => {
		if(success_component){
			document.querySelector(".success")?.classList.add("show-success")
		}else{
			document.querySelector(".success")?.classList.remove("show-success")
		}
	}, [success_component])

	return (
		<div className="forms">
			<div className="success">
				{success_component}
			</div>
			<div className="error">
			</div>
			<div className="manage-buttons">
				<button className="option-button"><OptionIcon/></button>
				<div className="context-menu">
					{is_admin && <div className="option" onClick={() => setCreateForm(forms_data)}>
						<button><CreateIcon/></button>
						<span>Create new form</span>
					</div>}
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
						<option value="creator_id">Creator ID</option>
						<option value="public">Public</option>
						<option value="obsolete">Obsolete</option>
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
						<th className='order' onClick={() => setOrder('created_at')}>
							Created at {order === 'created_at'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('name')}>
							Name {order === 'name'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('creator_id')}>
							Creator {order === 'creator_id'? <SortIcon/>: null}
						</th>
						<th className='order' onClick={() => setOrder('public')}>
							State {order === 'public'? <SortIcon/>: null}
						</th>
						<th>View</th>
						<th>Update</th>
					</tr>
				</thead>
				<tbody>
					{forms_data && forms_data.map(fd => {
						return <tr key={fd.id}>
							<td>{fd.id}</td>
							<td title={fd.created_at}>{formatDate(fd.created_at)}</td>
							<td>{fd.name}</td>
							<td>{fd.creator_id}</td>
							<td>{!fd.public? 'Private': (fd.obsolete? 'Obsolete': 'Public')}</td>
							<td><Link to={'/forms/' + fd.id}><ReadIcon/></Link></td>
							<td><Link to={'/forms/' + fd.id + '/update'}><UpdateIcon/></Link></td>
						</tr>
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
				{create_form_component}
			</div>
		</div>
	);
};

export default AllFormsPage;
