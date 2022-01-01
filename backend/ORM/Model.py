from ORM.Base import Base
from ORM.session import Session
from sqlalchemy import Column, ForeignKey, BigInteger, String, DateTime, Date, Integer, Enum, Boolean, func, inspect, \
    text
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
    user_name = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String, nullable=False)
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
    receivers = relationship("Receiver", back_populates="user")

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

    @property
    def potential_instances(self) -> Optional[List['Instance']]:
        handled_sections = inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields).\
            filter(Section.phase_id == Phase.id, InstanceField.instance_id == Instance.id)
        return inspect(self).session.query(Instance).join(Instance.current_phase).join(Phase.sections).\
            join(Section.position).join(Position.users_positions).join(UserPosition.user).\
            filter(User.id == self.id, ~handled_sections.exists()).all()


class Form(Base):
    __tablename__ = "forms"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    public = Column(Boolean, server_default='false')
    obsolete = Column(Boolean, server_default='false')

    # many-to-one relationship(s)
    creator = relationship("User", back_populates="created_forms")

    # one-to-many relationship(s)
    phases = relationship("Phase", cascade="all, delete", back_populates="form")
    instances = relationship("Instance", back_populates="form")

    def __repr__(self):
        return f'''
Form(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
creator_id: {self.creator_id}
public: {self.public}
obsolete: {self.obsolete}
)
'''

    @property
    def sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.form).\
            filter(Form.id == self.id).all()

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
    def begin_phases(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form) \
            .filter(Form.id == self.id). \
            filter(Phase.phase_type == 'begin').all()

    @property
    def end_phases(self) -> Optional['Phase']:
        return inspect(self).session.query(Phase).join(Phase.form) \
            .filter(Form.id == self.id). \
            filter(Phase.phase_type == 'end').all()

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
    name = Column(String, nullable=False)
    phase_id = Column(BigInteger, ForeignKey("phases.id", ondelete="CASCADE"))
    position_id = Column(BigInteger, ForeignKey("positions.id"))
    order = Column(Integer)

    # many-to-one relationship(s)
    phase = relationship("Phase", back_populates="sections")
    position = relationship("Position", back_populates="sections")

    # one-to-many relationship(s)
    fields = relationship("Field", cascade="all, delete", back_populates="section")
    receivers = relationship("Receiver", back_populates="section")

    def __repr__(self):
        return f'''
Section(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
phase_id: {self.phase_id}
position_id: {self.position_id}
order: {self.order}
)
'''

    @property
    def creator(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.created_forms).join(Form.phases).join(Phase.sections). \
            filter(Section.id == self.id).first()

    @property
    def form(self) -> Optional['Form']:
        return inspect(self).session.query(Form).join(Form.phases).join(Phase.sections).\
            filter(Section.id == self.id).first()

    @property
    def public(self) -> bool:
        return self.phase.public

    @property
    def obsolete(self) -> bool:
        return self.form.obsolete

    @property
    def potential_handlers(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions). \
            filter(UserPosition.position_id == self.position_id).all()


class Field(Base):
    __tablename__ = "fields"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    section_id = Column(BigInteger, ForeignKey("sections.id", ondelete="CASCADE"))
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

    @property
    def public(self) -> bool:
        return self.section.public

    @property
    def obsolete(self) -> bool:
        return self.form.obsolete

    def content(self, instance_id):
        return inspect(self).session.query(InstanceField)\
            .filter(InstanceField.instance_id == instance_id, InstanceField.field_id == self.id)\
            .first()


