from ORM.Base import Base
from ORM.session import Session
from sqlalchemy import Column, ForeignKey, BigInteger, String, DateTime, Date, Integer, Enum, Boolean, func, inspect
from sqlalchemy.orm import relationship, backref
from typing import Optional, List
import hashlib


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_name = Column(String(50), unique=True)
    _password = Column('password', String)
    email = Column(String(50), unique=True)
    phone = Column(String(20))
    public_key = Column(String)
    birthdate = Column(Date)
    disabled = Column(Boolean, server_default="false")

    # one-to-many relationship(s)
    created_forms = relationship("Form", back_populates="creator")
    created_groups = relationship("Group", back_populates="creator")
    created_roles = relationship("Role", back_populates="creator")
    created_positions = relationship("Position", back_populates="creator")
    created_users_positions = relationship("UserPosition", back_populates="creator",
                                           foreign_keys="UserPosition.creator_id")
    users_positions = relationship("UserPosition", back_populates="user", foreign_keys="UserPosition.user_id")
    created_instances = relationship("Instance", back_populates="creator")
    instances_fields = relationship("InstanceField", back_populates="creator")

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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """
        :param value: For later implementation: This value must be validated
        """
        self._password = hashlib.sha256(value.encode()).hexdigest()

    @property
    def held_positions(self) -> Optional[List['Position']]:
        """get all groups roles of this user"""

        return inspect(self).session.query(Position) \
            .join(Position.users_positions) \
            .join(UserPosition.user) \
            .filter(User.id == self.id) \
            .all()

    @property
    def is_admin(self) -> bool:
        for r in self.held_roles:
            if r.role == 'admin':
                return True
        return False

    @property
    def is_gr_admin(self) -> bool:
        for r in self.held_roles:
            if r.role == 'group_admin':
                return True
        return False

    @property
    def is_admin_or_gr_admin(self) -> bool:
        """
        check if this user is admin or group admin in one query
        """
        for r in self.held_roles:
            if r.role == 'admin' or r.role == 'group_admin':
                return True
        return False

    @property
    def is_handler(self) -> bool:
        for r in self.held_roles:
            if r.role == 'handler':
                return True
        return False

    @property
    def is_applicant(self) -> bool:
        for r in self.held_roles:
            if r.role == 'applicant':
                return True
        return False

    # def ga_cr_gs(self, session: Session) -> Optional[List['Group']]:
    #     """get all groups created by user with role admin"""
    #     return session.query(Group).filter(Group.admin_id == self.id).all()

    @property
    def joined_groups(self) -> Optional[List['Group']]:
        """get all joined groups of this user"""
        return inspect(self).session.query(Group) \
            .join(Group.positions) \
            .join(Position.users_positions) \
            .filter(UserPosition.user_id == self.id) \
            .all()

    # def ga_cr_rs(self, session: Session) -> Optional[List['Role']]:
    #     """get all created roles of a user with role admin"""
    #     return session.query(Role).join(Role.creator).filter(Role.creator_id == self.id).all()

    @property
    def held_roles(self) -> Optional[List['Role']]:
        """get all roles held by this user"""
        return inspect(self).session.query(Role) \
            .join(Role.positions) \
            .join(Position.users_positions) \
            .filter(UserPosition.user_id == self.id) \
            .all()

    # def ga_cr_forms(self, session: Session) -> Optional[List['Form']]:
    #     """get all created form of this user with role admin or group admin"""
    #     return session.query(Form).join(Form.creator).filter(Form.creator_id == self.id).all()

    # def ga_cr_instances(self, session: Session) -> Optional[List['Instance']]:
    #     """get all form instances created by this user"""
    #     return session.query(Instance)\
    #         .join(Instance.creator)\
    #         .filter(Instance.creator_id == self.id).all()

    @property
    def participated_instances(self) -> Optional[List['Instance']]:
        """get all participated form instances of this user"""
        return inspect(self).session.query(Instance) \
            .join(Instance.instances_fields) \
            .join(InstanceField.creator) \
            .filter(InstanceField.creator_id == self.id) \
            .all()

    def ga_av_sections(self, fi: 'Instance', session: Session) -> Optional[List['Section']]:
        """get all available sections of a form instance for this user"""
        pass

    def ga_av_phases(self, fi: 'Instance', session: Session) -> Optional[List['Phase']]:
        """get all available phases of a form instance for this user"""
        pass

    def ga_av_fields(self, fi: 'Instance', session: Session) -> Optional[List['Field']]:
        pass

    # def create_role(self, 'Role'):


