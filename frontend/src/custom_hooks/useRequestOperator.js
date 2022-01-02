import { useState, useEffect } from "react"
const useRequestOperator = (req_opr, params = null, abortController) => {
    const [data, setData] = useState(null)
    const [pending, setPending] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
        req_opr(params)
        .then(data => {
            console.log(data);
            setData(data);
            setPending(false);
            setError(null);
        })
        .catch(e => {
            if (e.name === "AbortError") {
                console.log("fetch's aborted");
            }
            else{
                console.log(e);
                setPending(false);
                setError(true);
            }
        })
        return () => {
            abortController.abort();
        }
    }, [])
    return {data, pending, error};
}
 
export default useRequestOperator;