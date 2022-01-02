import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Navbar from './components/navbar/navbar';
import { Hnavbar } from './components/hnavbar/hnavbar';
import HomePage from './pages/home_page/home_page';

import FormPage from './pages/form_page/form_page';
import FormIndex from './pages/form_page';
import CreateFormPage from './pages/form_page/create_form_page';
import ReadFormPage from './pages/form_page/read_form_page';
import UpdateFormPage from './pages/form_page/update_form_page';

import InstancePage from './pages/instance_page/instance_page';
import InstanceIndex from './pages/instance_page/index';
import { CreateInstancePage } from './pages/instance_page/create_instance_page';
import { ReadInstancePage } from './pages/instance_page/read_instance_page';
import { UpdateInstancePage } from './pages/instance_page/update_instance_page';
import { ReadCommitsPage } from './pages/instance_page/commit_page/read_commits_page';

import { LoginPage } from './pages/login_page/login_page';
import { LoginIndex } from './pages/login_page';

import { createContext, useEffect, useState } from 'react';
import { useController } from './controllers';

import { NotFoundPage } from './pages/not_found_page/not_found_page';

import './main.css';
import { ReadCommitPage } from './pages/instance_page/commit_page/read_commit_page';
import { Test } from './pages/test/test';

export const UserContext = createContext();

function App() {
	const { UserCtlr } = useController();
	const location = useLocation();
	const navigate = useNavigate();

	const [login, setLogin] = useState(false);
	const [user_data, setUserData] = useState();
	const [held_positions, setHeldPositions] = useState();

	
	useEffect(() => {
		UserCtlr.get_rsc_ins('me').then((data) => {
			setUserData(data);
		});
		UserCtlr.get_rel_rsc('me', 'held_positions').then((data) =>
			setHeldPositions(data)
		);
	}, []);

	useEffect(() => {
		if (location.pathname === '/login') setLogin(true);
		else setLogin(false);
		if (location.state === 'new_login'){
			console.log('new login');
			UserCtlr.get_rsc_ins('me').then((data) => {
				setUserData(data);
			});
			UserCtlr.get_rel_rsc('me', 'held_positions').then((data) =>
				setHeldPositions(data)
			);
		}
	}, [location]);
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
							<Route path="/forms" element={<FormPage />}>
								<Route path="" element={<FormIndex />} />
								<Route path="create" element={<CreateFormPage />} />
								<Route path=":id" element={<ReadFormPage />} />
								<Route
									path=":id/update"
									element={<UpdateFormPage />}
								/>
							</Route>

							<Route path="/instances" element={<InstancePage />}>
								<Route path="" element={<InstanceIndex />} />
								<Route
									path="create"
									element={<CreateInstancePage />}
								/>
								<Route path=":id" element={<ReadInstancePage />} />
								<Route path=":id/commits" element={<ReadCommitsPage/>} />
								<Route path=":id/commits/:hash_commit" element={<ReadCommitPage/>}/>
								<Route path=":id/update" element={<UpdateInstancePage />} />
							</Route>

							<Route path='/test' element={<Test/>} />
							<Route path="*" element={<NotFoundPage/>} />
						</Routes>
					</div>
				</UserContext.Provider>
			</div>
		</div>
	);
}

export default App;
