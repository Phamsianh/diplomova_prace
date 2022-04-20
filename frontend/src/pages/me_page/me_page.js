import { Outlet } from "react-router-dom";
import './main.css'
export const MePage = () => {
    return (
    <div className='instance-page page'>
        <Outlet></Outlet>
    </div>
    );
};