class Instance(Base):
    __tablename__ = "instances"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    current_phase_id = Column(BigInteger, ForeignKey("phases.id"))
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    _current_state = Column("current_state", Enum(
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
    instances_fields = relationship("InstanceField", cascade="all,delete", back_populates="instance")
    receivers = relationship("Receiver", back_populates="instance")
    commits = relationship("Commit", back_populates="instance")
    head = relationship("Head", back_populates="instance", uselist=False)

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
    def current_state(self):
        current_appointed_positions = self.current_appointed_positions
        number_of_part = len(current_appointed_positions)
        uninit = 0
        init = 0
        resolving = 0
        resolved = 0

        for c_a_p in current_appointed_positions:
            part_state = self.part_state(self.current_phase_id, c_a_p.id)
            if part_state is None:
                uninit += 1
                continue
            if part_state == "init":
                init += 1
                continue
            if part_state == "resolving":
                resolving += 1
                continue
            if part_state == "resolved":
                resolved += 1

        if uninit == number_of_part:
            return "pending"
        if resolved == number_of_part:
            return "done" if self.current_phase.phase_type == "end" else "full resolved"
        if init == number_of_part or resolving == number_of_part or init + resolving == number_of_part:
            return "initialized" if self.current_phase.phase_type == "begin" else "full received"
        if uninit > 0:
            if resolved == 0:
                return "partial received"
            else:
                return "partial received & partial resolved"
        else:
            return "full received & partial resolved"

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
    def participants(self) -> Optional['User']:
        return inspect(self).session.query(User).join(User.instances_fields).\
            filter(InstanceField.instance_id == self.id).all()

    @property
    def current_appointed_positions(self) -> Optional[List['Position']]:
        return inspect(self).session.query(Position).join(Position.sections).join(Section.phase).join(Phase.instances).\
            filter(Instance.id == self.id).all()

    @property
    def current_remaining_positions(self) -> Optional[List['Position']]:
        handled_sections = inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields). \
            join(InstanceField.instance).filter(Section.position_id == Position.id, Instance.id == self.id)
        return inspect(self).session.query(Position).join(Position.sections).join(Section.phase).join(Phase.instances).\
            filter(Instance.id == self.id, ~handled_sections.exists()).all()

    @property
    def current_designated_position(self) -> Optional['Position']:
        return inspect(self).session.query(Position).join(Position.phases).join(Phase.instances). \
            filter(Instance.id == self.id).first()

    @property
    def current_handled_position(self) -> Optional[List['Position']]:
        handled_sections = inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields).\
            filter(Position.id == Section.position_id, Instance.id == self.id)
        return inspect(self).session.query(Position).join(Position.sections).join(Section.phase).join(Phase.instances).\
            filter(Instance.id == self.id, handled_sections.exists()).all()

    def part_state(self, phase_id: int, position_id: int) -> Optional[str]:
        session = inspect(self).session
        sections = session.query(Section).join(Section.fields).join(Field.instances_fields).\
            filter(Section.phase_id == phase_id, Section.position_id == position_id,
                   InstanceField.instance_id == self.id).all()
        if not sections:
            return None
        else:
            state = ''
            for s in sections:
                section_state = self.section_state(s.id)
                if section_state == 'resolving':
                    return 'resolving'
                if section_state == 'resolved':
                    state += 'r'
                else:
                    state += 'i'
            return 'resolved' if 'i' not in state else 'init' if 'r' not in state else 'resolving'

    @property
    def sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.form).join(Form.instances). \
            filter(Instance.id == self.id).all()

    def sections_of_part(self, position_id: int) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.form).\
            filter(Form.id == self.form_id, Section.position_id == position_id).all()

    @property
    def current_sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.instances). \
            filter(Instance.id == self.id).all()

    @property
    def current_init_sections(self) -> Optional[List['Section']]:
        init_fields = inspect(self).session.query(Instance).join(Instance.instances_fields). \
            join(InstanceField.field).filter(Field.section_id == Section.id, Instance.id == self.id)
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.instances). \
            filter(Instance.id == self.id, init_fields.exists(), text(f"""null = all (
        select instances_fields.resolved from instances_fields
        join instances on instances.id = instances_fields.instance_id
        join fields on instances_fields.field_id = fields.id
        where sections.id = fields.section_id and instances.id = {self.id}
        )""")).all()

    @property
    def resolved_sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields). \
            filter(InstanceField.instance_id == self.id, InstanceField.resolved == True).all()

    @property
    def current_resolved_sections(self) -> Optional[List['Section']]:
        # pass
        session = inspect(self).session
        current_sections: List['Section'] = session.query(Section).join(Section.phase).join(Phase.instances).\
            filter(Instance.id == self.id).all()
        current_resolved_sections = []
        for s in current_sections:
            if self.is_section_resolved(s.id):
                current_resolved_sections.append(s)
        return None if not current_resolved_sections else current_resolved_sections

    @property
    def current_resolving_sections(self) -> Optional[List['Section']]:
        resolving_fields = inspect(self).session.query(Instance).join(Instance.instances_fields).\
            join(InstanceField.field).\
            filter(
            Field.section_id == Section.id, Instance.id == self.id, InstanceField.resolved == False
        )
        return inspect(self).session.query(Section).join(Section.phase).join(Phase.instances). \
            filter(Instance.id == self.id, resolving_fields.exists()).all()

    def section_state(self, section_id: int) -> Optional[str]:
        session = inspect(self).session
        fields = session.query(Field).join(Field.instances_fields).\
            filter(Field.section_id == section_id, InstanceField.instance_id == self.id)
        if not fields:
            return None
        else:
            state = ''
            for f in fields:
                field_state = self.field_state(f.id)
                if field_state == 'resolving':
                    return 'resolving'
                if field_state == 'resolved':
                    state += 'r'
                else:
                    state += 'i'
            return 'resolved' if 'i' not in state else 'init' if 'r' not in state else 'resolving'

    @property
    def fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form) \
            .join(Form.instances).filter(Instance.id == self.id).all()

    def fields_of_part(self, position_id: int) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form).\
            filter(Form.id == self.form_id, Section.position_id == position_id).all()

    @property
    def begin_fields(self) -> Optional['Field']:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase).join(Phase.form).\
            join(Form.instances).filter(Instance.id == self.id, Phase.phase_type == 'begin').all()

    def field_state(self, field_id: int) -> Optional[str]:
        instance_field = inspect(self).session.query(InstanceField).\
                filter(InstanceField.instance_id == self.id, InstanceField.field_id == field_id).first()
        if not instance_field:
            return None
        else:
            if instance_field.resolved:
                return 'resolved'
            else:
                return 'init' if instance_field.value is None else 'resolving'

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
    def current_director(self) -> Optional[User]:
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position).\
            join(Position.phases).join(Phase.instances).join(Instance.instances_fields).\
            filter(InstanceField.instance_id == self.id, InstanceField.creator_id == User.id).first()

    @property
    def current_potential_director(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position).\
            join(Position.phases).join(Phase.instances).\
            filter(Instance.id == self.id).all()

    @property
    def curr_handlers(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.instances_fields).join(InstanceField.field). \
            join(Field.section).join(Section.phase).join(Phase.instances).filter(Instance.id == self.id).all()

    @property
    def current_potential_handlers(self) -> Optional[List['User']]:
        handled_sections = inspect(self).session.query(Section).join(Section.fields).join(Field.instances_fields).\
            filter(InstanceField.instance_id == self.id, Position.id == Section.position_id)
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position).\
            join(Position.sections).join(Section.phase).join(Phase.instances).\
            filter(Instance.id == self.id, ~handled_sections.exists()).all()

    def section_handler(self, section_id: int) -> Optional['User']:
        return inspect(self).session.query(User).join(User.instances_fields).join(InstanceField.field). \
            filter(InstanceField.instance_id == self.id, Field.section_id == section_id).first()

    @property
    def latest_envelopes(self) -> Optional[List['Envelope']]:
        last_hash_commit = self.head.last_hash_commit
        return inspect(self).session.query(Envelope)\
            .join(Envelope.trees_envelopes)\
            .join(TreeEnvelope.tree)\
            .join(Tree.commit)\
            .filter(Commit.hash_commit == last_hash_commit).all()


