from ORM.Model import User, Role, Group, Position, UserPosition
from ORM.session import session

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
zdenekvintr = User(
    first_name='Zdeněk',
    last_name='Vintr',
    user_name='zdenekvintr',
    password='strongpassword',
    email='zdenek.vintr@unob.cz',
    phone='973443474'
)

role_system_admin = Role(name="System Admin", role="admin")
role_rector = Role(name="Rector", role="admin")
role_dean = Role(name="Dean", role="group_admin")
role_vice_dean = Role(name="Vice Dean", role="handler")
role_guarantor = Role(name="Guarantor", role="handler")
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

admin_of_UoD = Position(name="Admin of University of Defence", role=role_system_admin, group=group_UoD)
rector_of_UoD = Position(name="Rector of University of Defence", role=role_rector, group=group_UoD)
dean = Position(name="Dean", role=role_dean)
dean_of_FMT = Position(name="Dean of FMT (GrAdmin)", role=role_dean, group=group_FMT)
dean_of_FMl = Position(name="Dean of FML (GrAdmin)", role=role_dean, group=group_FML)
dean_of_FMHS = Position(name="Dean of FMHS (GrAdmin)", role=role_dean, group=group_FMHS)
vice_dean = Position(name="Vice Dean", role=role_vice_dean)
vice_dean_of_FMT = Position(name="Vice Dean of FMT", role=role_vice_dean, group=group_FMT)
guarantor = Position(name="Guarantor", role=role_guarantor)
head_of_department = Position(name="Head of Department", role=role_head_of_department)
head_of_DoICO = Position(name="Head of Department of Informatics and Cyber Operations", role=role_head_of_department,
                         group=group_DoICO)
head_of_DoWA = Position(name="Head of Department of Weapons and Ammunition", role=role_head_of_department,
                        group=group_DoWA)
leading_teacher = Position(name="Leading Teacher", role=role_leading_teacher)
consultant = Position(name="Consultant", role=role_consultant)
student = Position(name="Student", role=role_student)
student_of_CIT = Position(name="Student of 2-CIT-C", role=role_student, group=group_2_CIT_C)
student_of_WA = Position(name="Student of 2-WA-C", role=role_student, group=group_2_WA_C)
exchange_student_of_CIT = Position(name="Exchange Student of 2-CIT-C", role=role_student, group=group_2_CIT_C)


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
    role_guarantor,
    role_head_of_department,
    role_leading_teacher,
    role_consultant,
    role_student,
    role_exchange_student
]
phamsianh.created_positions = [
    admin_of_UoD,
    rector_of_UoD,
    dean,
    dean_of_FMl,
    dean_of_FMT,
    dean_of_FMHS,
    vice_dean,
    vice_dean_of_FMT,
    guarantor,
    head_of_department,
    head_of_DoICO,
    head_of_DoWA,
    leading_teacher,
    consultant,
    student,
    student_of_CIT,
    exchange_student_of_CIT,
    student_of_WA
]

phamsianh_student = UserPosition(user=phamsianh, position=student)

phamsianh_student_CIT = UserPosition(user=phamsianh, position=student_of_CIT)

phamsianh_exchange_student_CIT = UserPosition(user=phamsianh, position=exchange_student_of_CIT)

phamsianh_admin_UoD = UserPosition(user=phamsianh, position=admin_of_UoD)

zuzanakrocova_rector_admin_UoD = UserPosition(user=zuzanakrocova, position=rector_of_UoD)

vlastimilneumann_dean = UserPosition(user=vlastimilneumann, position=dean)

vlastimilneumann_dean_gr_admin_FMT = UserPosition(user=vlastimilneumann, position=dean_of_FMT)

janfarlik_vice_dean = UserPosition(user=janfarlik, position=vice_dean)

janfarlik_vice_dean_FMT = UserPosition(user=janfarlik, position=vice_dean_of_FMT)

zdenekvintr_guarantor = UserPosition(user=zdenekvintr, position=guarantor)

petrfrantis_head_of_department = UserPosition(user=petrfrantis, position=head_of_department)

petrfrantis_head_of_DoICO = UserPosition(user=petrfrantis, position=head_of_DoICO)

alexandrstefek_leading_teacher = UserPosition(user=alexandrstefek, position=leading_teacher)

alexandrstefek_consultant = UserPosition(user=alexandrstefek, position=consultant)

petrfrantis_leading_teacher = UserPosition(user=petrfrantis, position=leading_teacher)

petrfrantis_consultant = UserPosition(user=petrfrantis, position=consultant)

phamsianh.created_users_positions = [
    phamsianh_student,
    phamsianh_student_CIT,
    phamsianh_admin_UoD,
    phamsianh_exchange_student_CIT,
    zuzanakrocova_rector_admin_UoD,
    vlastimilneumann_dean,
    vlastimilneumann_dean_gr_admin_FMT,
    janfarlik_vice_dean,
    janfarlik_vice_dean_FMT,
    zdenekvintr_guarantor,
    petrfrantis_head_of_department,
    petrfrantis_head_of_DoICO,
    alexandrstefek_leading_teacher,
    alexandrstefek_consultant,
    petrfrantis_leading_teacher,
    petrfrantis_consultant
]

session.add_all([phamsianh, alexandrstefek, zuzanakrocova, vlastimilneumann, petrfrantis, zdenekvintr])
session.commit()
session.close()

