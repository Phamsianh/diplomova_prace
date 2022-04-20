import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/navbar/navbar';
import { Hnavbar } from './components/hnavbar/hnavbar';
import HomePage from './pages/home_page/home_page1';

import FormPage from './pages/form_page/form_page';
import AllFormsPage from './pages/form_page/all_forms_page';
import CreateFormPage from './pages/form_page/create_form_page';
import ReadFormPage from './pages/form_page/read_form_page';
// import ReadFormPage from './pages/form_page/read_form_page1';
import UpdateFormPage from './pages/form_page/update_form_page';

import InstancePage from './pages/instance_page/instance_page';
import AllInstancesPage from './pages/instance_page/all_instances_page';
import { CreateInstancePage } from './pages/instance_page/create_instance_page';
import { UpdateInstancePage } from './pages/instance_page/update_instance_page';

import { LoginPage } from './pages/login_page/login_page';
import { LoginIndex } from './pages/login_page';

import { createContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { NotFoundPage } from './pages/not_found_page/not_found_page';

import { MeInfoPage } from './pages/me_page/me_info_page';
import { ChangePassword } from './pages/me_page/change_password';
import { MyFormsPage } from './pages/me_page/my_forms_page';
import { MyInstancesPage } from './pages/me_page/my_instances_page';
import { MyParticipatedInstancesPage } from './pages/me_page/my_participated_instance';
import { MyPendingInstancesPage } from './pages/me_page/my_pending_instances';

import { UserController } from './controllers/UserController';
import { SignUp } from './pages/login_page/signup';
import { GroupPage } from './pages/group_page/group_page';
import { CreateGroupPage } from './pages/group_page/create_group_page';
import { AllGroupsPage } from './pages/group_page/all_groups_page';
import RolePage from './pages/role_page/role_page';
import { AllRolesPage } from './pages/role_page/all_roles_page';
import PositionPage from './pages/positions_page/position_page';
import { AllPositionsPage } from './pages/positions_page/all_positions_page';
import './main.css';
import { Footer } from './components/footer/footer';
import { MePage } from './pages/me_page/me_page';

export const UserContext = createContext();

function App() {
	const location = useLocation();

	const [login, setLogin] = useState(false);
	const [user_data, setUserData] = useState();
	const [held_positions, setHeldPositions] = useState();

	const navigate = useNavigate();

	useEffect(() => {
		if (location.pathname === '/login' || location.pathname === '/login/signup') { 
			setLogin(true);
			return;
		}
		setLogin(false);
	}, [location]);

	useEffect(() => {
		let UserCtlr = new UserController(localStorage.getItem('access_token'))
		UserCtlr.get_rsc_ins('me').then((data) => {
			setUserData(data);
			UserCtlr.get_rel_rsc('me', 'held_positions').then((data) =>
				setHeldPositions(data)
			);
		}).catch(() => {
			if (location.pathname !== '/login/signup'){navigate('/login')}
		});
	}, [localStorage.getItem('access_token')])
	

	return (
		<div className="App">
			<div className="container">
				<UserContext.Provider value={{ user_data, held_positions }}>
					{login ? '' : <Navbar />}
					<div className="body">
						{login? '' :<Hnavbar/>}
						<Routes>
							<Route path="/login" element={<LoginPage />}>
								<Route path="signup" element={<SignUp />} />
								<Route path="" element={<LoginIndex />} />
							</Route>

							<Route path="/" element={<HomePage />} />
							<Route path="/me" element={<MePage/>}>
								<Route path="" element={<MeInfoPage/>} />
								<Route path="change_password" element={<ChangePassword/>} />
								<Route path="forms" element={<MyFormsPage/>} />
								<Route path="instances" element={<MyInstancesPage/>} />
								<Route path="participated_instances" element={<MyParticipatedInstancesPage/>} />
								<Route path="pending_instances" element={<MyPendingInstancesPage/>} />
							</Route>

							<Route path="/groups" element={<GroupPage />}>
								<Route path="" element={<AllGroupsPage />} />
							</Route>

							<Route path="/roles" element={<RolePage />}>
								<Route path="" element={<AllRolesPage />} />
							</Route>

							<Route path="/positions" element={<PositionPage />}>
								<Route path="" element={<AllPositionsPage />} />
							</Route>

							<Route path="/forms" element={<FormPage />}>
								<Route path="" element={<AllFormsPage />} />
								{/* <Route path="create" element={<CreateFormPage />} /> */}
								<Route path=":id" element={<ReadFormPage />} />
								<Route path=":id/update" element={<UpdateFormPage />} />
							</Route>

							<Route path="/instances" element={<InstancePage />}>
								<Route path="" element={<AllInstancesPage />} />
								<Route path="create" element={<CreateInstancePage />} />
								<Route path=":id" element={<UpdateInstancePage />} />
							</Route>
							<Route path="*" element={<NotFoundPage/>} />
						</Routes>
						{login? '' :<Footer/>}
					</div>
				</UserContext.Provider>
			</div>
		</div>
	);
}

export default App;
