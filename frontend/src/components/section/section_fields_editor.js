import { useState, useEffect } from 'react';
import { FieldEditor } from '../field/field_editor';
import ReadSection from './read_section';
import CreateField from '../field/create_field';
import ReadField from '../field/read_field';
import UpdateField from '../field/update_field';
import { UpdateIcon, DeleteIcon, CancelIcon, CreateIcon } from '../icon';
import { useController } from '../../controllers';

export const SectionFieldsEditor = ({
	section_data,
	handleDeleteSection,
	handleUpdateSection,
	cancelUpdateSection,
}) => {
	const [fields_data, setFieldsData] = useState([]);
	const [toggle_field_creator, setToggleFieldCreator] = useState(false);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);
	const [current_section_data, setCurrentSectionData] =
		useState(section_data);
	const [section_component, setSectionComponent] = useState(
		<ReadSection section_data={section_data} />
	);
	const { SectionCtlr, FieldCtlr } = useController();

	useEffect(() => {
		SectionCtlr.get_rel_rsc(section_data.id, 'fields').then((data) => {
			setFieldsData(data);
		});
	}, []);

	const handleSubmit = (e) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
			section_id: section_data.id,
			order: !isNaN(e.target.order.value) ? 1 : e.target.order.value,
		};
		setToggleFieldCreator(false);
		FieldCtlr.post_rsc(req_bod).then((data) => {
			setFieldsData(fields_data.concat(data));
		});
	};
	const enableFieldCreator = () => {
		setToggleFieldCreator(true);
	};
	const disableFieldCreator = () => {
		setToggleFieldCreator(false);
	};

	const handleDeleteField = async (field_id) => {
		let data = await FieldCtlr.delete_rsc_ins(field_id);
		if (data === null) {
			setFieldsData(
				fields_data.filter((fd) => {
					return fd.id != field_id;
				})
			);
		}
	};

	const handleUpdateField = (
		current_field_data,
		setFieldComponent,
		setCurrentFieldData,
		setToggleUpdateButton
	) => {
		setFieldComponent(
			<UpdateField
				old_field_data={current_field_data}
				handleSubmit={(e) =>
					updateField(
						e,
						current_field_data.id,
						setFieldComponent,
						setCurrentFieldData,
						setToggleUpdateButton
					)
				}
			/>
		);
	};

	const updateField = async (
		e,
		field_id,
		setFieldComponent,
		setCurrentFieldData,
		setToggleUpdateButton
	) => {
		e.preventDefault();
		const req_bod = {
			name: e.target.name.value,
			order: !isNaN(e.target.order.value) ? 1 : e.target.order.value,
		};
		let data = await FieldCtlr.patch_rsc_ins(field_id, req_bod);
		setCurrentFieldData(data);
		setFieldComponent(<ReadField field_data={data} />);
		setToggleUpdateButton(true);
	};

	const cancelUpdateField = (current_field_data, setFieldComponent) => {
		setFieldComponent(<ReadField field_data={current_field_data} />);
	};

	return (
		<div className="section">
			<div className="manage-buttons">
				{toggle_update_button && (
					<button
						onClick={() => {
							setToggleUpdateButton(false);
							handleUpdateSection(
								current_section_data,
								setSectionComponent,
								setCurrentSectionData,
								setToggleUpdateButton
							);
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
							setToggleUpdateButton(true);
							cancelUpdateSection(
								current_section_data,
								setSectionComponent
							);
						}}
					>
						<CancelIcon />
					</button>
				)}
				{toggle_update_button && (
					<button
						onClick={() => handleDeleteSection(section_data.id)}
					>
						<DeleteIcon />
					</button>
				)}
			</div>
			{section_component}

			<div className="fields">
				{fields_data.map((fd) => {
					return (
						<FieldEditor
							key={fd.id}
							field_data={fd}
							handleDeleteField={handleDeleteField}
							handleUpdateField={handleUpdateField}
							cancelUpdateField={cancelUpdateField}
						/>
					);
				})}
				{toggle_field_creator && (
					<CreateField handleCreate={handleSubmit} cancelCreate={disableFieldCreator}/>
				)}
				{toggle_field_creator ? (
					''
				) : (
					<button onClick={enableFieldCreator} title='New Field'><CreateIcon/></button>
				)}
			</div>
		</div>
	);
};
