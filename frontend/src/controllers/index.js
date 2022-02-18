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

export function useController() {
    const token = localStorage.getItem('access_token');

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