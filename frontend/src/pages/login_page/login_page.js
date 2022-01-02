import { Outlet } from 'react-router-dom'
import './main.css'

export const LoginPage = () => {
    return (
        <div className='login-page page'>
            <Outlet></Outlet>
        </div>
    )
}
