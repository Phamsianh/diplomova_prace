import { Outlet } from 'react-router-dom';
import './main.css'

const RolePage = () => {
    return (
        <div className='role-page page'>
            <Outlet></Outlet>
        </div>
    )
}

export default RolePage
