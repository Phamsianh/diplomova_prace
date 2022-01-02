import { useState, useEffect, useContext } from 'react';
import { CancelIcon, DeleteIcon, UpdateIcon } from '../icon';
import { ReadTransition } from './read_transition';

export const TransitionEditor = ({
	transition_data,
	handleDeleteTransition,
	handleUpdateTransition,
	cancelUpdateTransition,
}) => {
	const [current_transition_data, setCurrentTransitionData] =
		useState(transition_data);
	const [transition_component, setTransitionComponent] = useState(
		<ReadTransition transition_data={transition_data} />
	);
    const [toggle_update_transition_button, setToggleUpdateTransitionButton] = useState(true)

	return (
		<div className="transition">
			<div className="manage-buttons">
				{toggle_update_transition_button && <button
					title="Update Transition"
					onClick={() => {
                        handleUpdateTransition(		
                            current_transition_data, // state
                            setTransitionComponent,
                            setCurrentTransitionData,
                            setToggleUpdateTransitionButton
                        )
                        setToggleUpdateTransitionButton(false);
                    }}
				>
					<UpdateIcon />
				</button>}

				{toggle_update_transition_button && <button
					title="Delete Transition"
					onClick={() => handleDeleteTransition(transition_data.id)}
				>
					<DeleteIcon />
				</button>}
				
                {toggle_update_transition_button?'':<button
					title="Cancel Update"
					onClick={() => {
						console.log('cancel update');
                        setToggleUpdateTransitionButton(true);
						cancelUpdateTransition(current_transition_data, setTransitionComponent);
					}}
				>
					<CancelIcon />
				</button>}
			</div>

			{transition_component}
		</div>
	);
};
