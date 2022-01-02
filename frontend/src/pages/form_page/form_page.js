import { Outlet } from 'react-router-dom';
import './main.css'

const FormPage = () => {
    return (
        <div className='form-page page'>
            <Outlet></Outlet>
        </div>
    )
}

export default FormPage
