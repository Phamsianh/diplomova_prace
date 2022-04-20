import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon, DeleteIcon } from '../components/icon';

export const useDeletePosition = (setPositionsData) => {
    const [psts_data, setRlsData] = useState();
    const [delete_position_component, setDeletePositionComponent] = useState();
    const [deleting, setDeleting] = useState(false);
    const [success_component, setSuccessComponent] = useState();
    
    const { PositionCtlr } = useController();

    function setDeletePosition(positions_data) {
        setDeleting(true);
        setRlsData(positions_data);
    }

    useEffect (() => {
        if (deleting) {
            setDeletePositionComponent(
                <DeletePosition 
                positions_data={psts_data} 
                handleDelete={deletePosition} 
                cancelDelete={cancelDelete} />
            )
        }
        else{
            setDeletePositionComponent(null);
        }
    }, [deleting])

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])

    async function deletePosition(e) {
        e.preventDefault();
        let selected_position_id = e.target.selected_position_id.value
		let data = await PositionCtlr.delete_rsc_ins(selected_position_id);
        // console.log(data);
        if (data == null) {
            setDeleting(false)
            setSuccessComponent(<DeletePositionSuccess clearMessage={clearMessage}/>)
            setPositionsData(psts_data.filter(pd => pd.id != selected_position_id))
            
        }
    }

    function cancelDelete(e) {
        e.preventDefault();
        setDeleting(false);
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }
    
    return {delete_position_component, deleting, setDeletePosition, success_component};
};

function DeletePosition({positions_data, handleDelete, cancelDelete}) {
    const [selected_position_id, setSelectedPositionId] = useState();
    useEffect(() => {
        setSelectedPositionId(positions_data[0].id)
    }, [])
    return <div className="delete-position">
        <form onSubmit={handleDelete}>
            <div className="manage-buttons">
                <button type="submit"><DeleteIcon/></button>
                <button onClick={cancelDelete}><CancelIcon/></button>
            </div>

            {selected_position_id && <select name="selected_position_id" id="selected_position_id" value={selected_position_id} onChange={ e => setSelectedPositionId(e.target.value) }>
                {positions_data.map(pd => {
                    return <option key={pd.id} value={pd.id}>{pd.name} - {pd.id}</option>
                })}
            </select>}
        </form>
    </div>
}

function DeletePositionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Position is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}