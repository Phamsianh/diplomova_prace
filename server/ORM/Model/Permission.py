from ORM.Base import Base
from ORM.engine import engine
from sqlalchemy import Column, TIMESTAMP, BigInteger, text, Boolean, ForeignKey


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    role_id = Column(BigInteger, ForeignKey('roles.id'))

    create_form_structure = Column(Boolean, default=False)
    read_form_structure = Column(Boolean, default=False)
    update_form_structure = Column(Boolean, default=False)
    delete_form_structure = Column(Boolean, default=False)

    create_user = Column(Boolean, default=False)
    read_user = Column(Boolean, default=False)
    update_user = Column(Boolean, default=False)
    delete_user = Column(Boolean, default=False)

    create_role = Column(Boolean, default=False)
    read_role = Column(Boolean, default=False)
    update_role = Column(Boolean, default=False)
    delete_role = Column(Boolean, default=False)

    create_form_instance = Column(Boolean, default=True)
    read_form_instance = Column(Boolean, default=True)
    update_form_instance = Column(Boolean, default=True)
    delete_form_instance = Column(Boolean, default=True)

    def __repr__(self):
        return f'''
Permission(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}

create_form_structure: {self.create_form_structure}
read_form_structure: {self.read_form_structure}
update_form_structure: {self.update_form_structure}
delete_form_structure: {self.delete_form_structure}

create_user: {self.create_user}
read_user: {self.read_user}
update_user: {self.update_user}
delete_user: {self.delete_user}

create_role: {self.create_role}
read_role: {self.read_role}
update_role: {self.update_role}
delete_role: {self.delete_role}

create_form_instance: {self.create_form_instance}
read_form_instance: {self.read_form_instance}
update_form_instance: {self.update_form_instance}
delete_form_instance: {self.delete_form_instance}
)
'''


# if __name__ == "__main__":
#     from ORM.Model.Role import Role
#     Base.metadata.create_all(engine)
