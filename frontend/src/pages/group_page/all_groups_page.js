import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../App';
import { CreateIcon, DeleteIcon, OptionIcon, ReadIcon, UpdateIcon } from '../../components/icon';

import { useCreateGroup } from '../../custom_hooks/useCreateGroup';
import { useReadGroupDetail } from '../../custom_hooks/useReadGroupDetail';
import { useReadGroupPage } from '../../custom_hooks/useReadGroupPage';
import { useUpdateGroup } from '../../custom_hooks/useUpdateGroup';
import { useDeleteGroup } from '../../custom_hooks/useDeleteGroup';

export const AllGroupsPage = () => {
	const [is_admin, setIsAdmin] = useState(false);
	const { held_positions } = useContext(UserContext);
	useEffect(() => {
		if (!held_positions) return;
		if (held_positions.find((hp) => hp.role_id == 1)) setIsAdmin(true);
		else setIsAdmin(false);
	}, [held_positions]);

	const {
		groups_data, 
		setGroupsData, 
	} = useReadGroupPage();
	const {read_group_detail_component, setReadGroupDetail, reading} = useReadGroupDetail()
	const {create_group_component, setCreateGroup, creating, success_component: c_g_success_component, error_component: c_g_error_component} = useCreateGroup(setGroupsData);
	const {update_group_component, setGroupToUpdate, updating, success_component: u_g_success_component} = useUpdateGroup(setGroupsData)
	const {delete_group_component, deleting, setDeleteGroup, success_component: d_g_success_component} = useDeleteGroup(setGroupsData)

	useEffect(() => {
		if(reading || creating || updating || deleting) {
			document.querySelector(".modal").classList.add("show-modal");
		}
		else {
			document.querySelector(".modal")?.classList.remove("show-modal");
		}
	}, [reading, creating, updating, deleting])

	useEffect(() => {
		if(c_g_success_component || u_g_success_component || d_g_success_component){
			document.querySelector(".success")?.classList.add("show-success")
		}else{
			document.querySelector(".success")?.classList.remove("show-success")
		}
	}, [c_g_success_component, u_g_success_component, d_g_success_component])

	useEffect(() => {
		if(c_g_error_component ){
			document.querySelector(".error")?.classList.add("show-error")
		}else{
			document.querySelector(".error")?.classList.remove("show-error")
		}
	}, [c_g_error_component])

	return (
		<div className="groups">
			<div className="success">
				{c_g_success_component}
				{u_g_success_component}
				{d_g_success_component}
			</div>
			<div className="error">
				{c_g_error_component}
			</div>
			<div className="manage-buttons">
				<button className="option-button"><OptionIcon/></button>
				<div className="context-menu">
					<div className="option" onClick={() => setReadGroupDetail(groups_data)}>
						<button><ReadIcon/></button>
						<span>Read group's detail</span>
					</div>
					{is_admin && <div className="option" onClick={() => setCreateGroup(groups_data)}>
						<button><CreateIcon/></button>
						<span>Create group</span>
					</div>}
					{is_admin &&
					<div className="option" onClick={() => setGroupToUpdate(groups_data)}>
						<button><UpdateIcon/></button>
						<span>Update group</span>
					</div>}
					{is_admin &&
					<div className="option" onClick={() => setDeleteGroup(groups_data)}>
						<button><DeleteIcon/></button>
						<span>Delete group</span>
					</div>}
				</div>
			</div>
      		<div id="groups-cy"></div>
			<div className="modal">
				{read_group_detail_component}
				{create_group_component}
				{update_group_component}
				{delete_group_component}
			</div>
		</div>
	);
};
