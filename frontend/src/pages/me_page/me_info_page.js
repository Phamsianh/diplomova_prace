import { useContext } from "react";
import { UserContext } from "../../App";

export const MeInfoPage = () => {
    const {user_data, held_positions} = useContext(UserContext)
    return (
    <div className='me-page'>
        {user_data && held_positions && <div>
            <h3>{user_data.first_name} {user_data.last_name}</h3>
            <p>Username: {user_data.user_name}</p>
            <p>Email: {user_data.email}</p>
            <p>Phone: {user_data.phone}</p>
            <p>Birthday: {user_data.birthdate}</p>
            <p>Held positions: {held_positions.map((hp, i) => hp.name + (i !== held_positions.length - 1 ? ", ": "."))}</p>
        </div>}
    </div>
    );
};
