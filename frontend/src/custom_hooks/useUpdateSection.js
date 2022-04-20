import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateSection = (all_positions_data, setSectionsData) => {
    const [updating, setUpdating] = useState(false);
    const [section_data, setSectionData] = useState();
    const [phase_data, setPhaseData] = useState();
    const [scts_data, setSctsData] = useState();
    const [update_section_component, setUpdateSectionComponent] = useState();
    const [success_component, setSuccessComponent] = useState();

    const { SectionCtlr } = useController();

    function setSectionToUpdate(section_data, sections_data, phase_data) {
        if (updating) return;
        setUpdating(true);
        setSectionData(section_data);
        setPhaseData(phase_data);
        setSctsData(sections_data);
    }

    useEffect(() => {
        if (updating) {
            setUpdateSectionComponent(
                <UpdateSection old_section_data={section_data} handleSubmit={handleSubmit} all_positions_data={all_positions_data} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateSectionComponent(null);
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
			phase_id: phase_data.id,
			position_id: e.target.position_id.value,
			order: e.target.order.value,
		};
		let data = await SectionCtlr.patch_rsc_ins(section_data.id, req_bod);
		// console.log('updated section data', data);
        setSuccessComponent(<UpdateSectionSuccess clearMessage={clearMessage}/>)
        setSectionsData(scts_data.map(sd => sd.id == data.id? data: sd))
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

    return {update_section_component, setSectionToUpdate, updating, success_component};
};


const UpdateSection = ({old_section_data, handleSubmit, all_positions_data, cancelSubmit}) => {
    const [name, setName] = useState(old_section_data.name);
	const [position_id, setPositionId] = useState(old_section_data.position_id);
	const [order, setOrder] = useState(old_section_data.order);
	const [positions, setPositions] = useState(all_positions_data);

	return (
		<div className="update-section">
			<form onSubmit={handleSubmit}>
				<div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

				<h2 className="action">Updating Section {old_section_data.id}</h2>

				<label htmlFor="name">Name</label>
				<input
					type="text"
					id="name"
					value={name}
					onChange={(e) => setName(e.target.value)}
				/>

				<label htmlFor="position_id">Position</label>
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

function UpdateSectionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Section is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}