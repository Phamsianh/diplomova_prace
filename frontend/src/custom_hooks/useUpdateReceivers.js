import { useState, useEffect } from 'react';
import { CancelIcon, SaveIcon } from '../components/icon';
import { useController } from '../controllers';

export const useUpdateReceiver = (setReceivers) => {
    const [updating, setUpdating] = useState(false);
    const [instance_data, setInstanceData] = useState();
    const [receivers_data, setReceiversData] = useState();
    const [current_receivers, setCurrentReceivers] = useState();
    const [current_sections, setCurrentSections] = useState();
    const [update_receiver_component, setUpdateReceiverComponent] = useState();
    const [success_component, setSuccessComponent] = useState();


    const { ReceiverCtlr } = useController();

    function setReceiverToUpdate(instance_data, current_receivers, current_sections, receivers) {
        if (updating) return;
        setUpdating(true);
        setInstanceData(instance_data)
        setCurrentReceivers(current_receivers)
        setCurrentSections(current_sections);
        setReceiversData(receivers);
    }

    useEffect(() => {
        if (updating) {
            setUpdateReceiverComponent(
                <UpdateReceiver 
                current_receivers={current_receivers}
                current_sections={current_sections} 
                receivers_data={receivers_data} 
                handleSubmit={handleSubmit} 
                cancelSubmit={cancelSubmit}/>
            )
        }
        else {
			setUpdateReceiverComponent(null);
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
        if (e.target.update.value == 'true') {
            const req_bod = {
                user_id: e.target.user_id.value
            }
            let receiver_id = e.target.existed_receiver_id.value
            let data = await ReceiverCtlr.patch_rsc_ins(receiver_id, req_bod)
            // console.log("updated receiver data", data);
            setReceivers(receivers_data.map(rd => rd.id == receiver_id? data : rd))
            setSuccessComponent(<UpdateReceiverSuccess clearMessage={clearMessage}/>)
            setUpdating(false);
        }
        else {
            const req_bod = {
                instance_id: instance_data.id,
                section_id: e.target.selected_section_id.value,
                user_id: e.target.user_id.value
            };
            let data = await ReceiverCtlr.post_rsc(req_bod)
            // console.log("new receiver data", data);
            setReceivers(receivers_data.concat(data))
            setSuccessComponent(<UpdateReceiverSuccess clearMessage={clearMessage}/>)
            setUpdating(false);
        }
    }

    function cancelSubmit (e) {
		e.preventDefault();
        setUpdating(false);
    }
    
    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {update_receiver_component, setReceiverToUpdate, updating, success_component};
};

const UpdateReceiver = ({
    current_sections,
    receivers_data,
    handleSubmit, 
    cancelSubmit
}) => {
    
    const [selected_section_id, setSelectedSectionId] = useState(current_sections[0].id);
    const [all_current_potential_receivers, setAllCurrentPotentialReceivers] = useState();
    const [current_potential_receivers, setCurrentPotentialReceivers] = useState();
    const [existed_receiver, setExistedReceiver] = useState(false);
    const [update, setUpdate] = useState(false);
    const [user_id, setUserId] = useState();
    const { SectionCtlr } = useController();

    useEffect(() => {
        if (!selected_section_id) return
        let existed_receiver = receivers_data.find(rd => rd.section_id == selected_section_id)
        if (existed_receiver) {
            setExistedReceiver(existed_receiver)
            setUpdate(true)
        }
        else {
            setUpdate(false)
        }
    }, [selected_section_id])

    useEffect(() => {
        if(!existed_receiver) return
        setUserId(existed_receiver.user_id)
    }, [existed_receiver])

    useEffect(() => {
        async function setCurrentPotentialReceivers() {
            let all_current_potential_receivers = {};
            for (const section of current_sections) {
                all_current_potential_receivers[section.id] = await SectionCtlr.get_rel_rsc(section.id, "potential_receivers")
            }
            // console.log("all current potential receivers", all_current_potential_receivers);
            setAllCurrentPotentialReceivers(all_current_potential_receivers);
        }
        setCurrentPotentialReceivers();
    }, [])

    useEffect(() => {
        if (!selected_section_id || !all_current_potential_receivers) return;
        setCurrentPotentialReceivers(all_current_potential_receivers[selected_section_id])
    }, [selected_section_id, all_current_potential_receivers])
    return (
        <div className="update-receiver">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
					<button type="submit"><SaveIcon/></button>
					<button onClick={cancelSubmit}><CancelIcon/></button>
				</div>

                <h2>Select section</h2>

                <select name="selected_section_id" id="selected_section_id" value={selected_section_id} onChange={e => setSelectedSectionId(e.target.value)}>
                    {current_sections.map(cs => {
                        return <option key={cs.id} value={cs.id}>{cs.name} - {cs.id}</option>
                    })}
                </select>
                
                {update ? "Updating receiver" : "Adding receiver"}
                <input type="hidden" name="update" value={update} />
                {existed_receiver && <input type="hidden" name="existed_receiver_id" value={existed_receiver.id} />}

                {selected_section_id && <select name="user_id" id="user_id" value={user_id} onChange={e => setUserId(e.target.value)}>
                    {current_potential_receivers && current_potential_receivers.map(cpr => {
                        return <option key={cpr.id} value={cpr.id}>{cpr.first_name} {cpr.last_name}</option>
                    })}
                </select>}
				
            </form>
        </div>
    )
}


function UpdateReceiverSuccess({clearMessage}) {
    return (
        <div>
            <h4>Receiver is updated successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}

