import { UserController } from './UserController';
import { GroupController } from './GroupController';
import { RoleController } from './RoleController';
import { FormController } from './FormController';
import { PhaseController } from './PhaseController';
import { TransitionController } from './TransitionController';
import { SectionController } from './SectionController';
import { FieldController } from './FieldController';
import { InstanceController } from './InstanceController';
import { InstanceFieldController } from './InstanceFieldController';
import { PositionController } from './PositionController';
import { CommitController } from './CommitController';
import { ReceiverController } from './ReceiverController';
import { UserPositionController } from './UserPositionController';

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
    const GroupCtlr = new GroupController(token);
    const RoleCtlr = new RoleController(token);
    const PositionCtlr = new PositionController(token);
    const CommitCtlr = new CommitController(token);
    const ReceiverCtlr = new ReceiverController(token);
	const UserPositionCtlr = new UserPositionController(token);

	return {
		UserCtlr,
		GroupCtlr,
		RoleCtlr,
		FormCtlr,
		PhaseCtlr,
		TransitionCtlr,
		SectionCtlr,
		FieldCtlr,
		InstanceCtlr,
		InstanceFieldCtlr,
		PositionCtlr,
		CommitCtlr,
		ReceiverCtlr,
		UserPositionCtlr
	};
}