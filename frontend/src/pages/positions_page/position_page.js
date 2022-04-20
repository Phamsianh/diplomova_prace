import { Outlet } from 'react-router-dom';
import './main.css'

const PositionPage = () => {
    return (
        <div className='position-page page'>
            <Outlet></Outlet>
        </div>
    )
}

export default PositionPage
