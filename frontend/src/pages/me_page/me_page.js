import { Outlet } from "react-router-dom";

export const MePage = () => {
    return (
    <div className='instance-page page'>
        <Outlet></Outlet>
    </div>
    );
};