class Form(Base):
    __tablename__ = "forms"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="created_forms")

    # one-to-many relationship(s)
    phases = relationship("Phase", back_populates="form")
    sections = relationship("Section", back_populates="form")
    instances = relationship("Instance", back_populates="form")

    def __repr__(self):
        return f'''
Form(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
creator_id: {self.creator_id}
)
'''

    @property
    def fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field) \
            .join(Field.section) \
            .join(Section.phase) \
            .join(Phase.form) \
            .filter(Form.id == self.id).all()

    @property
    def begin_phase(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form) \
            .filter(Form.id == self.id). \
            filter(Phase.phase_type == 'begin').first()

    @property
    def end_phase(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form) \
            .filter(Form.id == self.id). \
            filter(Phase.phase_type == 'end').first()

    @property
    def begin_fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form).\
            filter(Form.id == self.id, Phase.phase_type == 'begin').all()

    @property
    def transitions(self) -> Optional[List['Transition']]:
        q1 = inspect(self).session.query(Transition).join(Transition.from_phase).join(Phase.form). \
            filter(Form.id == self.id)
        q2 = inspect(self).session.query(Transition).join(Transition.to_phase).join(Phase.form). \
            filter(Form.id == self.id)
        return q1.union(q2).all()

    @property
    def available_positions(self) -> Optional[List['Position']]:
        return inspect(self).session.query(Position).join(Position.sections).join(Section.phase).join(Phase.form). \
            filter(Form.id == self.id).all()


class Section(Base):
    __tablename__ = "sections"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    phase_id = Column(BigInteger, ForeignKey("phases.id"))
    position_id = Column(BigInteger, ForeignKey("positions.id"))
    order = Column(Integer)

    # many-to-one relationship(s)
    form = relationship("Form", back_populates="sections")
    phase = relationship("Phase", back_populates="sections")
    position = relationship("Position", back_populates="sections")

    # one-to-many relationship(s)
    fields = relationship("Field", back_populates="section")

    def __repr__(self):
        return f'''
Section(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
form_id: {self.form_id}
phase_id: {self.phase_id}
position_id: {self.position_id}
order: {self.order}
)
'''

    @property
    def creator(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.created_forms).join(Form.phases).join(Phase.sections). \
            filter(Section.id == self.id).first()


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
    instances_fields = relationship("InstanceField", back_populates="field")

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

    @property
    def creator(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.created_forms).join(Form.phases).join(Phase.sections) \
            .join(Section.fields).filter(Field.id == self.id).first()

    @property
    def phase(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.sections).join(Section.fields). \
            filter(Field.id == self.id)

    @property
    def form(self) -> Optional['Form']:
        return inspect(self).session.query(Form).join(Form.phases).join(Phase.sections).join(Section.fields). \
            filter(Field.id == self.id).first()

    @property
    def position(self) -> Optional['Position']:
        return inspect(self).session.query(Position).join(Position.sections).join(Section.fields). \
            filter(Field.id == self.id).first()


