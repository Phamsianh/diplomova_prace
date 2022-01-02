import { useState, useEffect, useContext } from "react"
import { useController } from "../../../controllers"
import { InstanceContentContext } from "../../../pages/instance_page/read_instance_page"
import ReadPhase from "../../phase/read_phase"
import { ReadSectionFields } from "./read_section_fields"

export const ReadPhaseSections = ({phase_data}) => {
    const {instance_data} = useContext(InstanceContentContext)
    const {PhaseCtlr} = useController();
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