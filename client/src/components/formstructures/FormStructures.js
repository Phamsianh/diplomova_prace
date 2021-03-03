import { useEffect, useState } from "react";
import authGet from "../../HttpRequest/authGet"

const FormStructures = () => {
    const [data, setData] = useState('')

    useEffect(async () => {
        const d = await authGet("http://localhost:8888/formstructures")
        setData(JSON.stringify(d))
        console.log(d)
    }, [])

    return (
        <div className="formstructures">
            form structures <br/>
            res: <br/>
            {data}
        </div>
    );
}
 
export default FormStructures;