class Instance(Base):
    __tablename__ = "instances"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    current_phase_id = Column(BigInteger, ForeignKey("phases.id"))
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
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
    form = relationship("Form", back_populates="instances")
    current_phase = relationship("Phase", back_populates="instances")
    creator = relationship("User", back_populates="created_instances")

    # one-to-many relationship(s)
    instances_fields = relationship("InstanceField", back_populates="instance")

    def __repr__(self):
        return f'''
Instance(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_id: {self.form_id}
current_phase_id: {self.current_phase_id}
creator_id: {self.creator_id}
current_state: {self.current_state}
)
'''

    @property
    def phases(self) -> Optional[List['Phase']]:
        return inspect(self).session.query(Phase).join(Phase.form).join(Form.instances). \
            filter(Instance.id == self.id).all()

    @property
    def begin_phase(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form).join(Form.instances).\
            filter(Instance.id == self.id, Phase.phase_type == 'begin').first()

    @property
    def end_phase(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form).join(Form.instances).\
            filter(Instance.id == self.id, Phase.phase_type == 'end').first()

    @property
    def current_appointed_positions(self) -> Optional[List['Position']]:
        return inspect(self).session.query(Position). \
            join(Position.sections).join(Section.phase).join(Phase.instances). \
            filter(Instance.id == self.id).all()

    @property
    def current_remaining_positions(self) -> Optional[List['Position']]:
        handled_positions = inspect(self).session.query(Instance).join(Instance.instances_fields). \
            join(InstanceField.field).join(Field.section).filter(Section.position_id == Position.id)
        return inspect(self).session.query(Position).join(Position.sections).join(Section.phase). \
            join(Phase.instances).filter(Instance.id == self.id).filter(~handled_positions.exists()).all()

    @property
    def current_designated_position(self) -> Optional['Position']:
        return inspect(self).session.query(Position).join(Position.phases).join(Phase.instances). \
            filter(Instance.id == self.id).first()

    @property
    def sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.form).join(Form.instances). \
            filter(Instance.id == self.id).all()

    @property
    def resolved_sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields). \
            filter(InstanceField.instance_id == self.id).all()

    @property
    def unfilled_sections(self) -> Optional[List['Section']]:
        filled_sections = inspect(self).session.query(Instance).join(Instance.instances_fields). \
            join(InstanceField.field).filter(Field.section_id == Section.id)
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.form). \
            filter(Form.id == self.form_id).filter(~filled_sections.exists()).all()

    @property
    def fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form) \
            .join(Form.instances).filter(Instance.id == self.id).all()

    @property
    def begin_fields(self) -> Optional['Field']:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form).\
            join(Form.instances).filter(Instance.id == self.id, Phase.phase_type == 'begin').all()

    @property
    def filled_fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.instances_fields). \
            filter(InstanceField.instance_id == self.id).all()

    @property
    def unfilled_fields(self) -> Optional[List['Field']]:
        filled_fields = inspect(self).session.query(Instance).join(Instance.instances_fields). \
            filter(InstanceField.field_id == Field.id)

        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form). \
            filter(Form.id == self.form_id).filter(~filled_fields.exists()).all()

    @property
    def avai_next_phases(self) -> Optional[List['Phase']]:
        if self.current_state in ['initialized', 'full resolved']:
            return inspect(self).session.query(Phase).join(Phase.to_transitions). \
                filter(Transition.from_phase_id == self.current_phase_id).all()
        else:
            return None

    @property
    def avai_next_sections(self) -> Optional[List['Phase']]:
        return

    @property
    def curr_resp_users(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.instances_fields).join(InstanceField.field). \
            join(Field.section).join(Section.phase).join(Phase.instances).filter(Instance.id == self.id).all()

    def resp_usr_section(self, section_id: int) -> Optional['User']:
        return inspect(self).session.query(User).join(User.instances_fields).join(InstanceField.field). \
            filter(InstanceField.instance_id == self.id, Field.section_id == section_id).first()


class InstanceField(Base):
    __tablename__ = "instances_fields"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    instance_id = Column(BigInteger, ForeignKey("instances.id"))
    field_id = Column(BigInteger, ForeignKey("fields.id"))
    creator_id = Column(BigInteger, ForeignKey("users.id"))
    value = Column(String)
    resolved = Column(Boolean, server_default='false')

    # many-to-one relationship(s)
    instance = relationship("Instance", back_populates="instances_fields")
    field = relationship("Field", back_populates="instances_fields")
    creator = relationship("User", back_populates="instances_fields")

    # one-to-many relationship(s)
    # instances_fields = relationship("InstanceField", back_populates="instance")
    # histories = relationship("History", back_populates="instance")

    def __repr__(self):
        return f'''
InstanceField(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
instance_id: {self.instance_id}
field_id: {self.field_id}
value: {self.value}
creator_id: {self.creator_id}
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
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    superior_group_id = Column(BigInteger, ForeignKey("groups.id"))

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="created_groups")
    # one-to-many relationship(s)
    positions = relationship("Position", back_populates="group")
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
admin_id: {self.creator_id},
superior_group_id: {self.superior_group_id}
)
'''

    @property
    def roles(self) -> Optional[List['Role']]:
        return inspect(self).session.query(Role).join(Role.positions).filter(Position.group_id == self.id).all()

    @property
    def joiners(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position). \
            filter(Position.group_id == self.id).all()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), unique=True)
    role = Column(Enum("admin", "group_admin", "handler", "applicant", name="role_enum"))
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="created_roles")

    # one-to-many relationship(s)
    positions = relationship("Position", back_populates="role")

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

    @property
    def groups(self) -> Optional[List['Group']]:
        return inspect(self).session.query(Group).join(Group.positions).filter(Position.role_id == self.id).all()

    @property
    def roles_without_group(self) -> Optional[List['Role']]:
        return inspect(self).session.query(Role).join(Role.positions).filter_by(group_id=None).all()


