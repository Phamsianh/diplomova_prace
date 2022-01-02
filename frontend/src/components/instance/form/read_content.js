import { ResolvedIcon, ResolvingIcon } from '../../icon';

export const ReadContent = ({ content_data }) => {
	const { value, resolved } = content_data;
	return (
		<div className="read-content">
			<div className="value">{value}</div>
			<div className="resolved">{resolved? <ResolvedIcon />: <ResolvingIcon/>}</div>
		</div>
	);
};
