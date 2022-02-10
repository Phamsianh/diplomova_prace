import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';

export const useDeleteTransition = (setTransitionsData) => {
    const [success_component, setSuccessComponent] = useState();

    const { TransitionCtlr } = useController();

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])


    async function deleteTransition(transition_data, transitions_data) {
		let data = await TransitionCtlr.delete_rsc_ins(transition_data.id);
        console.log(data);
        if (data == null) {
            console.log(transitions_data.filter(td => td.id != transition_data.id));
            setSuccessComponent(<DeletePhaseSuccess clearMessage={clearMessage}/>)
            setTransitionsData(transitions_data.filter(td => td.id != transition_data.id))    
        }
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {deleteTransition, success_component};
};


function DeletePhaseSuccess({clearMessage}) {
    return (
        <div>
            <h4>Phase is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}