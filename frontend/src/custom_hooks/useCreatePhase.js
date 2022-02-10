import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreatePhase = ( all_positions_data, setPhasesData ) => {
    const [creating, setCreating] = useState(false);
    const [phs_data, setPhsData] = useState();
    const [form_data, setFormData] = useState();
    const [create_phase_component, setCreatePhaseComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();

    const {PhaseCtlr} = useController();

    function setCreatePhase(form_data, phases_data) {
        setCreating(true);
        setFormData(form_data)
        setPhsData(phases_data);
    }

    useEffect(() => {
        if (creating) {
            setCreatePhaseComponent(
                <CreatePhase 
                all_positions_data={all_positions_data}
                phases_data={phs_data}
                handleSubmit={handleSubmit} 
                cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setCreatePhaseComponent(null);
        }
    }, [creating])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
			form_id: form_data.id,
			name: e.target.name.value,
			description: e.target.description.value,
			position_id: e.target.position_id.value,
			phase_type: e.target.phase_type.value,
            order: e.target.order.value
		};
        const data = await PhaseCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreatePhaseSuccess clearMessage={clearMessage}/>)
        setPhasesData([...phs_data, data])
        setCreating(false);
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setCreating(false);
    }
    
    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

  return {create_phase_component, setCreatePhase, creating, success_component};
};

const CreatePhase = ({
    all_positions_data,
    phases_data,
    handleSubmit, 
    cancelSubmit}) => {
	const [name, setName] = useState('New phase');
	const [description, setDescription] = useState('');
	const [position_id, setPositionId] = useState(1);
	const [phase_type, setPhaseType] = useState(phases_data.length == 0 ? 'begin': 'transit');
	const [positions, setPositions] = useState(all_positions_data);
	const [order, setOrder] = useState(phases_data.length + 1);

	return (
        <div className='create-phase'>
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon/></button>
                    <button onClick={cancelSubmit}><CancelIcon/></button>
                </div>

                <h2 className='action'>Creating New Phase</h2>

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

                <label htmlFor="position_id">Position</label><br />
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

function CreatePhaseSuccess({clearMessage}) {
    return (
        <div>
            <h4>Phase is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

