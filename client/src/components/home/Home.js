import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { get_cookie } from '../../cookies_parser';
import authGet from "../../HttpRequest/authGet";



const Home = () => {
  const [content, setContent] = useState("");
  const history = useHistory();
  const url = 'http://localhost:8888/';

  if (!get_cookie("user_id")) {
        history.push("/login");
  }
  useEffect(() => {
    authGet(url)
    .then( data => { setContent(data.data.user_name) } )
    .catch( error => { console.log(error) });
  },[])

  // useEffect( async () => {
  //   const res = await fetch(url,{
  //     method: 'GET',
  //     mode: 'cors',
  //     credentials: 'include'
  //   })
  //   const data = await res.json();
  //   console.log(data.data.user_name)
  //   setContent(data.data.user_name)
  // },[]);

  return <div className="home">
    User_name: {content}
  </div>;
};

export default Home;
