import React from 'react'
import { Link } from 'react-router-dom'

const NavEle = ({to, name}) => {
    return (
        <div className="nav-ele">
            <Link to={to}>{name}</Link>
        </div>
    )
}

export default NavEle
