import { useState, useEffect } from "react"
import { UserCtlr } from '../controllers'

export function useUser (token) {
    const [user_data, setUserData] = useState(null)
    useEffect(() => {
        UserCtlr.get_rsc_ins(token).then(data => {
            setUserData(data)
            console.log('user_data', data);
        })
    }, [token])

    return {user_data}
}