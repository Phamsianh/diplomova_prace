import { useState, useEffect, useContext } from 'react';
import { CancelIcon, CreateIcon } from '../icon';
import { PhasesData } from '../form/read_form_phases';

export const CreateTransition = ({ handleCreate, cancelCreate, from_phase_id }) => {
	const phases_data = useContext(PhasesData)
	// const [phases_data, setPhasesData] = useState(phases_data_context && phases_data_context);
	const [name, setName] = useState();
	const [to_phase_id, setToPhaseId] = useState();
	const [filtered_phases_data, setFiltered_phases_data] = useState()

	useEffect(() => {
		setFiltered_phases_data(phases_data.filter(pd => {
			return pd.id !== from_phase_id
		}))
	}, [phases_data])

	return (
		<div className="transition">
			<div className="create-transition">
				<div className="manage-buttons">
					<button onClick={cancelCreate}>
						<CancelIcon />
					</button>
				</div>

				<form onSubmit={handleCreate}>
					<label>
						Name
						<input
							id="name"
							type="text"
							placeholder="Transition Name"
							onChange={(e) => setName(e.target.value)}
						/>
					</label><br />
					<label>
						Next Phase
						<select
							name="to_phase_id"
							id="to_phase_id"
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
					<button type="submit"><CreateIcon/></button>
				</form>
			</div>
		</div>
	);
};
