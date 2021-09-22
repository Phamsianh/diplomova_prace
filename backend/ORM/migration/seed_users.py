from ORM.Model import User, Role, Group, GroupRole, UserGroupRole
from ORM.session import session
import hashlib

phamsianh = User(
    first_name='Si Anh',
    last_name='Pham',
    user_name='phamsianh97',
    password='strongpassword',
    email='phamsianh97@gmail.com',
    phone='739875282',
)
alexandrstefek = User(
    first_name='Alexandr',
    last_name='Stefek',
    user_name='alexandrstefek',
    password='strongpassword',
    email='alexandr.stefek@unob.cz',
    phone='973442256'
)
zuzanakrocova = User(
    first_name='Zuzana',
    last_name='Kročová',
    user_name='zuzanakrocova',
    password='strongpassword',
    email='zuzana.krocova@unob.cz',
    phone='973442281'
)
vlastimilneumann = User(
    first_name='Vlastimil',
    last_name='Neumann',
    user_name='vlastimilneumann',
    password='strongpassword',
    email='vlastimil.neumann@unob.cz',
    phone='973442296'
)
janfarlik = User(
    first_name='Jan',
    last_name='Farlík',
    user_name='janfarlik',
    password='strongpassword',
    email='jan.farlik@unob.cz',
    phone='973442511'
)
petrfrantis = User(
    first_name='Petr',
    last_name='Františ',
    user_name='petrfrantis',
    password='strongpassword',
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
role_exchange_student = Role(name="Exchange Student", role="applicant")

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

admin_of_UoD = GroupRole(name="Admin of University of Defence", role=role_system_admin, group=group_UoD)
rector_of_UoD = GroupRole(name="Rector of University of Defence", role=role_rector, group=group_UoD)
dean_of_FMT = GroupRole(name="Dean of FMT (GrAdmin)", role=role_dean, group=group_FMT)
dean_of_FMl = GroupRole(name="Dean of FMl (GrAdmin)", role=role_dean, group=group_FML)
dean_of_FMHS = GroupRole(name="Dean of FMHS (GrAdmin)", role=role_dean, group=group_FMHS)
vice_dean_of_FMT = GroupRole(name="Vice Dean of FMT", role=role_vice_dean, group=group_FMT)
head_of_DoICO = GroupRole(name="Head of Department of Informatics and Cyber Operations", role=role_head_of_department,
                          group=group_DoICO)
head_of_DoWA = GroupRole(name="Head of Department of Weapons and Ammunition", role=role_head_of_department,
                         group=group_DoWA)
leading_teacher = GroupRole(name="Leading Teacher", role=role_leading_teacher)
consultant = GroupRole(name="Consultant", role=role_consultant)
student_of_CIT = GroupRole(name="Student of 2-CIT-C", role=role_student, group=group_2_CIT_C)
student_of_WA = GroupRole(name="Student of 2-WA-C", role=role_student, group=group_2_WA_C)
exchange_student_of_CIT = GroupRole(name="Exchange Student of 2-CIT-C", role=role_student, group=group_2_CIT_C)

# group_UoD.groups_roles = [admin_of_UoD, rector_of_UoD]
# group_FMT.groups_roles = [dean_of_FMT, vice_dean_of_FMT]
# group_FML.groups_roles = [dean_of_FMl]
# group_FMHS.groups_roles = [dean_of_FMHS]
# group_DoICO.groups_roles = [head_of_DoICO]
# group_DoWA.groups_roles = [head_of_DoWA]
# group_2_CIT_C.groups_roles = [student_of_CIT, exchange_student_of_CIT]
# group_2_WA_C.groups_roles = [student_of_WA]
#
# role_system_admin.groups_roles = [admin_of_UoD]
# role_rector.groups_roles = [rector_of_UoD]
# role_dean.groups_roles = [dean_of_FMT, dean_of_FMl, dean_of_FMHS]
# role_vice_dean.groups_roles = [vice_dean_of_FMT]
# role_head_of_department.groups_roles = [head_of_DoICO, head_of_DoWA]
# role_leading_teacher.groups_roles = [leading_teacher]
# role_consultant.groups_roles = [consultant]
# role_student.groups_roles = [student_of_CIT, student_of_WA]
# role_exchange_student.groups_roles = [exchange_student_of_CIT]

phamsianh.created_groups = [
    group_UoD,
    group_FMT,
    group_FML,
    group_FMHS,
    group_DoICO,
    group_DoWA,
    group_2_CIT_C,
    group_2_WA_C
]
phamsianh.created_roles = [
    role_system_admin,
    role_rector,
    role_dean,
    role_vice_dean,
    role_head_of_department,
    role_leading_teacher,
    role_consultant,
    role_student,
    role_exchange_student
]
phamsianh.created_groups_roles = [
    admin_of_UoD,
    rector_of_UoD,
    dean_of_FMl,
    dean_of_FMT,
    dean_of_FMHS,
    vice_dean_of_FMT,
    head_of_DoICO,
    head_of_DoWA,
    leading_teacher,
    consultant,
    student_of_CIT,
    exchange_student_of_CIT,
    student_of_WA
]

phamsianh_student_CIT = UserGroupRole(user=phamsianh, group_role=student_of_CIT)
# phamsianh_student_CIT.user = phamsianh
# phamsianh_student_CIT.group_role = student_of_CIT

phamsianh_exchange_student_CIT = UserGroupRole(user=phamsianh, group_role=exchange_student_of_CIT)
# phamsianh_exchange_student_CIT.user = phamsianh
# phamsianh_exchange_student_CIT.group_role = exchange_student_of_CIT

phamsianh_admin_UoD = UserGroupRole(user=phamsianh, group_role=admin_of_UoD)
# phamsianh_admin_UoD.user = phamsianh
# phamsianh_admin_UoD.group_role = admin_of_UoD

zuzanakrocova_rector_admin_UoD = UserGroupRole(user=zuzanakrocova, group_role=rector_of_UoD)
# zuzanakrocova_rector_admin_UoD.user = zuzanakrocova
# zuzanakrocova_rector_admin_UoD.group_role = rector_of_UoD

vlastimilneumann_dean_gr_admin_FMT = UserGroupRole(user=vlastimilneumann, group_role=dean_of_FMT)
# vlastimilneumann_dean_gr_admin_FMT.user = vlastimilneumann
# vlastimilneumann_dean_gr_admin_FMT.group_role = dean_of_FMT

janfarlik_vice_dean_FMT = UserGroupRole(user=janfarlik, group_role=vice_dean_of_FMT)
# janfarlik_vice_dean_FMT.user = janfarlik
# janfarlik_vice_dean_FMT.group_role = vice_dean_of_FMT

petrfrantis_head_of_DoICO = UserGroupRole(user=petrfrantis, group_role=head_of_DoICO)
# petrfrantis_head_of_DoICO.user = petrfrantis
# petrfrantis_head_of_DoICO.group_role = head_of_DoICO

alexandrstefek_leading_teacher = UserGroupRole(user=alexandrstefek, group_role=leading_teacher)
# alexandrstefek_leading_teacher.user = alexandrstefek
# alexandrstefek_leading_teacher.group_role = leading_teacher

alexandrstefek_consultant = UserGroupRole(user=alexandrstefek, group_role=consultant)
# alexandrstefek_consultant.user = alexandrstefek
# alexandrstefek_consultant.group_role = consultant

petrfrantis_consultant = UserGroupRole(user=petrfrantis, group_role=consultant)
# petrfrantis_consultant.user = petrfrantis
# petrfrantis_consultant.group_role = consultant

phamsianh.created_users_groups_roles = [
    phamsianh_student_CIT,
    phamsianh_admin_UoD,
    zuzanakrocova_rector_admin_UoD,
    vlastimilneumann_dean_gr_admin_FMT,
    janfarlik_vice_dean_FMT,
    petrfrantis_head_of_DoICO,
    alexandrstefek_leading_teacher,
    alexandrstefek_consultant,
    petrfrantis_consultant
]

session.add_all([phamsianh, alexandrstefek, zuzanakrocova, vlastimilneumann, petrfrantis])
session.commit()
session.close()

