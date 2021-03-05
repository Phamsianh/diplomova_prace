from sqlalchemy import Column, TIMESTAMP, BigInteger, text, ForeignKey
from ORM.Base import Base


class UserFormTemplate1(Base):
    __tablename__ = "users_form_template_1"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    form_template_1_id = Column(BigInteger, ForeignKey('form_template_1.id'))
    user_id = Column(BigInteger, ForeignKey("users.id"))

    def __repr__(self):
        return f'''
UserFormTemplate1(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_template_1id: {self.form_template1_id}
user_id: {self.user_id}
'''


