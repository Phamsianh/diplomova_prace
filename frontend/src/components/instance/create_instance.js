import {useEffect, useState} from 'react'
// import { FormCtlr, InstanceCtlr } from '../../controllers';
import { useNavigate } from 'react-router-dom'
import { useController } from '../../controllers';

export const CreateInstance = () => {
    const [forms, setForms] = useState();
    const navigate = useNavigate();
    const {FormCtlr, InstanceCtlr} = useController();

    useEffect(() => {
        FormCtlr.get_rsc_col().then(data => {
            console.log(data);
            setForms(data)
        })
    }, [])

    const createInstance = async (e) => {
        e.preventDefault();
        const req_bod = {
            form_id: e.target.form_id.value
        }
        let data = await InstanceCtlr.post_rsc(req_bod)
        navigate('/instances/' + data.id)
    }

    return (
        <div className='create-instance'>
            <form onSubmit={createInstance}>
                <label htmlFor='form_id'>Form</label>
                <select name="form_id" id="form_id">
                    {forms && forms.map(f => {
                        return <option key={f.id} value={f.id}>{f.name}</option>
                    })}
                </select>
                <input type="submit" value="Create" />
            </form>
        </div>
    )
}
