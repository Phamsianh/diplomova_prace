import React from 'react'
import "./row.css"

const Row = ({name, value}) => {
    return (
        <div className='row'>
            <p className="name">{name}</p>
            <p className="value">{value}</p>
        </div>
    )
}

export default Row
