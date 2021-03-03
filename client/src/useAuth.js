import { useEffect, useState } from "react";

const useAuth = async (url) => {
  const [data, setData] = useState();
  // const [ispending, setIsPending] = useState(true);
  // const [error, setError] = useState(null);

  useEffect(async () => {
    const abortCont = new AbortController();
    try {
      const res = await fetch(url, {
        method: "GET",
        mode: "cors",
        credentials: "include",
        signal: abortCont.signal,
      });
      if (!res.ok) throw Error("Request failed");
      else {
        console.log(res);
        setData(await res.json());
        // setIsPending(false);
        // setError(null);
      }
    } 
    catch (err) {
      if (err.name === "AbbortError") {
        console.log("fetch aborted");
      } else {
        console.log(err.message);
        // setIsPending(false);
        // setError(err.message);
      }
    }
    return () => abortCont.abort();
  }, [url]);

  // return { data, ispending, error };
  // const d = await data;
  return await data;
};

export default useAuth;
