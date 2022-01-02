import { useState, useEffect } from "react"
import { SectionCtlr } from "../../controllers"
import ReadSection from "./read_section"

export const ActiveReadSection = ({section_id}) => {
    const [sectiondata, setSectiondata] = useState()

    useEffect(() => {
        SectionCtlr.get_rsc_ins(section_id).then(data =>{
            setSectiondata(data)
        })
    }, [])
    return (
        <>
        {sectiondata && <ReadSection section_data={sectiondata}/>}
        </>
    )
}
