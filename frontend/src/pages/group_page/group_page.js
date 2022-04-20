import { Outlet } from 'react-router-dom';
import './main.css'

export const GroupPage = () => {
    return (
        <div className='group-page page'>
            <Outlet></Outlet>
        </div>
    )
}