class InstanceField(Base):
    __tablename__ = "instances_fields"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    instance_id = Column(BigInteger, ForeignKey("instances.id", ondelete="CASCADE"))
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


class Receiver(Base):
    __tablename__ = "receiver"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    instance_id = Column(BigInteger, ForeignKey("instances.id"))
    section_id = Column(BigInteger, ForeignKey("sections.id"))
    receiver_id = Column(BigInteger, ForeignKey("users.id"))

    # relationship(s) many-to-one
    instance = relationship("Instance", back_populates="receivers")
    section = relationship("Section", back_populates="receivers")
    user = relationship("User", back_populates="receivers")


class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(100), nullable=False)
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
    name = Column(String(50), unique=True, nullable=False)
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

    @property
    def holders(self) -> Optional[List['User']]:
        return inspect(self).session.query(User).join(User.users_positions).join(UserPosition.position).\
            filter(Position.role_id == self.id).all()


class Phase(Base):
    __tablename__ = "phases"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    form_id = Column(BigInteger, ForeignKey("forms.id"))
    name = Column(String(100), nullable=False)
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
    from_transitions = relationship("Transition", cascade="all, delete", back_populates="from_phase", foreign_keys="Transition.from_phase_id")
    to_transitions = relationship("Transition", cascade="all, delete", back_populates="to_phase", foreign_keys="Transition.to_phase_id")

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

    @property
    def public(self) -> bool:
        return self.form.public

    @property
    def obsolete(self) -> bool:
        return self.form.obsolete

    @property
    def designated_sections(self) -> Optional[List['Section']]:
        return inspect(self).session.query(Section).join(Section.phase).\
            filter(Section.position_id == Phase.position_id, Phase.position_id == self.id).all()

    @property
    def designated_fields(self) -> Optional[List['Field']]:
        return inspect(self).session.query(Field).join(Field.section).join(Section.phase). \
            filter(Section.position_id == Phase.position_id, Phase.position_id == self.id).all()


