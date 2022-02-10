import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';

export const useDeletePhase = (setPhasesData) => {
    const [success_component, setSuccessComponent] = useState();

    const { PhaseCtlr } = useController();

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])
    
    async function deletePhase(phase_data, phases_data) {
		let data = await PhaseCtlr.delete_rsc_ins(phase_data.id);
        console.log(data);
        if (data == null) {
            console.log(phases_data.filter(pd => pd.id != phase_data.id));
            setSuccessComponent(<DeletePhaseSuccess clearMessage={clearMessage}/>)
            setPhasesData(phases_data.filter(pd => pd.id != phase_data.id))    
        }
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {deletePhase, success_component};
};

function DeletePhaseSuccess({clearMessage}) {
    return (
        <div>
            <h4>Phase is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}