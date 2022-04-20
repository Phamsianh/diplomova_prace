import React, { useContext } from 'react';
import Tab from '../../components/tab/tab';
import { useState, useEffect } from 'react';
import { useController } from '../../controllers';
import { UserContext } from '../../App';
import { useNavigate } from 'react-router-dom';

const AllInstancesPage = () => {
	const [instances_data, setInstancesData] = useState(null);
	const [is_admin, setIsAdmin] = useState();
	const [limit, setLimit] = useState(50);
	const [number_of_pages, setNumberOfPages] = useState();
	const [current_page, setCurrentPage] = useState(1);
	const [attribute, setAttribute] = useState('id');
	const [search, setSearch] = useState('');
	const [instances_length, setInstancesLength] = useState();
	const { held_positions } = useContext(UserContext);
	const { InstanceCtlr} = useController();
	const navigate = useNavigate();

	useEffect(() => {
		if (!held_positions) return;
		if (held_positions.find((hp) => hp.role_id == 1)) setIsAdmin(true);
		else setIsAdmin(false);
	}, [held_positions]);

	useEffect(() => {
		if (is_admin === undefined) return
		if (!is_admin) navigate('/me/instances')
	}, [is_admin])

    useEffect(() => {
		InstanceCtlr.get_rsc_col().then((data) => {
			setInstancesData(data);
		})
	}, []);

	useEffect(() => {
		if(search){
			InstanceCtlr.get_rsc_col_lth(attribute, search).then(data => {
				setInstancesLength(data);
			})
		}
		else{
			InstanceCtlr.get_rsc_col_lth().then(data => {
				setInstancesLength(data);
			})
		}
	}, [search])

	useEffect(() => {
		if (!limit || limit == 0 || !instances_length)return
		setNumberOfPages(Math.ceil(instances_length/(limit)))
		setCurrentPage(1);
	}, [limit, instances_length])

	useEffect(() => {
		if (!limit || limit == 0)return
		let offset = (current_page-1)*limit
		if(!search){
			InstanceCtlr.get_rsc_col(limit, offset).then((data) => {
				setInstancesData(data);
			});
		}else{
			InstanceCtlr.get_rsc_col(limit, offset, attribute, search).then((data) => {
				setInstancesData(data);
			});
		}
	}, [limit, current_page, search])


	return (
		<div>
			<div className="pagination">
				<div className="limit">
					<span>Limit</span>
					<input type="number" name="limit" id="limit" min='1' max='100' value={limit} onChange={(e) => setLimit(e.target.value)}/>
				</div>
				<div className="search">
					<span>Search: </span>
					<select name="attribute" id="attribute" value={attribute} onChange={e => setAttribute(e.target.value)}>
						<option value="id">ID</option>
						<option value="form_id">Form ID</option>
						<option value="created_at">Time created</option>
						<option value="updated_at">Time last update</option>
						<option value="current_phase_id">Current Phase ID</option>
						<option value="creator_id">Creator ID</option>
					</select>
					<input type="text" name="search" id="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder='Enter value'/>
				</div>
			</div>
			<Tab
				// name="All instances"
				overview_data={instances_data}
				title="Instance"
				rsc_name="instances"
			></Tab>
			<div className="pagination">
				<div className="page_numbers">
					{number_of_pages && [...Array(number_of_pages).keys()].map(page => {
						return <button key={page} className={current_page==page+1?'current_page page_number':'page_number'} onClick={()=> setCurrentPage(page+1)}>{page+1}</button>
					})}
				</div>
			</div>
		</div>
	);
};

export default AllInstancesPage;
