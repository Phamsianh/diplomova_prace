import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreateTransition = (setTransitionsData) => {
    const [creating, setCreating] = useState(false);
    const [trs_data, setTrsData] = useState();
    const [phases_data, setPhasesData] = useState();
    const [from_phase_data, setFromPhaseData] = useState();
    const [create_transition_component, setCreateTransitionComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();
    const [error_component, setErrorComponent] = useState();

    const { TransitionCtlr } = useController();

    function setTransitionToCreate(transitions_data, from_phase_data, phases_data) {
        if (creating) return;
        setCreating(true);
        setTrsData(transitions_data);
        setFromPhaseData(from_phase_data);
        setPhasesData(phases_data);
    }

    useEffect(() => {
        if (creating) {
            setCreateTransitionComponent(
                <CreateTransition 
                handleSubmit={handleSubmit} cancelSubmit={cancelSubmit} 
                from_phase_data={from_phase_data} phases_data={phases_data} transitions_data={trs_data}/>
            )
        }
        else {
			setCreateTransitionComponent(null);
		};
    }, [creating])

	useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

	useEffect(() => {
        if(!error_component) return
        setTimeout(() => {
            setErrorComponent(null)
        }, 3000)
    }, [error_component])

    async function handleSubmit(e) {
		e.preventDefault();
        const req_bod = {
			name: e.target.name.value,
			from_phase_id: from_phase_data.id,
			to_phase_id: e.target.to_phase_id.value,
		};
		let data = await TransitionCtlr.post_rsc(req_bod).catch(e => {
			setErrorComponent(
				<CreateTransitionError message={e.message} clearMessage={clearError} />
			)
			throw e
		});
		console.log('created transition data', data);
        setSuccessComponent(<CreateTransitionSuccess clearMessage={clearSuccess}/>)
        setTransitionsData([...trs_data, data])
        setCreating(false);
    }

    function cancelSubmit (e) {
		e.preventDefault();
        setCreating(false);
    }

	function clearSuccess(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

	function clearError(e) {
        e.preventDefault();
		setErrorComponent(null)
	}

    return {create_transition_component, setTransitionToCreate, creating, success_component, error_component};
};

const CreateTransition = ({handleSubmit, cancelSubmit, from_phase_data, phases_data, transitions_data}) => {
	const [name, setName] = useState('');
	const [next_phases, setNextPhases] = useState(
		phases_data.filter(pd => {
			if(pd.id == from_phase_data.id || transitions_data.find(t => t.from_phase_id == from_phase_data.id && t.to_phase_id == pd.id)) return false
			return true
		})
	)
	const [to_phase_id, setToPhaseId] = useState();


	return (
		<div className="create-transition">
			<form onSubmit={handleSubmit}>
				<div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <h2 className='action'>Create Transition</h2>

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
						{next_phases && next_phases.map((np) => {
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

function CreateTransitionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Transition is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

function CreateTransitionError({message, clearMessage}) {
	return(
		<div>
			<h4>{message}</h4>
			<button onClick={clearMessage}><CancelIcon/></button>
		</div>
	)
}