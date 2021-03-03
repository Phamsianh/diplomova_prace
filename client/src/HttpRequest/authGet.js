async function authGet(url){
  
  const res = await fetch(url,{
    method: "GET",
    mode: "cors",
    credentials: "include"
  });

  if (res.ok) {
    return await res.json();
  }
  else throw Error('failed to fetch');
}
 
export default authGet;