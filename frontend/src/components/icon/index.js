import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
	faEdit,
	faTrash,
	faPlus,
	faEye,
	faSave,
	faTimes,
	faCheckCircle,
	faExchangeAlt,
	faUserEdit,
    faFileSignature,
	faHome,
	faUser,
	faFile,
	faFileAlt,
	faSignInAlt,
	faSignOutAlt,
	faCircle as fasCircle,
	faEllipsisV,
	faEllipsisH,
	faFileMedical,
	faFilePdf,
	faCheck,
	faBars,
} from '@fortawesome/free-solid-svg-icons';
import { faCircle } from '@fortawesome/free-regular-svg-icons';
export const CreateIcon = () => {
	return <FontAwesomeIcon icon={faPlus} title="Create" />;
};

export const ReadIcon = () => {
	return <FontAwesomeIcon icon={faEye} title="Read" />;
};

export const UpdateIcon = () => {
	return <FontAwesomeIcon icon={faEdit} title="Update" />;
};

export const DeleteIcon = () => {
	return <FontAwesomeIcon icon={faTrash} title="Delete" />;
};

export const CancelIcon = () => {
	return <FontAwesomeIcon icon={faTimes} title="Cancel" />;
};

export const SaveIcon = () => {
	return <FontAwesomeIcon icon={faSave} title="Save" />;
};

export const InitInstanceIcon = () => {
	return <FontAwesomeIcon icon={faFileMedical} title='Init Instance' />
}

export const ResolvedIcon = () => {
	return (
		<FontAwesomeIcon
			icon={faCheckCircle}
			title="Resolved"
			size="lg"
			color="#0a3d62"
		/>
	);
};

export const ResolvingIcon = () => {
	return (
		<FontAwesomeIcon
			icon={faCircle}
			title="Resolved"
			size="lg"
			color="#0a3d62"
		/>
	);
};

export const TransitInstanceIcon = () => {
	return <FontAwesomeIcon icon={faExchangeAlt} title="Transit" />;
};

export const ReceiveInstanceIcon = () => {
	return <FontAwesomeIcon icon={faUserEdit} title="Receive" />;
};

export const HandleInstanceIcon = () => {
	return <FontAwesomeIcon icon={faFileSignature} title="Handle" />;
};

export const HomePageIcon = () => {
	return <FontAwesomeIcon icon={faHome} title="Home" />;
};

export const FormPageIcon = () => {
	return <FontAwesomeIcon icon={faFile} title="Form Page" />;
};

export const InstancePageIcon = () => {
	return <FontAwesomeIcon icon={faFileAlt} title="Instance Page" />;
};

export const LogoutPageIcon = () => {
	return <FontAwesomeIcon icon={faSignOutAlt} title="Log out" />;
};

export const LoginPageIcon = () => {
	return <FontAwesomeIcon icon={faSignInAlt} title="Log in" />;
};

export const UserPageIcon = () => {
	return <FontAwesomeIcon icon={faUser} title="User Page" />;
}

export const SubpageIcon = () => {
	return (
		<FontAwesomeIcon
			icon={fasCircle}
			title="Subpage"
			size="xs"
		/>
	);
};

export const CommitsPageIcon = () => {
	return <FontAwesomeIcon icon={faEllipsisV} title="Commits Page" />;
}

export const CommitIcon = () => {
	return <FontAwesomeIcon icon={fasCircle} title="Commits Page" />;
}

export const OptionIcon = () => {
	return <FontAwesomeIcon icon={faEllipsisH} title="Options" />;
}

export const PrintPDFIcon = () => {
	return <FontAwesomeIcon icon={faFilePdf} title="Print Form" />;
}

export const YesIcon = () => {
	return <FontAwesomeIcon icon={faCheck} title="Yes" />;
}

export const NoIcon = () => {
	return <FontAwesomeIcon icon={faTimes} title="No" />;
}

export const MenuBarIcon = () => {
	return <FontAwesomeIcon icon={faBars} title="Menu" />;
}