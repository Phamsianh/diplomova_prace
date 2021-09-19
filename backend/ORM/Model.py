from ORM.Base import Base
from ORM.session import session
from sqlalchemy import Column, ForeignKey, BigInteger, String, DateTime, Date, Integer, Enum, func
from sqlalchemy.orm import relationship, backref
from typing import Optional


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_name = Column(String(50), unique=True)
    password = Column(String)
    email = Column(String(50), unique=True)
    phone = Column(String(20))
    public_key = Column(String)
    birthdate = Column(Date)

    # one-to-many relationship(s)
    forms = relationship("Form", back_populates="creator")
    groups = relationship("Group", back_populates="creator")
    roles = relationship("Role", back_populates="creator")
    users_groups_roles = relationship("UserGroupRole", back_populates="user")
    form_instances = relationship("FormInstance", back_populates="creator")
    users_form_instances = relationship("UserFormInstance", back_populates="user")
    groups_roles = relationship("GroupRole", back_populates="creator")

    def __repr__(self):
        return f'''
User(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
first_name: {self.first_name}
last_name: {self.last_name}
user_name: {self.user_name}
password: {self.password}
email: {self.email}
phone: {self.phone}
public_key: {self.public_key}
birthdate: {self.birthdate}
)
'''

    def ga_gs_rs(self) -> Optional[list['GroupRole']]:
        """get all groups roles of a user"""

        return session.query(GroupRole)\
            .join(GroupRole.users_groups_roles)\
            .join(UserGroupRole.user)\
            .filter(User.id == self.id)\
            .all()

    def is_admin(self) -> bool:
        for g_r in self.ga_gs_rs():
            if g_r.role.role == 'admin':
                return True
        return False

    def is_gr_admin(self) -> bool:
        for g_r in self.ga_gs_rs():
            if g_r.role.role == 'group_admin':
                return True
        return False

    def is_handler(self) -> bool:
        for g_r in self.ga_gs_rs():
            if g_r.role.role == 'handler':
                return True
        return False

    def is_applicant(self) -> bool:
        for g_r in self.ga_gs_rs():
            if g_r.role.role == 'applicant':
                return True
        return False

    def ga_cr_gs(self) -> Optional[list['Group']]:
        """get all groups created by user with role admin"""
        return session.query(Group).filter(Group.admin_id == self.id).all()

    def ga_jd_gs(self) -> Optional[list['Group']]:
        """get all joined groups of a user"""
        return session.query(Group) \
            .join(Group.groups_roles) \
            .join(GroupRole.users_groups_roles) \
            .filter(UserGroupRole.user_id == self.id) \
            .all()

    def ga_cr_rs(self) -> Optional[list['Role']]:
        """get all created roles of a user with role admin"""
        return session.query(Role).join(Role.creator).filter(Role.creator_id == self.id).all()

    def ga_held_roles(self) -> Optional[list['Role']]:
        """get all roles held by a user"""
        return session.query(Role) \
            .join(Role.groups_roles) \
            .join(GroupRole.users_groups_roles) \
            .filter(UserGroupRole.user_id == self.id) \
            .all()

    def ga_cr_forms(self) -> Optional[list['Form']]:
        """get all created form of this user with role admin or group admin"""
        return session.query(Form).join(Form.creator).filter(Form.creator_id == self.id).all()

    def ga_cr_form_instances(self) -> Optional[list['FormInstance']]:
        """get all form instances created by this user"""
        return session.query(FormInstance)\
            .join(FormInstance.creator)\
            .filter(FormInstance.creator_id == self.id).all()

    def ga_av_sections(self, fi: 'FormInstance') -> Optional[list['Section']]:
        """get all available sections of a form instance for this user"""
        pass

    def ga_av_phases(self, fi: 'FormInstance') -> Optional[list['Phase']]:
        """get all available phases of a form instance for this user"""
        pass

    def ga_av_fields(self, fi: 'FormInstance') -> Optional[list['Field']]:
        pass

    # def create_role(self, 'Role'):


class Form(Base):
    __tablename__ = "forms"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'))

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="forms")

    # one-to-many relationship(s)
    phases = relationship("Phase", back_populates="form")
    # sections = relationship("Section", back_populates="form") #For later consideration
    form_instances = relationship("FormInstance", back_populates="form")

    def __repr__(self):
        return f'''
FormStructure(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
creator_id: {self.creator_id}
)
'''


