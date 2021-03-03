from controllers.HomeController import Home
from controllers.auth.LoginController import Login
from controllers.auth.RegisterController import Register
from controllers.auth.ResetPasswordController import ResetPassword
from controllers.admin.manage_form_structure.GetAllFormStructures import GetAllFormStructures
from controllers.admin.manage_form_structure.CreateFormStructure import CreateFormStructure
from controllers.admin.manage_user.GetAllUsers import GetAllUsers
from controllers.admin.manage_role.GetAllRoles import GetAllRoles

route = [
    # For all users
    (r'/', Home),
    (r'/login', Login),
    (r'/register', Register),
    (r'/resetpassword', ResetPassword),

    # For admins
    (r'/formstructures', GetAllFormStructures),
    (r'/formstructures/create', CreateFormStructure),
    (r'/users', GetAllUsers),
    (r'/roles', GetAllRoles)
]
