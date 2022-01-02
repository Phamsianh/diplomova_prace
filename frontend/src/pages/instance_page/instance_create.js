import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useController } from '../../controllers';


const InstanceCreate = () => {
	const [forms_data, setFormsData] = useState([]);
	const [form_id, setFormId] = useState(1);
    const navigate = useNavigate();
	const {FormCtlr, InstanceCtlr} = useController();

	useEffect(() => {
		FormCtlr.get_rsc_col().then((data) => {
			setFormsData(data);
		});
	}, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        const req_bod = {
            form_id: e.target.form_id.value
        }
        InstanceCtlr.post_rsc(req_bod).then(data => {
            navigate(`/instances/${data.id}`)
        })
    }

	return (
		<div className="instance-create">
			<form onSubmit={handleSubmit}>
				<label htmlFor="form_id">Form Name</label>
				<select
					name="form_id"
					id="form_id"
                    value={form_id}
					onChange={(e) => {
						setFormId(e.target.value)
					}}
				>
					{forms_data.map((f_d) => {
						return (
							<option value={f_d.id} key={f_d.id}>
								{f_d.name}
							</option>
						);
					})}
				</select>
				<br />
				<button>Initialize</button>
			</form>
		</div>
	);
};

export default InstanceCreate;
