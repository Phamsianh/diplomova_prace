import Row from './row'
import "./overview.css"
import { Link } from 'react-router-dom'
import { ReadIcon, UpdateIcon } from '../icon' 
import { formatDate } from '../../utils/datetime'

const Overview = ({title="Title", data, to, update}) => {
    return (
        <div className='overview'>
            <h2>
                {title}
            </h2>
            {data?
                Object.entries(data).map( ([k, v]) => {
                    if (k === 'created_at' || k === 'updated_at') {
                        return <Row key={k} name={k} value={formatDate(v)}></Row>
                    }
                    if ( k === "public" || k === "obsolete") {
                        return <Row key={k} name={k} value={String(v)}></Row>
                    }
                    return <Row key={k} name={k} value={v}></Row>
                })
            :''}
            <div className="manage-form">
                <Link to={to}><ReadIcon/></Link>
                {update && <Link to={to + '/update'}><UpdateIcon/></Link>}
            </div>
        </div>
    )
}

export default Overview
