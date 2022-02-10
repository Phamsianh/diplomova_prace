import React from 'react'
import "./row.css"

const Row = ({name, value}) => {
    return (
        <div className='row'>
            <p className="name">{name.split('_').join(' ')}</p>
            <p className="value">{value}</p>
        </div>
    )
}

export default Row
