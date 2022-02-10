import { useState, useEffect } from 'react';
import { CancelIcon, CreateIcon } from '../components/icon';
import { useController } from '../controllers';

export const useCreateSection = (all_positions_data, setSectionsData) => {
    const [creating, setCreating] = useState(false);
    const [Sss_data, setSssData] = useState();
    const [phase_data, setPhaseData] = useState();
    const [create_section_component, setCreateSectionComponent] =  useState();
    const [success_component, setSuccessComponent] = useState();


    const {SectionCtlr} = useController();

    function setCreateSection(phase_data, sections_data) {
        setCreating(true);
        setPhaseData(phase_data)
        setSssData(sections_data);
    }

    useEffect(() => {
        if (creating) {
            setCreateSectionComponent(
                <CreateSection 
                phase_data={phase_data}
                all_positions_data={all_positions_data}
                sections_data={Sss_data}
                handleSubmit={handleSubmit} 
                cancelSubmit={cancelSubmit} 
                />
            )
        }
        else {
            setCreateSectionComponent(null);
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
			name: e.target.name.value,
			phase_id: phase_data.id,
			position_id: e.target.position_id.value,
			order: e.target.order.value,
		};
        const data = await SectionCtlr.post_rsc(req_bod);
        setSuccessComponent(<CreateSectionSuccess clearMessage={clearMessage}/>)
        setSectionsData([...Sss_data, data])
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

  return {create_section_component, setCreateSection, creating, success_component};
};


const CreateSection = ({
    phase_data, 
    all_positions_data,
    sections_data,
    handleSubmit, 
    cancelSubmit}) => {
    const [name, setName] = useState('New section');
	const [position_id, setPositionId] = useState(phase_data.position_id);
	const [order, setOrder] = useState(sections_data.filter(s => s.phase_id == phase_data.id).length + 1);
	const [positions, setPositions] = useState(all_positions_data);

	return (
        <div className="create-section">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button type="submit"><CreateIcon /></button>
                    <button onClick={cancelSubmit}><CancelIcon /></button>
                </div>

                <h2 className='action'>Create New Section</h2>

                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />

                <label htmlFor="position_id">Position</label>
                <br />
                <select
                    id="position_id"
                    onChange={(e) => setPositionId(e.target.value)}
                    value={position_id}
                >
                    {positions
                        ? positions.map((p) => {
                                return (
                                    <option value={p.id} key={p.id}>
                                        {p.name}
                                    </option>
                                );
                            })
                        : ''}
                </select>
                <br />

                <label htmlFor="order">Order</label>
                <input
                    type="number"
                    id="order"
                    value={order}
                    min="-2147483648"
                    max="2147483648"
                    onChange={(e) => setOrder(e.target.value)}
                />
            </form>
        </div>
	);
}

function CreateSectionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Section is created successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}
