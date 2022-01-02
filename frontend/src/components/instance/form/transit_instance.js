import { useEffect, useState  } from 'react';
import { SaveIcon } from '../../icon';
import { useController } from '../../../controllers';

export const TransitInstance = ({
	old_instance_data,
	handleUpdateInstance,
}) => {
	const [next_phases, setNextPhases] = useState();
	const {PhaseCtlr} = useController();
	
    useEffect(() => {
        PhaseCtlr.get_rel_rsc(old_instance_data.current_phase_id, 'next_phases').then(data => {
            setNextPhases(data)
            console.log('next phases data', data);
        })
    }, [])
	return (
		<div className="update-instance transit-instance">
			<form onSubmit={handleUpdateInstance}>
				<label>
					Next Phase
					<select name="current_phase_id" id="current_phase_id">
						{next_phases && next_phases.map((fpd) => {
							return <option key={fpd.id} value={fpd.id}>{fpd.name}</option>;
						})}
					</select>
					<button type="submit" title="Update">
						<SaveIcon />
					</button>
				</label>
			</form>
		</div>
	);
};