class Transition(Base):
    __tablename__ = "transitions"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50))
    from_phase_id = Column(BigInteger, ForeignKey("phases.id", ondelete="CASCADE"))
    to_phase_id = Column(BigInteger, ForeignKey("phases.id", ondelete="CASCADE"))
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

    @property
    def form(self) -> Optional['Form']:
        return inspect(self).session.query(Form).join(Form.phases).join(Phase.from_transitions).\
            filter(Transition.id == self.id).first()

    @property
    def public(self) -> bool:
        return self.from_phase.public

    @property
    def obsolete(self) -> bool:
        return self.from_phase.obsolete


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


class Envelope(Base):
    __tablename__ = "envelopes"

    hash_envelope = Column(String, primary_key=True, unique=True)
    encrypted_content = Column(String)
    digital_signature = Column(String)
    field_id = Column(BigInteger, ForeignKey('fields.id'), nullable=False)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    resolved = Column(Boolean)

    # many-to-one relationship(s)
    creator = relationship("User", backref="envelopes")
    field = relationship("Field", backref="envelopes")

    # one-to-many relationship(s)
    trees_envelopes = relationship('TreeEnvelope', back_populates='envelope')


class Tree(Base):
    __tablename__ = "trees"

    hash_tree = Column(String, primary_key=True)

    # one-to-one relationship(s)
    commit = relationship('Commit', back_populates="tree", uselist=False)
    # one-to-many relationship(s)
    trees_envelopes = relationship('TreeEnvelope', back_populates='tree')


class TreeEnvelope(Base):
    __tablename__ = "trees_envelopes"

    id = Column(BigInteger, primary_key=True)
    hash_tree = Column(String, ForeignKey('trees.hash_tree'))
    hash_envelope = Column(String, ForeignKey('envelopes.hash_envelope'))

    envelope = relationship('Envelope', back_populates="trees_envelopes")
    tree = relationship('Tree', back_populates='trees_envelopes')


class Commit(Base):
    __tablename__ = "commits"

    hash_commit = Column(String, primary_key=True)
    prev_hash_commit = Column(String, ForeignKey('commits.hash_commit'))
    hash_tree = Column(String, ForeignKey('trees.hash_tree'), unique=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    instance_id = Column(BigInteger, ForeignKey("instances.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    current_phase_id = Column(BigInteger, ForeignKey("phases.id"))

    # one-to-one relationship(s)
    tree = relationship('Tree', back_populates='commit')
    head = relationship('Head', back_populates='last_commit', uselist=False)
    # many-to-one relationship(s)
    instance = relationship('Instance', back_populates='commits')
    prev_commit = relationship('Commit', backref="next_commit", remote_side=[hash_commit])

    @property
    def envelopes(self):
        return inspect(self).session.query(Envelope).join(Envelope.trees_envelopes).join(TreeEnvelope.tree).join(Tree.commit).\
            filter(Commit.hash_commit == self.hash_commit).all()


class Head(Base):
    __tablename__ = "heads"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    instance_id = Column(BigInteger, ForeignKey('instances.id'))
    last_hash_commit = Column(String, ForeignKey('commits.hash_commit'))

    # one-to-one relationship(s)
    last_commit = relationship('Commit', back_populates='head')
    instance = relationship('Instance', back_populates='head')


class ASafe(Base):
    __tablename__ = "asafes"

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    instance_id = Column(BigInteger, ForeignKey("instances.id"), nullable=False)
    key = Column(String)
    type = Column(String, Enum(
        'aes',
        name='akey_type'
    ), server_default='aes')
    length = Column(Integer, Enum('128', '192', '256', name='akey_length'), server_default='256')

    creator = relationship("User", backref="asafes")
    instance = relationship('Instance', backref='asafes')


class PPSafe(Base):
    __tablename__ = "ppsafes"

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    public_key = Column(String)
    private_key = Column(String)
    type = Column(String, Enum('ecc', name="ppkey_type"))
    length = Column(Integer)

    creator = relationship("User", backref="ppsafes")
