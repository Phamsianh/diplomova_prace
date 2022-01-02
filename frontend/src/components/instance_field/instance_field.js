import React from 'react';

const InstanceField = ({ instance_field_data }) => {

	return (
		<div className="instance-field">
			<input type="text" name="instance_field_value" id="{instance_field_data.id}" defaultValue={instance_field_data.value} />
            <div className="resolved">{instance_field_data.resolved? "resolved": "unresolved"}</div>
		</div>
	);
};

export default InstanceField;
