import { useState, useEffect, useContext } from 'react';
import ReadFieldContent from './read_field_content';
import ReadSection from '../../section/read_section';
import { InstanceContentContext } from '../../../pages/instance_page/read_instance_page';
import UpdateFieldContent from './update_field_content';
import { useController } from '../../../controllers';
import { UserContext } from '../../../App';

export const ReadSectionFields = ({ section_data }) => {
	const { page, instance_data, content_data } = useContext(
		InstanceContentContext
	);
	const { user_data } = useContext(UserContext);
	const { SectionCtlr } = useController();
	const [fieldsdata, setFieldsdata] = useState([]);

	useEffect(() => {
		SectionCtlr.get_rel_rsc(section_data.id, 'fields').then((data) => {
			setFieldsdata(data);
		});
	}, []);

	return (
		<div className="section">
			<ReadSection section_data={section_data} />
			<div className="fields">
				{fieldsdata &&
					instance_data &&
					fieldsdata.map((fd) => {
						if (page === 'read') {
							return (
								<ReadFieldContent key={fd.id} field_data={fd} />
							);
						} else {
							// only return UpdateFieldContent when:
							// 1. this section is in current phase of instance
							// 2. content data exist
							// 3. user is creator of this content data
							if (
								instance_data.current_phase_id ===
									section_data.phase_id &&
								content_data.find(
									(cd) =>
										cd.field_id === fd.id &&
										cd.creator_id === user_data.id
								)
							) {
								return (
									<UpdateFieldContent
										key={fd.id}
										field_data={fd}
									/>
								);
							} else {
								return (
									<ReadFieldContent
										key={fd.id}
										field_data={fd}
									/>
								);
							}
						}
					})}
			</div>
		</div>
	);
};
