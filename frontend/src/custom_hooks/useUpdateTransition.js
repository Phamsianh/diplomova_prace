import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateTransition = (setTransitionsData) => {
    const [updating, setUpdating] = useState(false);
    const [transition_data, setTransitionData] = useState();
    const [trs_data, setTrsData] = useState();
    const [phases_data, setPhasesData] = useState();
    const [from_phase_data, setFromPhaseData] = useState();
    const [update_transition_component, setUpdateTransitionComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const { TransitionCtlr } = useController();

    function setTransitionToUpdate(transition_data, transitions_data, from_phase_data, phases_data) {
        if (updating) return;
        setUpdating(true);
        setTransitionData(transition_data);
        setTrsData(transitions_data);
        setFromPhaseData(from_phase_data);
        setPhasesData(phases_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateTransitionComponent(
                <UpdateTransition 
                old_transition_data={transition_data}
                from_phase_data={from_phase_data}
				phases_data={phases_data}
				transitions_data={trs_data}
				handleSubmit={handleSubmit} 
				cancelSubmit={cancelSubmit} 
				/>
            )
        }
        else {
			setUpdateTransitionComponent(null);
		};
    }, [updating])

	useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit(e) {
		e.preventDefault();
        const req_bod = {
			name: e.target.name.value,
			from_phase_id: from_phase_data.id,
			to_phase_id: e.target.to_phase_id.value,
		};
		let data = await TransitionCtlr.patch_rsc_ins(transition_data.id, req_bod);
		// console.log('updated transition data', data);
        setSuccessComponent(<UpdateTransitionSuccess clearMessage={clearMessage}/>)
        setTransitionsData(trs_data.map(pd => pd.id == data.id? data: pd))
        setUpdating(false);
    }

    function cancelSubmit (e) {
		e.preventDefault();
        setUpdating(false);
    }
    
    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {update_transition_component, setTransitionToUpdate, updating, success_component};
};

const UpdateTransition = ({
	old_transition_data, 
	from_phase_data, 
	phases_data,
	transitions_data,
	handleSubmit, 
	cancelSubmit, 
}) => {
	const [name, setName] = useState(old_transition_data.name);
	const [to_phase_id, setToPhaseId] = useState(old_transition_data.to_phase_id);
	const [next_phases, setNextPhases] = useState(phases_data.filter(pd => {
		if (pd.id == old_transition_data.to_phase_id) return true
		else if(
			pd.id === from_phase_data.id || 
			transitions_data.find(t => t.from_phase_id == from_phase_data.id && t.to_phase_id == pd.id)
			) return false
		else return true
	}))

	return (
		<div className="update-transition">
			<form onSubmit={handleSubmit}>
				<div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <h2 className='action'>Update Transition {old_transition_data.id}</h2>

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
						{next_phases.map((np) => {
								return (
									<option key={np.id} value={np.id}>
										{np.name}
									</option>
								);
							})}
					</select>
				</label>
			</form>
		</div>
	);
}

function UpdateTransitionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Transition is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}
