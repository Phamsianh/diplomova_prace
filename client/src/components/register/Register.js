import { useEffect, useState } from "react";
import { useHistory } from 'react-router-dom';

const Register = () => {
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [user_name, setUserName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirm_password, setConfirmPassword] = useState('');
    const [phone, setPhone] = useState('');

    const history = useHistory();


    const handleSubmit = (e) => {
        e.preventDefault();
        const formdata = new URLSearchParams({first_name, last_name, user_name, email, password, confirm_password, phone});
        console.log(formdata.toString());

        fetch('http://localhost:8888/register',{
            method: 'POST',
            mode: 'cors',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: formdata,
        }).then(res => res.json())
        .then(data => {
            console.log(data)
            if(data.register){
                history.push('/login');
            }
            else{
                console.log(data.error)
            }
        })
    }

    return (
    <div className="container flex-center height-100 mg_4">
        <form 
            onSubmit = {handleSubmit}
            className="flex-center flex-direction-column width-60 height-60 bg-grey box-shadow bd-round">
            <label className="flex-center flex-direction-column width-80 pd_1">
                First name
                <input
                    required
                    value = {first_name}
                    onChange = {(e) => setFirstName(e.target.value)}
                    type="text" 
                    name="first_name" 
                    placeholder="First name"
                   className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                Last name
                <input 
                    required
                    value = {last_name}
                    onChange = {(e) => setLastName(e.target.value)}
                    type="text" 
                    name="last_name" 
                    placeholder="Last name"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                User name
                <input 
                    required
                    value = {user_name}
                    onChange = {(e) => setUserName(e.target.value)}
                    type="text" 
                    name="user_name" 
                    placeholder="User name"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                Email
                <input
                    required
                    value = {email}
                    onChange = {(e) => setEmail(e.target.value)}
                    type="text" 
                    name="email" 
                    placeholder="Email"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                Password
                <input
                    required 
                    value = {password}
                    onChange = {(e) => setPassword(e.target.value)}
                    type="password" 
                    name="password" 
                    placeholder="Password"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                Confirm password
                <input 
                    required
                    value = {confirm_password}
                    onChange = {(e) => setConfirmPassword(e.target.value)}
                    type="password" 
                    name="confirm_password" 
                    placeholder="Confirm password"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <label className="flex-center flex-direction-column width-80 pd_1">
                Phone
                <input 
                    required
                    value = {phone}
                    onChange = {(e) => setPhone(e.target.value)}
                    type="text" 
                    name="phone" 
                    placeholder="Phone"
                    className="display-block width-100 pd_2 bd-round"/>
            </label>
            <input 
            type="submit" 
            value="Submit" 
            className="btn bd-round"/>
        </form>
    </div>
    );
}
 
export default Register;