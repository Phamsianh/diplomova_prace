import React, { useContext } from 'react';
import { UserContext } from '../../App';
import Overview from '../overview/overview';
import './tab.css';

const Tab = ({ name, overview_data, title, rsc_name }) => {
	const {user_data} = useContext(UserContext)
	return (
		<div className="tab">
			{/* <summary> */}
				<h1>{name}</h1>
			{/* </summary>
			<details> */}
				<div className="detail">
					{overview_data
						? overview_data.map((o_d) => {
								return (
									<Overview
										key={o_d.id}
										title={`${title} ${o_d.id}`}
										data={o_d}
										to={`/${rsc_name}/${o_d.id}`}
										update={o_d.creator_id == user_data?.id && !(rsc_name == 'instances')}
									></Overview>
								);
						  })
						: ''}
				</div>
			{/* </details> */}
		</div>
	);
};

export default Tab;
