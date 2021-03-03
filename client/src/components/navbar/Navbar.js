import { Link, useHistory } from "react-router-dom";
import { delete_cookie } from "../../cookies_parser"

const Navbar = () => {
  const linknames = ["Form Structures", "Users", "Roles"/*, "Form Templates", "Pending Requests"*/];
  const linklists = linknames.map((linkname, index) => {
    const link = '/' + linkname.split(' ').join('').toLowerCase();
    return <li key={index}>
      <Link to={link} className="btn bd-round" href="#">
        {linkname}
      </Link>
    </li>;
  });

  const history = useHistory();
  const handleLogout = () => {
    console.log('logout');
    delete_cookie('user_id');
    history.push('/login');
  }
  return (
    <nav className="bg-grey bd-round box-shadow pd_4">
      <div className="logo">
        <Link to='/' className='btn bd-round'>Home</Link>
      </div>
      <ul>
        {linklists}
      </ul>
      <button className='btn bd-round' onClick={handleLogout}>Logout</button>
    </nav>
  );
};

export default Navbar;
