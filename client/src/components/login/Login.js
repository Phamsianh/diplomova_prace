import { useState } from "react";
import { useHistory } from "react-router-dom";
import Loading from "./../loading/Loading";

const Login = () => {
  const history = useHistory();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState("");
  const [showform, setShowForm] = useState(true);
  const [emailerror, setEmailError] = useState("");
  const [passworderror, setPasswordError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowForm(false);
    setLoading("Pending request...");
    const user = { email, password };
    const formdata = new URLSearchParams(user);

    console.log(formdata.toString());
    fetch("http://localhost:8888/login", {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formdata,
      credentials: "include",
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setLoading("Fetching data...");
        if (data.auth) {
          setLoading("Redirecting to Home page...");
          history.push("/");
        } else {
          setEmailError(data.error.email);
          setPasswordError(data.error.password);
          setShowForm(true);
          setLoading("");
        }
      });
  };

  return (
    <div className="container flex-center height-100 mg_4">
      {loading && <Loading content={loading}></Loading>}
      {showform && (
        <form
          onSubmit={handleSubmit}
          className="flex-center flex-direction-column width-60 height-60 bg-grey box-shadow bd-round"
        >
          <label className="flex-center flex-direction-column width-80 pd_2 ">
            User name or email
            <input
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="text"
              placeholder="Email or user name..."
              name="email_or_username"
              className="display-block width-100 pd_2 bd-round"
            />
            {emailerror && <div className="red">{emailerror}</div>}
          </label>
          <label className="flex-center flex-direction-column width-80 pd_2 ">
            Password
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="Password..."
              name="password"
              className="display-block width-100 pd_2 bd-round"
            />
            {passworderror && <div className="red">{passworderror}</div>}
          </label>
          <input type="submit" value="Submit" className="btn bd-round" />
          <p>{email}</p>
          <p>{password}</p>
        </form>
      )}
    </div>
  );
};

export default Login;
