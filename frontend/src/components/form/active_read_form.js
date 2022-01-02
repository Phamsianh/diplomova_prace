import { useState, useEffect } from "react"
import { FormCtlr } from "../../controllers"
import ReadForm from "./read_form"

export const ActiveReadForm = ({phase_id}) => {
    const [formdata, setFormdata] = useState()

    useEffect(() => {
        FormCtlr.get_rsc_ins(phase_id).then(data => {
            setFormdata(data)
        })
    })
    return (
        <>
        {formdata && <ReadForm form_data={formdata}/>}
        </>
    )
}
