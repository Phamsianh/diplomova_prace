import { useState } from 'react';
import { SaveIcon } from '../../icon';

const UpdateContent = ({ old_content_data, handleUpdateContent }) => {
	const [value, setValue] = useState(old_content_data.value);
	const [resolved, setResolved] = useState(old_content_data.resolved);

	return (
		<div className="update-content" key={old_content_data.id}>
			<form onSubmit={handleUpdateContent}>
				<div className="value">
					{/* <input
						id="value"
						type="text"
						value={value === null ? '' : value}
						onChange={(e) => setValue(e.target.value)}
					/> */}
					<textarea
						id="value"
						type="text"
						value={value === null ? '' : value}
						onChange={(e) => setValue(e.target.value)}
					/>
					<input
						id="resolved"
						className="resolved"
						type="checkbox"
						checked={resolved}
						onChange={(e) => setResolved(e.target.checked)}
					/>
				</div>
				<br />
				<button type="submit">
					<SaveIcon />
				</button>
			</form>
		</div>
	);
};

export default UpdateContent;
