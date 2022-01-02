import { useState, useEffect } from 'react'
import { FieldCtlr } from '../../controllers'
import ReadField from './read_field'

export const ActiveReadField = ({field_id}) => {
    const [ fielddata, setFieldata ] = useState()
    useEffect(() => {
        FieldCtlr.get_rsc_ins(field_id).then(data => {
            setFieldata(data)
        })
    }, [])
    return (
        <>
        { fielddata && <ReadField field_data={fielddata}/>}
        </>
    )
}
