import { useState, useEffect } from 'react';
import { FormCtlr } from '../../controllers';
import { ReadForm } from './read_form';
import { ReadPhaseSections } from '../phase/read_phase_sections';
import { ReadTransition } from '../transition/read_transition';

export const ReadFormPhasesTransitions = ({ form_data }) => {
	const [phasesdata, setPhasesdata] = useState();
	const [transitionssdata, setTransitionsdata] = useState();

	useEffect(() => {
		FormCtlr.get_rel_rsc(form_data.id, 'phases').then((data) => {
			setPhasesdata(data);
		});
		FormCtlr.get_rel_rsc(form_data.id, 'transitions').then(data => {
			setTransitionsdata(data);
		})
	}, []);
	return (
		<>
			<ReadForm form_data={form_data} />
			<div className="phases">
				{phasesdata &&
					phasesdata.map((pd) => {
						return <ReadPhaseSections phase_data={pd} key={pd.id}/>
				})}
				{transitionssdata && 
					transitionssdata.map(td => {
						return <ReadTransition transition_data={td} key={td.id}/>
					})
				}
			</div>
		</>
	);
};
