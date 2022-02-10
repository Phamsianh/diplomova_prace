import { useState, useEffect } from 'react';
import { CancelIcon, NoIcon, SaveIcon, YesIcon } from '../components/icon';
import { useController } from '../controllers';

export const useReceiveInstance = (setInstanceData, setInstancesFieldsData) => {
    const [receiving, setReceiving] = useState(false);
    const [user_data, setUserData] = useState();
    const [ins, setInsData] = useState();
    const [current_sections, setCurrentSections] = useState();
    const [current_receivers, setCurrentReceivers] = useState();
    const [positions_data, setPositionsData] = useState();
    const [receive_instance_component, setReceiveInstanceComponent] = useState(null);
    const [success_component, setSuccessComponent] = useState();
    
    const { InstanceCtlr } = useController();

    function setReceiveInstance(user_data, instance_data, current_sections, current_receivers, positions_data){
        setReceiving(true);
        setUserData(user_data);
        setInsData(instance_data);
        setCurrentSections(current_sections);
        setCurrentReceivers(current_receivers);
        setPositionsData(positions_data);
    }

    useEffect(() => {
        if (receiving) {
            setReceiveInstanceComponent(
                <ReceiveInstance 
                user_data={user_data}
                instance_data={ins}
                current_sections={current_sections} 
                current_receivers={current_receivers}
                positions_data={positions_data}
                handleSubmit={handleSubmit} 
                cancelSubmit={cancelSubmit} />
            )
        }
        else {
            setReceiveInstanceComponent(null)
        }

    }, [receiving])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
            handle: true
        }
        let data = await InstanceCtlr.patch_rsc_ins(ins.id, req_bod)
        console.log("instance data after received", data);
        setSuccessComponent(<ReceiveInstanceSuccess clearMessage={clearMessage}/>)
        setInstanceData(data);
        data = await InstanceCtlr.get_rel_rsc(ins.id, 'instances_fields')
        console.log("instances fields data after received", data);
        setInstancesFieldsData(data);
        setReceiving(false);
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setReceiving(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {receive_instance_component, setReceiveInstance, receiving, success_component};
};

function ReceiveInstance ({user_data, current_sections, current_receivers, positions_data, handleSubmit, cancelSubmit}) {
    return (
        <div className="receive-instance">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button onClick={cancelSubmit}><CancelIcon/></button>
                </div>
                <h3 className='action'>Receive Instance</h3>
                
                <h4>Do you want to initialize these sections</h4>
                {current_sections.map(cs => {
                    if (current_receivers.find(cr => !cr.received && cr.section_id == cs.id && cr.user_id == user_data.id)) {
                        return (
                        <p key={cs.id}>
                            {cs.name? cs.name: 'Section Name'} 
                            - { positions_data && positions_data.find(pd => pd.id == cs.position_id)?.name}
                        </p>
                        )
                    }
                })}
                <button type='submit'><YesIcon/></button>
                <button onClick={cancelSubmit}><NoIcon/></button>
            </form>
        </div>
    )
}

function ReceiveInstanceSuccess({clearMessage}) {
    return (
        <div>
            <h4>Instance is received</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}