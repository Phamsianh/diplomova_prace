import { useEffect, useState } from "react";
import authGet from "../../HttpRequest/authGet"

const Roles = () => {
    const [data, setData] = useState('')

    useEffect(async () => {
        const d = await authGet("http://localhost:8888/roles")
        setData(JSON.stringify(d))
        console.log(d)
    }, [])

    return (
        <div className="roles">
            Roles <br/>
            res: <br/>
            {data}
        </div>
    );
}
 
export default Roles;