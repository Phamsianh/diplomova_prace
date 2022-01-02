import { useState, useEffect } from "react"
import { PhaseCtlr } from "../../controllers"
import ReadPhase from "./read_phase"
import { ReadSectionFields } from "../section/read_section_fields"

export const ReadPhaseSections = ({phase_data}) => {
    const [sectionsdata, setSectionsdata] = useState()

    useEffect(() => {
        PhaseCtlr.get_rel_rsc(phase_data.id, 'sections').then(data =>{
            setSectionsdata(data)
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
        </div>
    )
}