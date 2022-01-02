import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../../../App';
import { useController } from '../../../controllers';
import { InstanceContentContext } from '../../../pages/instance_page/read_instance_page';
import { HandleInstanceIcon } from '../../icon';

export const HandleInstance = ({ instance_data, setInstanceData, setIsHandling }) => {
	const { held_positions } = useContext(UserContext);
    const { setContentData } = useContext(InstanceContentContext)
	const { InstanceCtlr } = useController();

	const [filtered_cur_rmn_psts, setFilteredCurRmnPsts] = useState();
    const [select_all, setSelectAll] = useState(false)

	useEffect(() => {
		InstanceCtlr.get_rel_rsc(
			instance_data.id,
			'current_remaining_positions'
		).then((data) => {
			// setCurrentRemainingPositions(data);
			setFilteredCurRmnPsts(
				data.filter((crp) => {
					return held_positions.find((hp) => hp.id === crp.id);
				})
			);
            console.log('current remaining positions', data);
		});
	}, []);

	function handleInstance(e) {
        let req_bod = {}
		e.preventDefault();
        if (e.target.select_all.checked){
            req_bod = {
                instance_handle_request: {
                    handle: true,
                }
            }
        }else{
            req_bod = {
                instance_handle_request: {
                    handle: true,
                    handled_positions_id: filtered_cur_rmn_psts.filter(fcrp => {
                        return e.target['position_'+ fcrp.id].checked
                    }).map(fcrp => fcrp.id),
                },
            };
        }
        InstanceCtlr.patch_rsc_ins(instance_data.id, req_bod).then(data =>{
            setIsHandling(false)
            
            // update instance_data and content_data in InstanceContentContext will effect rerender ReadFieldContent and UpdateFieldContent
            setInstanceData(data)
            InstanceCtlr.get_rel_rsc(instance_data.id, 'instances_fields').then(data => {
                setContentData(data)
            })
        })
	}

    function handleSelectAll(e) {
        setSelectAll(!select_all)
        let checkboxes = document.getElementsByName('handle_positions_id')
        for (let checkbox of checkboxes) {
            checkbox.checked = e.target.checked;
        }
    }

	return (
		<div className="update-instance handle-instance">
			<form onSubmit={handleInstance}>
				<label>
					<fieldset>
                        <label>
                            <input
                                type="checkbox"
                                id="select_all"
                                name="handle_positions_id" 
                                value={'select_all'}
                                onChange={handleSelectAll}
                                checked={select_all}
                            />
                            Select All
                        </label><br />
						{filtered_cur_rmn_psts &&
							filtered_cur_rmn_psts.map((fcrp) => {
								return (
                                    <label key={fcrp.id}>
                                        <input
                                            type="checkbox"
                                            name="handle_positions_id"
                                            value={fcrp.id}
                                            id={'position_' + fcrp.id}
                                            onChange={() => setSelectAll(false)}
                                        />
                                        {fcrp.name}
                                        <br />
                                    </label>
								);
							})}
					</fieldset>
					<button type="submit" title="Handle Instance">
						<HandleInstanceIcon />
					</button>
				</label>
			</form>
		</div>
	);
};
