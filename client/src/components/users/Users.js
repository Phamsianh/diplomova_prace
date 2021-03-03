import { useEffect, useState } from "react";
import authGet from "../../HttpRequest/authGet"

const Users = () => {
    const [data, setData] = useState('')

    useEffect(async () => {
        const d = await authGet("http://localhost:8888/users")
        setData(JSON.stringify(d))
        console.log(d)
    }, [])

    return (
        <div className="users">
            Users <br/>
            res: <br/>
            {data}
        </div>
    );
}
 
export default Users;