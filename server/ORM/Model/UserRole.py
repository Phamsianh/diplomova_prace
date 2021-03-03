from ORM.Base import Base
from sqlalchemy import Column, TIMESTAMP, BigInteger, text, ForeignKey


class UserRole(Base):
    __tablename__ = 'users_roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    role_id = Column(BigInteger, ForeignKey('roles.id'))

    def __repr__(self):
        return f'''
UserRole(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
user_id: {self.user_id}
role_id: {self.role_id}
)
'''