import { useState, useEffect, createContext } from 'react';
// import { FormCtlr } from '../../controllers';
import { ReadForm } from './read_form';
// import { ReadPhaseSections } from '../phase/read_phase_sections';
import { ReadPhaseSectionsTransitions } from '../phase/read_phase_sections_transitions';
import { useController } from '../../controllers';
import { InitInstanceIcon } from '../icon';
import { useNavigate } from 'react-router-dom';

export const PhasesData = createContext();

export const ReadFormPhases = ({ form_data }) => {
	const [phasesdata, setPhasesdata] = useState();
	const {FormCtlr, InstanceCtlr} = useController();
	const navigate = useNavigate()

	useEffect(() => {
		FormCtlr.get_rel_rsc(form_data.id, 'phases').then((data) => {
			setPhasesdata(data);
		});
	}, []);

	return (
		<>
		{phasesdata && 
			<PhasesData.Provider value={phasesdata}>
				<ReadForm form_data={form_data} />
				<div className="phases">
					{phasesdata &&
						phasesdata.map((pd) => {
							return <ReadPhaseSectionsTransitions phase_data={pd} key={pd.id}/>
						})}
				</div>
			</PhasesData.Provider>}
		</>
	);
};
