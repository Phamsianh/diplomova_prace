import React from 'react';
import Overview from '../overview/overview';
import './tab.css';

const Tab = ({ name, overview_data, title, rsc_name }) => {
	return (
		<div className="tab">
			<summary>
				<h1>{name}</h1>
			</summary>
			<details>
				<div className="detail">
					{overview_data
						? overview_data.map((o_d, index) => {
								return (
									<Overview
										key={index}
										title={`${title} ${o_d.id}`}
										data={o_d}
										to={`/${rsc_name}/${o_d.id}`}
									></Overview>
								);
						  })
						: ''}
				</div>
			</details>
		</div>
	);
};

export default Tab;
