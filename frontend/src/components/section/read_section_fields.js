import { useState, useEffect } from "react"
import ReadField from "../field/read_field"
import ReadSection from "./read_section"
import { useController } from '../../controllers'

export const ReadSectionFields = ({section_data}) => {
    const [fieldsdata, setFieldsdata] = useState([])
    const { SectionCtlr } = useController();

    useEffect(() => {
        SectionCtlr.get_rel_rsc(section_data.id, 'fields').then(data =>{
            setFieldsdata(data)
        })
    }, [])
    return (
        <div className="section">
            <ReadSection section_data={section_data} />
            <div className="fields">
                {fieldsdata && fieldsdata.map(fd => {
                    return <div className="field" key={fd.id}><ReadField field_data={fd}/></div>
                })}
            </div>
        </div>
    )
}