import { useState, useEffect } from 'react';
import { PhaseCtlr } from '../controllers';

export async function usePhase() {
	const [phases_data, setPhasesData] = useState([]);
	const [toggle_phase_creator, setTogglePhaseCreator] = useState(false);

	const createPhase = (e, form_id) => {
		e.preventDefault();
		const req_bod = {
			form_id: form_id,
			name: e.target.name.value,
			description: e.target.description.value,
			position_id: e.target.position_id.value,
			phase_type: e.target.phase_type.value,
		};
		setTogglePhaseCreator(false);
		PhaseCtlr.post_rsc(req_bod).then((data) => {
			setPhasesData(phases_data.concat(data));
		});
	};

	const enablePhaseCreator = () => {
		setTogglePhaseCreator(true);
	};
	const disablePhaseCreator = () => {
		setTogglePhaseCreator(false);
	};

	const handleDeletePhase = (phase_id) => {
		PhaseCtlr.delete_rsc_ins(phase_id).then((data) => {
			console.log(data);
		});
	};

	return {
		phases_data,
		setPhasesData,
		toggle_phase_creator,
		setTogglePhaseCreator,
		createPhase,
		enablePhaseCreator,
		disablePhaseCreator,
		handleDeletePhase,
	};
}
