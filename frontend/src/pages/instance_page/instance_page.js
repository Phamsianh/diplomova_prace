import { Outlet } from 'react-router-dom'
import './main.css'
const InstancePage = () => {
    return (
        <div className='instance-page page'>
            <Outlet></Outlet>
        </div>
    )
}

export default InstancePage
