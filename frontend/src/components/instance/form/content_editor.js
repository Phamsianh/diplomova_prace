import { useState } from 'react';
// import { InstanceFieldCtlr } from '../../../controllers';
import { ReadContent } from './read_content';
import UpdateContent from './update_content';
import { CancelIcon, UpdateIcon } from '../../icon';
import { useController } from '../../../controllers';

const ContentEditor = ({ content_data }) => {
	const [current_content_data, setCurrentContentData] = useState(content_data);
	const [content_component, setContentComponent] = useState(
		<ReadContent content_data={content_data} />
	);
	const [toggle_update_button, setToggleUpdateButton] = useState(true);
	const {InstanceFieldCtlr} = useController();

	const handleUpdateContentEditor = () => {
		setToggleUpdateButton(false);
		setContentComponent(
			<UpdateContent
				old_content_data={current_content_data}
				handleUpdateContent={updateContent}
			/>
		);
	};

	const updateContent = async (e) => {
		e.preventDefault();
		const req_bod = {
			value: e.target.value.value,
			resolved: e.target.resolved.checked,
		};
		let data = await InstanceFieldCtlr.patch_rsc_ins(content_data.id, req_bod)
		console.log('updated content data', data);
		setCurrentContentData(data);
		setContentComponent(<ReadContent content_data={data}/>)
		setToggleUpdateButton(true);
	};

	const cancelUpdateContentEditor = () => {
		setContentComponent(<ReadContent content_data={current_content_data} />)
		setToggleUpdateButton(true)
	}

	return (
		<div className="content">
			<div className="manage-buttons">
				{toggle_update_button && (
					<button onClick={handleUpdateContentEditor}><UpdateIcon/></button>
				)}
				{toggle_update_button ? '' : <button onClick={cancelUpdateContentEditor}><CancelIcon/></button>}
			</div>

			{content_component}
		</div>
	);
};

export default ContentEditor;
