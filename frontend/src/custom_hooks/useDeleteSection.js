import { useController } from '../controllers';
import { useState, useEffect } from 'react';
import { CancelIcon } from '../components/icon';

export const useDeleteSection = (setSectionsData) => {
    const [success_component, setSuccessComponent] = useState();

    const { SectionCtlr } = useController();

    useEffect(() => {
        if(!success_component) return
        setTimeout(() => {
            setSuccessComponent(null)
        }, 3000)
    }, [success_component])
    
    async function deleteSection(section_data, sections_data) {
		let data = await SectionCtlr.delete_rsc_ins(section_data.id);
        // console.log(data);
        if (data == null) {
            setSuccessComponent(<DeleteSectionSuccess clearMessage={clearMessage}/>)
            setSectionsData(sections_data.filter(sd => sd.id != section_data.id))    
        }
    }

    function clearMessage(e) {
        e.preventDefault();
        setSuccessComponent(null)
    }

    return {deleteSection, success_component};
};

function DeleteSectionSuccess({clearMessage}) {
    return (
        <div>
            <h4>Section is deleted successfully</h4>
            <button onClick={clearMessage}><CancelIcon/></button>
        </div>
    )
}