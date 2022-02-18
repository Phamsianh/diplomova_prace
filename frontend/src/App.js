import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/navbar/navbar';
import { Hnavbar } from './components/hnavbar/hnavbar';
import HomePage from './pages/home_page/home_page';

import FormPage from './pages/form_page/form_page';
import AllFormsPage from './pages/form_page/all_forms_page';
import CreateFormPage from './pages/form_page/create_form_page';
import ReadFormPage from './pages/form_page1/read_form_page';
import UpdateFormPage from './pages/form_page1/update_form_page';

import InstancePage from './pages/instance_page/instance_page';
import AllInstancesPage from './pages/instance_page/all_instances_page';
import { CreateInstancePage } from './pages/instance_page/create_instance_page';
import { UpdateInstancePage } from './pages/instance_page1/read_instance_page';

import { LoginPage } from './pages/login_page/login_page';
import { LoginIndex } from './pages/login_page';

import { createContext, useEffect, useState } from 'react';
import { useController } from './controllers';
import { useNavigate } from 'react-router-dom';

import { NotFoundPage } from './pages/not_found_page/not_found_page';

import { MeInfoPage } from './pages/me_page/me_info_page';
import { MyFormsPage } from './pages/me_page/my_forms_page';
import { MyInstancesPage } from './pages/me_page/my_instances_page';
import { MyParticipatedInstancesPage } from './pages/me_page/my_participated_instance';
import { MyPendingInstancesPage } from './pages/me_page/my_pending_instances';

import './main.css';
import { UserController } from './controllers/UserController';

export const UserContext = createContext();

function App() {
	const location = useLocation();

	const [login, setLogin] = useState(false);
	const [user_data, setUserData] = useState();
	const [held_positions, setHeldPositions] = useState();

	const navigate = useNavigate();

	useEffect(() => {
		if (location.pathname === '/login') { console.log("login"); setLogin(true); return }
		setLogin(false);
	}, [location]);

	useEffect(() => {
		console.log('access token change');
		let UserCtlr = new UserController(localStorage.getItem('access_token'))
		UserCtlr.get_rsc_ins('me').then((data) => {
			setUserData(data);
			UserCtlr.get_rel_rsc('me', 'held_positions').then((data) =>
				setHeldPositions(data)
			);
		}).catch(() => navigate('/login'));
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
								<Route path="" element={<LoginIndex />} />
							</Route>

							<Route path="/" element={<HomePage />} />
							<Route path="me">
								<Route path="" element={<MeInfoPage/>} />
								<Route path="forms" element={<MyFormsPage/>} />
								<Route path="instances" element={<MyInstancesPage/>} />
								<Route path="participated_instances" element={<MyParticipatedInstancesPage/>} />
								<Route path="pending_instances" element={<MyPendingInstancesPage/>} />
							</Route>

							<Route path="/forms" element={<FormPage />}>
								<Route path="" element={<AllFormsPage />} />
								<Route path="create" element={<CreateFormPage />} />
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
					</div>
				</UserContext.Provider>
			</div>
		</div>
	);
}

export default App;
