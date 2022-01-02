import { useState, useEffect, useContext } from 'react';
import { SaveIcon } from '../icon';
import { PhasesData } from '../form/read_form_phases';

export const UpdateTransition = ({ 
    old_transition_data,
    handleUpdateTransition,
	from_phase_id
}) => {
	const phases_data = useContext(PhasesData);
	const [name, setName] = useState(old_transition_data.name);
	const [to_phase_id, setToPhaseId] = useState(old_transition_data.to_phase_id);
	const [filtered_phases_data, setFiltered_phases_data] = useState()

	useEffect(() => {
		setFiltered_phases_data(phases_data.filter(pd => {
			return pd.id !== from_phase_id
		}))
	}, [phases_data])

	return (
		<div className="update-transition">
			<form onSubmit={handleUpdateTransition}>
				<label>
					Name
					<input
						id="name"
						type="text"
						value={name}
						placeholder="Transition Name"
						onChange={(e) => setName(e.target.value)}
					/>
				</label><br />
				<label>
					Next Phase
					<select
						id="to_phase_id"
						name="to_phase_id"
						value={to_phase_id}
						onChange={(e) => setToPhaseId(e.target.value)}
					>
						{filtered_phases_data &&
							filtered_phases_data.map((pd) => {
								return (
									<option key={pd.id} value={pd.id}>
										{pd.name}
									</option>
								);
							})}
					</select>
				</label>
				<button type="submit"><SaveIcon/></button>
			</form>
		</div>
	);
};
