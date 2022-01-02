import { useState, useEffect } from "react"
import { PhaseCtlr } from "../../controllers"
import ReadPhase from "./read_phase"

export const ActiveReadPhase = ({phase_id}) => {
    const [phasedata, setPhasedata] = useState()

    useEffect(() => {
        PhaseCtlr.get_rsc_ins(phase_id).then(data => {
            setPhasedata(data)
        })
    })
    return (
        <>
        {phasedata && <ReadPhase phase_data={phasedata}/>}
        </>
    )
}
