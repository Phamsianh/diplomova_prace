import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdatePhase = (all_positions_data, setPhasesData) => {
    const [updating, setUpdating] = useState(false);
    const [phase_data, setPhaseData] = useState();
    const [phs_data, setPhsData] = useState();
    const [update_phase_component, setUpdatePhaseComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();
	
    const { PhaseCtlr } = useController();

    function setPhaseToUpdate(phase_data, phases_data) {
        if (updating) return;
        setUpdating(true);
        setPhaseData(phase_data);
        setPhsData(phases_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdatePhaseComponent(
                <UpdatePhase 
				old_phase_data={phase_data} 
				phases_data={phs_data}
				handleSubmit={handleSubmit} 
				all_positions_data={all_positions_data} 
				cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdatePhaseComponent(null);
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
			description: e.target.description.value,
			position_id: e.target.position_id.value,
			phase_type: e.target.phase_type.value,
			order: e.target.order.value
		};
		let data = await PhaseCtlr.patch_rsc_ins(phase_data.id, req_bod);
		console.log('updated phase data', data);
        setSuccessComponent(<UpdatePhaseSuccess clearMessage={clearMessage}/>)
        setPhasesData(phs_data.map(pd => pd.id == data.id? data: pd))
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

    return {update_phase_component, setPhaseToUpdate, updating, success_component};
};



const UpdatePhase = ({ 
	old_phase_data,
	phases_data,
	handleSubmit, 
	all_positions_data, 
	cancelSubmit}) => {
	const [name, setName] = useState(old_phase_data.name);
	const [description, setDescription] = useState(old_phase_data.description?old_phase_data.description:'');
	const [position_id, setPositionId] = useState(old_phase_data.position_id);
	const [phase_type, setPhaseType] = useState(old_phase_data.phase_type);
	const [positions, setPositions] = useState(all_positions_data);
	const [order, setOrder] = useState(old_phase_data.order);

	return (
		<div className='update-phase'>
			<form onSubmit={handleSubmit}>
				<div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

				<h2 className="action">Updating Phase {old_phase_data.id}</h2>

				<label htmlFor="name">Name</label>
				<input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>

				<label htmlFor="description">Description</label>
				<input
					type="text"
					id="description"
					value={description}
					onChange={(e) => setDescription(e.target.value)}
				/>

				<label htmlFor="position_id">Position</label>
				<select id="position_id" onChange={(e) => setPositionId(e.target.value)} value={position_id}>
					{positions
						? positions.map((p) => {
								return (
									<option
										value={p.id}
                                        key={p.id}
									>
										{p.name}
									</option>
								);
						  })
						: ''}
				</select><br />
                
				<label htmlFor="phase_type">Phase Type</label>
				<select
					id="phase_type"
					value={phase_type}
					onChange={(e) => setPhaseType(e.target.value)}
				>
					<option value="begin">Begin</option>
					<option value="transit">Transit</option>
					<option value="end">End</option>
				</select><br />
				
				<label htmlFor="order">Order</label>
				<input type="number" name="order" id="order" min='-2147483648' max='2147483648'  
				value={order} 
				onChange={e => setOrder(e.target.value)}/>
			</form>
		</div>
	);
};

export default UpdatePhase;


function UpdatePhaseSuccess({clearMessage}) {
    return (
        <div>
            <h4>Phase is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}