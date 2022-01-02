import { formatDate } from '../../utils/datetime';

const ReadField = ({ field_data }) => {
	return (
		<div className="read-field">
			<h3>{field_data.name ? field_data.name : 'Field Name'}</h3>
			<details>
				<summary></summary>
				<p>Field ID: {field_data.id}</p>
				<p className="created-at" title={field_data.created_at}>
					Created at: {formatDate(field_data.created_at)}
				</p>
			</details>
		</div>
	);
};

export default ReadField;
