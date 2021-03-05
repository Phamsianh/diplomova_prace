from ORM.Model.UserFormTemplate1 import UserFormTemplate1
from ORM.Base import Base
from sqlalchemy import Column, String, TIMESTAMP, BigInteger, text
from sqlalchemy.orm import relationship
from ORM.Model.FormStructure import FormStructure
from ORM.Model.UserRole import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    first_name = Column(String(50))
    last_name = Column(String(50))
    user_name = Column(String(50), unique=True)
    password = Column(String)
    email = Column(String(50), unique=True)
    phone = Column(String(20))
    public_key = Column(String)
    form_structures = relationship("FormStructure", backref="user")
    user_roles = relationship("UserRole", backref="user")


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
)
'''

    users_form_template_1 = relationship("UserFormTemplate1", backref="users")