class Section(Base):
    __tablename__ = "sections"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    # form_id = Column(BigInteger, ForeignKey("forms.id")) #For later consideration
    # phase_group_role_id = Column(BigInteger, ForeignKey("phases_groups_roles.id"))
    phase_id = Column(BigInteger, ForeignKey("phases.id"))
    group_role_id = Column(BigInteger, ForeignKey("groups_roles.id"))
    order = Column(Integer)

    # many-to-one relationship(s)
    # form = relationship("Form", back_populates="sections")  #For later consideration
    # phase_group_role = relationship("PhaseGroupRole", back_populates="sections")
    phase = relationship("Phase", back_populates="sections")
    group_role = relationship("GroupRole", back_populates="sections")

    # one-to-many relationship(s)
    fields = relationship("Field", back_populates="section")

    def __repr__(self):
        return f'''
Section(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
phase_id: {self.phase_id}
group_role_id: {self.group_role_id}
order: {self.order}
)
'''


class Field(Base):
    __tablename__ = "fields"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    section_id = Column(BigInteger, ForeignKey("sections.id"))
    order = Column(Integer)

    # many-to-one relationship(s)
    section = relationship("Section", back_populates="fields")

    # one-to-many relationship(s)
    form_instances_fields = relationship("FormInstanceField", back_populates="field")

    def __repr__(self):
        return f'''
Field(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
section_id: {self.section_id}
order: {self.order}
)
'''


class FormInstance(Base):
    __tablename__ = "form_instances"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    current_phase_id = Column(BigInteger, ForeignKey("phases.id"))
    creator_id = Column(BigInteger, ForeignKey("users.id"))
    current_state = Column(Enum(
        "initialized",
        "pending",
        "partial received",
        "full received",
        "partial received & partial resolved",
        "full received & partial resolved",
        "full resolved",
        "done",
        name="form_state_enum"
    ), server_default="initialized")

    # many-to-one relationship(s)
    form = relationship("Form", back_populates="form_instances")
    current_phase = relationship("Phase", back_populates="form_instances")
    creator = relationship("User", back_populates="form_instances")

    # one-to-many relationship(s)
    form_instances_fields = relationship("FormInstanceField", back_populates="form_instance")
    users_form_instances = relationship("UserFormInstance", back_populates="form_instance")

    # histories = relationship("History", back_populates="form_instance")

    def __repr__(self):
        return f'''
FormInstance(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_id: {self.form_id}
current_phase_id: {self.current_phase_id}
creator_id: {self.creator_id}
current_state: {self.current_state}
)
'''


class UserFormInstance(Base):
    __tablename__ = "users_form_instances"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(BigInteger, ForeignKey("users.id"))
    form_instance_id = Column(BigInteger, ForeignKey("form_instances.id"))

    # many-to-one relationship(s)
    user = relationship("User", back_populates="users_form_instances")
    form_instance = relationship("FormInstance", back_populates="users_form_instances")
    # one-to-many relationship(s)
    form_instances_fields = relationship("FormInstanceField", back_populates="participant")

    def __repr__(self):
        return f'''
UserFormInstance(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
user_id: {self.user_id}
form_instance_id: {self.form_instance_id}
)
'''


class FormInstanceField(Base):
    __tablename__ = "form_instances_fields"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_instance_id = Column(BigInteger, ForeignKey("form_instances.id"))
    field_id = Column(BigInteger, ForeignKey("fields.id"))
    value = Column(String)
    participant_id = Column(BigInteger, ForeignKey("users_form_instances.id"))

    # many-to-one relationship(s)
    form_instance = relationship("FormInstance", back_populates="form_instances_fields")
    field = relationship("Field", back_populates="form_instances_fields")
    participant = relationship("UserFormInstance", back_populates="form_instances_fields")

    # one-to-many relationship(s)
    # form_instances_fields = relationship("FormInstanceField", back_populates="form_instance")
    # histories = relationship("History", back_populates="form_instance")

    def __repr__(self):
        return f'''
FormInstanceField(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_instance_id: {self.form_instance_id}
field_id: {self.field_id}
value: {self.value}
editor_id: {self.editor_id}
)
'''


class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(100))
    address = Column(String(100))
    phone = Column(Integer)
    admin_id = Column(BigInteger, ForeignKey("users.id"))
    superior_group_id = Column(BigInteger, ForeignKey("groups.id"))

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="groups")
    # one-to-many relationship(s)
    groups_roles = relationship("GroupRole", back_populates="group")
    subordinate_groups = relationship("Group", backref=backref("superior_group", remote_side=[id]))

    def __repr__(self):
        return f'''
Group(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
address: {self.name}
phone: {self.phone}
admin_id: {self.admin_id},
superior_group_id: {self.superior_group_id}
)
'''


