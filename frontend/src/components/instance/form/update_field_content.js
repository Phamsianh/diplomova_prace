import ReadField from '../../field/read_field';
import { useState, useContext, useEffect } from 'react';
import { InstanceContentContext } from '../../../pages/instance_page/read_instance_page';
import { ReadContent } from './read_content';
import UpdateContent from './update_content';
import { useController } from '../../../controllers';
import { UpdateIcon, CancelIcon } from '../../icon';

const UpdateFieldContent = ({ field_data }) => {
	const {
		content_data: instance_contents,
		setContentData: setInstanceContentsData,
		instance_data,
		setInstanceData,
	} = useContext(InstanceContentContext);
	const [content_data, setContentData] = useState(
		instance_contents.find((ic) => {
			return ic.field_id === field_data.id;
		})
	);
	const [is_updating, setIsUpdating] = useState(false);
	const { InstanceFieldCtlr, InstanceCtlr } = useController();

	const handleUpdateContent = () => {
		setIsUpdating(true);
	};

	const updateContent = async (e) => {
		// updateContent include:
		// 1. setContentData in this UpdateFieldContent to updated content data
		e.preventDefault();
		const req_bod = {
			value: e.target.value.value,
			resolved: e.target.resolved.checked,
		};
		let data = await InstanceFieldCtlr.patch_rsc_ins(
			content_data.id,
			req_bod
		);
		console.log('updated content data', data);
		setContentData(data);
		setIsUpdating(false);

		// 2. update content_data in InstanceContentContext.
		// Will effect ReadFieldContent or UpdateFieldContent in it's next rerender
		setInstanceContentsData(instance_contents.map(ics => {
			return ics.id === data.id? data: ics
		}))

		//  3. update instance_data in InstanceContentContext. 
		//  Will trigger rerender ReadSectionField, hence ReadFieldContent or UpdateFieldContent.
		let instance_current_state = await InstanceCtlr.get_rel_rsc(
			instance_data.id,
			'current_state'
		);
		let ins_dat = Object.assign({}, instance_data);
		ins_dat.current_state = instance_current_state;
		setInstanceData(ins_dat);
	};

	const cancelUpdateContent = () => {
		setIsUpdating(false);
	};
	return (
		<div className="field">
			<ReadField field_data={field_data} />
			{content_data && (
				<div className="content">
					<div className="manage-buttons">
						{is_updating? '' : (
							<button onClick={handleUpdateContent}>
								<UpdateIcon />
							</button>
						)}
						{is_updating && (
							<button onClick={cancelUpdateContent}>
								<CancelIcon />
							</button>
						)}
					</div>

					{content_data && (is_updating ? '' : (
						<ReadContent content_data={content_data} />
					))}
					{content_data && is_updating && (
						<UpdateContent
							old_content_data={content_data}
							handleUpdateContent={updateContent}
						/>
					)}
				</div>
			)}
		</div>
	);
};

export default UpdateFieldContent;
