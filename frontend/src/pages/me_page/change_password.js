import {useState, useEffect, useContext} from 'react'
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../../App'
import { CancelIcon, SaveIcon } from '../../components/icon';
import domain from '../../config';
import { useController } from '../../controllers';

export const ChangePassword = () => {
    const {user_data} = useContext(UserContext)
    const [error, setError] = useState();
    const [old_password, setOldPassword] = useState('');
    const [new_password, setNewPassword] = useState('');
    const [new_password_again, setNewPasswordAgain] = useState('');
    const {UserCtlr} = useController();
    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        if (new_password !== new_password_again) {
            setError("Please retype your new password"); return;
        }
        if (old_password === new_password) {
            setError("New password must not be the same as old password"); return;
        }
        const password_regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,100}$/
        if (!password_regex.test(new_password)){
            setError("Password must contain at least 8 characters, at least 1 uppercase letter, 1 lower letter, 1 number and can contain special character"); return;
        }

        let url = domain + '/token'
        const form_data =  new FormData();
        form_data.append('username', user_data.user_name)
        form_data.append('password', new_password)
		const res = await fetch(url, {
		    method: 'POST',
		    'content-type': 'application/x-www-form-urlencoded',
		    mode: 'cors',
		    body: form_data,
		})
		if (!res.ok) {
			setError("Old password not true");return;
		}

        const req_bod = {
            password: e.target.new_password.value
        }
        let data = await UserCtlr.patch_rsc_ins('me', req_bod).catch(e => {
            throw new Error('Fail to change password')
        })
        navigate('/me')
    }
    function clearError(e) {
        e.preventDefault();
        setError('');
    }
  return (
    <div className='change-password-page page'>
        <form onSubmit={handleSubmit}>
            <div className={error? 'error show-error': "error"}>
                <div>
                    <h4>{error && error}</h4>
                    <button onClick={clearError}><CancelIcon/></button>
                </div>
            </div>
            <label>
                Old password
                <input type="password" name="old_password" id="old_password" value={old_password} onChange={e => setOldPassword(e.target.value)} required/>
            </label>
            <label>
                New password
                <input type="password" name="new_password" id="new_password" value={new_password} onChange={e => setNewPassword(e.target.value)} required/>
            </label>
            <label>
                Retype new password
                <input type="password" name="new_password_again" id="new_password_again" value={new_password_again} onChange={e => setNewPasswordAgain(e.target.value)} required/>
            </label>
            <button type="submit"><SaveIcon/></button>
        </form>
    </div>
  )
}
