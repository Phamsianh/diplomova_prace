import { useState, useEffect } from 'react';
import { CancelIcon, NoIcon, YesIcon } from '../components/icon';
import { useController } from '../controllers';

export const useMarkInstaceDone = (setInstanceData) => {
    const [marking_done, setMarkingDone] = useState(false);
    const [ins_data, setInsData] = useState();
    const [mark_done_component, setMarkDoneComponent] = useState(null);
    const [success_component, setSuccessComponent] = useState();

    const {InstanceCtlr} = useController();

    function setMarkDone(instance_data) {
        setMarkingDone(true)
        setInsData(instance_data);
    }

    useEffect(() => {
        if (marking_done) {
            setMarkDoneComponent(
                <MarkDoneComponent handleSubmit={handleSubmit} cancelSubmit={cancelSubmit}/>
            )
        }
        else {
            setMarkDoneComponent(null)
        }

    }, [marking_done])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {
            done: true
        }
        let data = await InstanceCtlr.patch_rsc_ins(ins_data.id, req_bod)
        // console.log("instance data after mark as done", data);
        setSuccessComponent(<MarkDoneSuccess clearMessage={clearMessage}/>)
        setInstanceData(data);
        setMarkingDone(false);
    }

    function cancelSubmit(e) {
        e.preventDefault();
        setMarkingDone(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {mark_done_component, marking_done, setMarkDone, success_component}
}

function MarkDoneComponent ({handleSubmit, cancelSubmit}) {
    return (
        <div className="mark-instance-done">
            <form onSubmit={handleSubmit}>
                <div className="manage-buttons">
                    <button onClick={cancelSubmit}><CancelIcon/></button>
                </div>
                <h3 className='action'>Mark instance as done</h3>
                
                <h4>Do you want to mark this instance as done?</h4>
                <p>Once you mark the instance as done, the instance cannot be modified</p>
                <button type='submit'><YesIcon/></button>
                <button onClick={cancelSubmit}><NoIcon/></button>
            </form>
        </div>
    )
}

function MarkDoneSuccess({clearMessage}) {
    return (
        <div>
            <h4>The instance is completely handled.</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}