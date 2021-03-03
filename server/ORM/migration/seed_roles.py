from ORM.Model.Role import Role
from ORM.Model.Permission import Permission
from ORM.session import session

admin_role = Role(name='Administrator')
staff_role = Role(name='Staff')
client_role = Role(name='Client')

admin_permission = Permission(
    role_id=1,

    create_form_structure=True,
    read_form_structure=True,
    update_form_structure=True,
    delete_form_structure=True,

    create_user=True,
    read_user=True,
    update_user=True,
    delete_user=True,

    create_role=True,
    read_role=True,
    update_role=True,
    delete_role=True,
)

staff_permission = Permission(role_id=2)
client_permission = Permission(role_id=3)

session.add_all([admin_role, staff_role, client_role])
session.add_all([admin_permission, staff_permission, client_permission])
session.commit()