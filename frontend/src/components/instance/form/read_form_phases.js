import { useState, useEffect } from 'react';
import { useController } from '../../../controllers';
import { ReadForm } from '../../form/read_form';
import { PhasesData } from '../../form/read_form_phases';
import { ReadPhaseSections } from './read_phase_sections';

export const ReadFormPhases = ({ form_data }) => {
	const [phasesdata, setPhasesdata] = useState();
	const {FormCtlr} = useController();
	
	useEffect(() => {
		FormCtlr.get_rel_rsc(form_data.id, 'phases').then((data) => {
			setPhasesdata(data);
		});
	}, []);
	
	return (
		<div className='form'>
			<ReadForm form_data={form_data} />
			<div className="phases">
				{phasesdata &&
					phasesdata.map((pd) => {
						return <ReadPhaseSections phase_data={pd} key={pd.id}/>
					})}
			</div>
		</div>
	);
};
