import ReadField from './read_field';
import { useState } from 'react';
import { UpdateIcon, DeleteIcon, CancelIcon } from '../icon';

export const FieldEditor = ({
	field_data,
	handleDeleteField,
	handleUpdateField,
	cancelUpdateField,
}) => {
	const [current_field_data, setCurrentFieldData] = useState(field_data);
	const [field_component, setFieldComponent] = useState(
		<ReadField field_data={field_data} />
	);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);

	return (
		<div className="field">
			<div className="manage-buttons">
				{toggle_update_button && (
					<button
						onClick={() => {
							handleUpdateField(
								current_field_data,
								setFieldComponent,
								setCurrentFieldData,
								setToggleUpdateButton
							);
							setToggleUpdateButton(false);
						}}
					>
						<UpdateIcon />
					</button>
				)}
				{toggle_update_button ? (
					''
				) : (
					<button
						onClick={() => {
							cancelUpdateField(
								current_field_data,
								setFieldComponent
							);
							setToggleUpdateButton(true);
						}}
					>
						<CancelIcon />
					</button>
				)}
				{toggle_update_button && (
					<button onClick={() => handleDeleteField(field_data.id)}>
						<DeleteIcon />
					</button>
				)}
			</div>
			{field_component}
		</div>
	);
};
