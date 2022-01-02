import { formatDate } from '../../utils/datetime';

export const ReadForm = ({ form_data }) => {
	return (
		<div className="read-form">
			<h1 className="name">{form_data.name}</h1>
			<details>
				<summary></summary>
				<p className="form-id">Form ID:{form_data.id}</p>
				<p className="creator-di">Creator ID: {form_data.creator_id}</p>
				<p className="created-at" title={form_data.created_at}>
					Created at: {formatDate(form_data.created_at)}
				</p>
				<p className="form-public">
					{form_data.public ? 'Public' : 'Private'}
				</p>
				<p className="form-obsolete">
					{form_data.obsolete ? 'Obsolete' : 'Up-to-date'}
				</p>
			</details>
		</div>
	);
};
