import { formatDate } from '../../utils/datetime';

const ReadSection = ({ section_data }) => {
	return (
		<div className="read-section">
			<h2 className="name">
				{section_data.name ? section_data.name : 'Section Name'}
			</h2>
			<details>
				<summary></summary>
				<p className="section-id">Section ID:{section_data.id}</p>
				<p className="created-at" title={section_data.created_at}>
					Created at: {formatDate(section_data.created_at)}
				</p>
				<p className="position-id">
					Position ID: {section_data.position_id}
				</p>
			</details>
		</div>
	);
};

export default ReadSection;
