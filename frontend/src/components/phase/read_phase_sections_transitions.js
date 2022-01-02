import { useState, useEffect } from "react"
import ReadPhase from "./read_phase"
import { ReadSectionFields } from "../section/read_section_fields"
import { ReadTransition } from "../transition/read_transition"
import { useController } from "../../controllers"

export const ReadPhaseSectionsTransitions = ({phase_data}) => {
    const [sectionsdata, setSectionsdata] = useState()
    const [transitionsdata, setTransitionsdata] = useState()
    const { PhaseCtlr } = useController();

    useEffect(() => {
        PhaseCtlr.get_rel_rsc(phase_data.id, 'sections').then(data =>{
            setSectionsdata(data)
        })
        PhaseCtlr.get_rel_rsc(phase_data.id, 'from_transitions').then(data => {
            console.log('totransitiondata', data);
            setTransitionsdata(data)
        })
    }, [])
    return (
        <div className="phase">
            <ReadPhase phase_data={phase_data} />
            
            <div className="sections">
                {sectionsdata && sectionsdata.map(sd => {
                    return <ReadSectionFields section_data={sd} key={sd.id}/>
                })}
            </div>
            
            <div className="transitions">
                {transitionsdata && transitionsdata.map(td => {
                    return <ReadTransition transition_data={td} key={td.id}/>
                })}
            </div>
        </div>
    )
}