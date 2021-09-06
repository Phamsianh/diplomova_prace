from ORM.Model import User, Role, Group, GroupRole, UserGroupRole
from ORM.session import session
import hashlib

phamsianh = User(
    first_name='Si Anh',
    last_name='Pham',
    user_name='phamsianh97',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='phamsianh97@gmail.com',
    phone='739875282',
)
alexandrstefek = User(
    first_name='Alexandr',
    last_name='Stefek',
    user_name='alexandrstefek',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='alexandr.stefek@unob.cz',
    phone='973442256'
)
zuzanakrocova = User(
    first_name='Zuzana',
    last_name='Kročová',
    user_name='zuzanakrocova',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='zuzana.krocova@unob.cz',
    phone='973442281'
)
vlastimilneumann = User(
    first_name='Vlastimil',
    last_name='Neumann',
    user_name='vlastimilneumann',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='vlastimil.neumann@unob.cz',
    phone='973442296'
)
janfarlik = User(
    first_name='Jan',
    last_name='Farlík',
    user_name='janfarlik',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='jan.farlik@unob.cz',
    phone='973442511'
)
petrfrantis = User(
    first_name='Petr',
    last_name='Františ',
    user_name='petrfrantis',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='petr.frantis@unob.cz',
    phone='973442348'
)

role_system_admin = Role(name="System Admin", role="admin")
role_rector = Role(name="Rector", role="admin")
role_dean = Role(name="Dean", role="group_admin")
role_vice_dean = Role(name="Vice Dean", role="handler")
role_head_of_department = Role(name="Head of Department", role="handler")
role_leading_teacher = Role(name="Leading Teacher", role="handler")
role_consultant = Role(name="Consultant", role="handler")
role_student = Role(name="Student", role="applicant")

group_UoD = Group(name="Universty of Defence")
group_FMT = Group(name="Faculty of Military Technology")
group_FML = Group(name="Faculty of Military Leadership")
group_FMHS = Group(name="Faculty of Military Health Sciences")
group_UoD.subordinate_groups = [group_FML, group_FMT, group_FMHS]
group_DoICO = Group(name="Department of Informatics and Cyber Operations")
group_DoWA = Group(name="Department of Weapons and Ammunition")
group_FMT.subordinate_groups = [group_DoICO, group_DoWA]
group_2_CIT_C = Group(name="2-CIT-C")
group_2_CIT_C.superior_group = group_DoICO
group_2_WA_C = Group(name="2-WA-C")
group_2_WA_C.superior_group = group_DoWA

admin_of_UoD = GroupRole(name="Admin of University of Defence")
rector_of_UoD = GroupRole(name="Rector of University of Defence")
dean_of_FMT = GroupRole(name="Dean of FMT (GrAdmin)")
dean_of_FMl = GroupRole(name="Dean of FMl (GrAdmin)")
dean_of_FMHS = GroupRole(name="Dean of FMHS (GrAdmin)")
vice_dean_of_FMT = GroupRole(name="Vice Dean of FMT")
head_of_DoICO = GroupRole(name="Head of Department of Informatics and Cyber Operations")
head_of_DoWA = GroupRole(name="Head of Department of Weapons and Ammunition")
leading_teacher = GroupRole(name="Leading Teacher")
consultant = GroupRole(name="Consultant")
student_of_CIT = GroupRole(name="Student of 2-CIT-C")
student_of_WA = GroupRole(name="Student of 2-WA-C")

group_UoD.groups_roles = [admin_of_UoD, rector_of_UoD]
group_FMT.groups_roles = [dean_of_FMT, vice_dean_of_FMT]
group_FML.groups_roles = [dean_of_FMl]
group_FMHS.groups_roles = [dean_of_FMHS]
group_DoICO.groups_roles = [head_of_DoICO]
group_DoWA.groups_roles = [head_of_DoWA]
group_2_CIT_C.groups_roles = [student_of_CIT]
group_2_WA_C.groups_roles = [student_of_WA]

role_system_admin.groups_roles = [admin_of_UoD]
role_rector.groups_roles = [rector_of_UoD]
role_dean.groups_roles = [dean_of_FMT, dean_of_FMl, dean_of_FMHS]
role_vice_dean.groups_roles = [vice_dean_of_FMT]
role_head_of_department.groups_roles = [head_of_DoICO, head_of_DoWA]
role_leading_teacher.groups_roles = [leading_teacher]
role_consultant.groups_roles = [consultant]
role_student.groups_roles = [student_of_CIT, student_of_WA]

phamsianh.groups = [
    group_UoD,
    group_FMT,
    group_FML,
    group_FMHS,
    group_DoICO,
    group_DoWA,
    group_2_CIT_C,
    group_2_WA_C
]
phamsianh.roles = [
    role_system_admin,
    role_rector,
    role_dean,
    role_vice_dean,
    role_head_of_department,
    role_leading_teacher,
    role_consultant,
    role_student
]

phamsianh_student_CIT = UserGroupRole()
phamsianh_student_CIT.user = phamsianh
phamsianh_student_CIT.group_role = student_of_CIT

phamsianh_admin_UoD = UserGroupRole()
phamsianh_admin_UoD.user = phamsianh
phamsianh_admin_UoD.group_role = admin_of_UoD

zuzanakrocova_rector_admin_UoD = UserGroupRole()
zuzanakrocova_rector_admin_UoD.user = zuzanakrocova
zuzanakrocova_rector_admin_UoD.group_role = rector_of_UoD

vlastimilneumann_dean_gr_admin_FMT = UserGroupRole()
vlastimilneumann_dean_gr_admin_FMT.user = vlastimilneumann
vlastimilneumann_dean_gr_admin_FMT.group_role = dean_of_FMT

janfarlik_vice_dean_FMT = UserGroupRole()
janfarlik_vice_dean_FMT.user = janfarlik
janfarlik_vice_dean_FMT.group_role = vice_dean_of_FMT

petrfrantis_head_of_DoICO = UserGroupRole()
petrfrantis_head_of_DoICO.user = petrfrantis
petrfrantis_head_of_DoICO.group_role = head_of_DoICO

alexandrstefek_leading_teacher = UserGroupRole()
alexandrstefek_leading_teacher.user = alexandrstefek
alexandrstefek_leading_teacher.group_role = leading_teacher

petrfrantis_consultant = UserGroupRole()
petrfrantis_consultant.user = petrfrantis
petrfrantis_consultant.group_role = consultant

session.add_all([phamsianh, alexandrstefek, zuzanakrocova, vlastimilneumann, petrfrantis])
session.commit()
session.close()

