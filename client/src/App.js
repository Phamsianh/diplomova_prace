import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Login from "./components/login/Login";
import Register from "./components/register/Register";
import Home from "./components/home/Home";
import FormStructures from "./components/formstructures/FormStructures";
import Users from "./components/users/Users";
import Navbar from "./components/navbar/Navbar";
import FormTemplates from "./components/formtemplates/FormTemplates";
import PendingRequests from "./components/pendingrequests/PendingRequests";
import Roles from "./components/roles/Roles";

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register}/>
        </Switch>

        <Switch>
          <Route exact path="/"><Navbar/><Home/></Route>
          <Route exact path="/formstructures"><Navbar/><FormStructures/></Route>
          <Route exact path="/users"><Navbar/><Users/></Route>
          <Route exact path="/roles"><Navbar/><Roles/></Route>
          {/* <Route exact path="/formtemplates"><Navbar/><FormTemplates/></Route>
          <Route exact path="/pendingrequests"><Navbar/><PendingRequests/></Route> */}
        </Switch>
      </div>
    </Router>
  );
}

export default App;
