from ORM.Base import Base
from ORM.engine import engine
from sqlalchemy import Column, String, TIMESTAMP, BigInteger, text
from sqlalchemy.orm import relationship
from ORM.Model.UserRole import UserRole
from ORM.Model.Permission import Permission


class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    name = Column(String(50), unique=True)
    role_users = relationship("UserRole", backref="role")
    permission = relationship("Permission", backref="role")

    def __repr__(self):
        return f'''
Role(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
name: {self.name}
)
'''


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)