class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), unique=True)
    role = Column(Enum("admin", "group_admin", "handler", "applicant", name="role_enum"))
    creator_id = Column(BigInteger, ForeignKey("users.id"))

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="roles")

    # one-to-many relationship(s)
    groups_roles = relationship("GroupRole", back_populates="role")

    def __repr__(self):
        return f'''
Role(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
role: {self.role}
creator_id: {self.creator_id}
)
'''


class Phase(Base):
    __tablename__ = "phases"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    name = Column(String(100))
    # order = Column(Integer) #For later consideration
    description = Column(String)
    group_role_id = Column(BigInteger, ForeignKey("groups_roles.id"))
    phase_type = Column(Enum("begin", "transit", "end", name="phase_enum"))

    # many-to-one relationship(s)
    form = relationship("Form", back_populates="phases")
    group_role = relationship("GroupRole", back_populates="phases")

    # one-to-many relationship(s)
    # phases_groups_roles = relationship("PhaseGroupRole", back_populates="phase")
    form_instances = relationship("FormInstance", back_populates="current_phase")
    sections = relationship("Section", back_populates="phase")
    # from_transitions = relationship("Transition", back_populates="from_phase", foreign_keys=["transitions.from_phase_id"])
    # to_transitions = relationship("Transition", back_populates="to_phase", foreign_keys=[])

    def __repr__(self):
        return f'''
Phase(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_id: {self.form_id}
description: {self.description}
group_role_id: {self.group_role_id}
phase_type: {self.phase_type}
)
'''


class Transition(Base):
    __tablename__ = "transitions"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50))
    from_phase_id = Column(BigInteger, ForeignKey("phases.id"))
    to_phase_id = Column(BigInteger, ForeignKey("phases.id"))
    order = Column(Integer)

    # many-to-one relationship(s)
    from_phase = relationship("Phase", backref="from_transitions", foreign_keys=[from_phase_id])
    to_phase = relationship("Phase", backref="to_transitions", foreign_keys=[to_phase_id])

    def __repr__(self):
        return f'''
Transition(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
from_phase_id: {self.from_phase_id}
to_phase_id: {self.to_phase_id}
order: {self.order}
name: {self.name}
)
'''


class GroupRole(Base):
    __tablename__ = 'groups_roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(100))
    group_id = Column(BigInteger, ForeignKey("groups.id"))
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    # many-to-one relationship(s)
    group = relationship("Group", back_populates="groups_roles")
    role = relationship("Role", back_populates="groups_roles")
    creator = relationship("User", back_populates="groups_roles")

    # one-to-many relationship(s)
    phases = relationship("Phase", back_populates="group_role")
    users_groups_roles = relationship("UserGroupRole", back_populates="group_role")
    # phases_groups_roles = relationship("PhaseGroupRole", back_populates="group_role")
    sections = relationship("Section", back_populates="group_role")

    def __repr__(self):
        return f'''
GroupRole(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
group_id: {self.group_id}
role_id: {self.role_id}
creator_id: {self.creator_id}
)
'''


class UserGroupRole(Base):
    __tablename__ = 'users_groups_roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(BigInteger, ForeignKey("users.id"))
    group_role_id = Column(BigInteger, ForeignKey("groups_roles.id"))

    # many-to-one relationship(s)
    user = relationship("User", back_populates="users_groups_roles")
    group_role = relationship("GroupRole", back_populates="users_groups_roles")

    def __repr__(self):
        return f'''
UserGroupRole(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
user_id: {self.user_id}
group_role_id: {self.group_role_id}
)
'''


# class PhaseGroupRole(Base):
#     __tablename__ = "phases_groups_roles"
#
#     id = Column(BigInteger, primary_key=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     phase_id = Column(BigInteger, ForeignKey("phases.id"))
#     group_role_id = Column(BigInteger, ForeignKey("groups_roles.id"))
#
#     # many-to-one relationship(s)
#     phase = relationship("Phase", back_populates="phases_groups_roles")
#     group_role = relationship("GroupRole", back_populates="phases_groups_roles")
#
#     # one-to-many relationship(s)
#     sections = relationship("Section", back_populates="phase_group_role")
#
#     def __repr__(self):
#         return f'''
# PhaseGroupRole(
# id: {self.id}
# created_at: {self.created_at}
# updated_at: {self.updated_at}
# phase_id: {self.phase_id}
# group_role_id: {self.group_role_id}
# )
# '''
