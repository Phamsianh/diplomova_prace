import { UserController } from './UserController';
import { FormController } from './FormController';
import { PhaseController } from './PhaseController';
import { TransitionController } from './TransitionController';
import { SectionController } from './SectionController';
import { FieldController } from './FieldController';
import { InstanceController } from './InstanceController';
import { InstanceFieldController } from './InstanceFieldController';
import { PositionController } from './PositionController';
import { CommitController } from './CommitController';
import { useNavigate } from 'react-router-dom';

// let token = localStorage.getItem('access_token');

// export const UserCtlr = new UserController(token);
// export const FormCtlr = new FormController(token);
// export const PhaseCtlr = new PhaseController(token);
// export const TransitionCtlr = new TransitionController(token);
// export const SectionCtlr = new SectionController(token);
// export const FieldCtlr = new FieldController(token);
// export const InstanceCtlr = new InstanceController(token);
// export const InstanceFieldCtlr = new InstanceFieldController(token);
// export const PositionCtlr = new PositionController(token);

export function useController() {
    const token = localStorage.getItem('access_token');
	const navigate = useNavigate();
	if (!token) {
		navigate('/login')
	}

    const UserCtlr = new UserController(token);
    const FormCtlr = new FormController(token);
    const PhaseCtlr = new PhaseController(token);
    const TransitionCtlr = new TransitionController(token);
    const SectionCtlr = new SectionController(token);
    const FieldCtlr = new FieldController(token);
    const InstanceCtlr = new InstanceController(token);
    const InstanceFieldCtlr = new InstanceFieldController(token);
    const PositionCtlr = new PositionController(token);
    const CommitCtlr = new CommitController(token);

	return {
		UserCtlr,
		FormCtlr,
		PhaseCtlr,
		TransitionCtlr,
		SectionCtlr,
		FieldCtlr,
		InstanceCtlr,
		InstanceFieldCtlr,
		PositionCtlr,
		CommitCtlr
	};
}