class Phase(Base):
    __tablename__ = "phases"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    name = Column(String(100))
    # order = Column(Integer) #For later consideration
    description = Column(String)
    position_id = Column(BigInteger, ForeignKey("positions.id"))
    phase_type = Column(Enum("begin", "transit", "end", name="phase_enum"))

    # many-to-one relationship(s)
    form = relationship("Form", back_populates="phases")
    position = relationship("Position", back_populates="phases")

    # one-to-many relationship(s)
    instances = relationship("Instance", back_populates="current_phase")
    sections = relationship("Section", back_populates="phase")
    from_transitions = relationship("Transition", back_populates="from_phase", foreign_keys="Transition.from_phase_id")
    to_transitions = relationship("Transition", back_populates="to_phase", foreign_keys="Transition.to_phase_id")

    def __repr__(self):
        return f'''
Phase(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_id: {self.form_id}
description: {self.description}
position_id: {self.position_id}
phase_type: {self.phase_type}
)
'''

    @property
    def creator(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.created_forms).join(Form.phases). \
            filter(Phase.id == self.id).first()

    @property
    def next_phases(self) -> Optional[List['Phase']]:
        return inspect(self).session.query(Phase).join(Phase.to_transitions). \
            filter(Transition.from_phase_id == self.id).all()

    @property
    def prev_phases(self) -> Optional[List['Phase']]:
        return inspect(self).session.query(Phase).join(Phase.from_transitions). \
            filter(Transition.to_phase_id == self.id).all()

    @property
    def positions(self) -> Optional[List['Position']]:
        return inspect(self).session.query(Position).join(Position.sections).filter(Section.phase_id == self.id).all()

    @property
    def fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).filter(Section.phase_id == self.id).all()

    @property
    def available_users(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position). \
            join(Position.sections).filter(Section.phase_id == self.id).all()


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
    from_phase = relationship("Phase", back_populates="from_transitions", foreign_keys=[from_phase_id])
    to_phase = relationship("Phase", back_populates="to_transitions", foreign_keys=[to_phase_id])

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

    @property
    def creator(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.created_forms).join(Form.phases). \
            join(Phase.from_transitions).filter(Transition.id == self.id).first()


class Position(Base):
    __tablename__ = 'positions'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(100))
    group_id = Column(BigInteger, ForeignKey("groups.id"))
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    # many-to-one relationship(s)
    group = relationship("Group", back_populates="positions")
    role = relationship("Role", back_populates="positions")
    creator = relationship("User", back_populates="created_positions")

    # one-to-many relationship(s)
    phases = relationship("Phase", back_populates="position")
    users_positions = relationship("UserPosition", back_populates="position")
    sections = relationship("Section", back_populates="position")

    def __repr__(self):
        return f'''
Position(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
group_id: {self.group_id}
role_id: {self.role_id}
creator_id: {self.creator_id}
)
'''

    @property
    def holders(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions). \
            filter(UserPosition.position_id == self.id).all()

    @property
    def available_fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).filter(Section.position_id == self.id).all()

    @property
    def available_instances(self) -> Optional[List['Instance']]:
        return inspect(self).session.query(Instance).join(Instance.current_phase).join(Phase.sections). \
            filter(Section.position_id == self.id).filter(Instance.current_state == 'pending').all()


class UserPosition(Base):
    __tablename__ = 'users_positions'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    creator_id = Column(BigInteger, ForeignKey("users.id"))
    user_id = Column(BigInteger, ForeignKey("users.id"))
    position_id = Column(BigInteger, ForeignKey("positions.id"))

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="created_users_positions", foreign_keys=[creator_id])
    user = relationship("User", back_populates="users_positions", foreign_keys=[user_id])
    position = relationship("Position", back_populates="users_positions")

    def __repr__(self):
        return f'''
UserPosition(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
creator_id: {self.creator_id}
user_id: {self.user_id}
position_id: {self.position_id}
)
'''
