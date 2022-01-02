import ReadField from '../../field/read_field';
import { useState, useContext, useEffect } from 'react';
import { InstanceContentContext } from '../../../pages/instance_page/read_instance_page';
import { ReadContent } from './read_content';

const ReadFieldContent = ({ field_data }) => {
	const {content_data: instance_contents} = useContext(InstanceContentContext);
	console.log('instance_contents', instance_contents);
	const [content_data, setContentData] = useState(instance_contents.find((ic) => {
		return ic.field_id == field_data.id;
	}))

	return (
		<div className='field'>
			<ReadField field_data={field_data} />
            {content_data && <div className="content">
				<ReadContent content_data={content_data}/>
			</div>}
		</div>
	);
};

export default ReadFieldContent;
