from sqlalchemy.orm import relationship
from ORM.Model.UserFormTemplate1 import UserFormTemplate1
from sqlalchemy import Column, String, TIMESTAMP, BigInteger, text, JSON, ForeignKey
from ORM.Base import Base


class FormTemplate1(Base):
    __tablename__ = "form_template_1"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    form_structure_id = Column(BigInteger, ForeignKey('form_structures.id'))   
    state = Column(String(20), default=text('init'))
    data = Column(JSON)

    def __repr__(self):
        return f'''
FormTemplate1(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_structure_id: {self.form_structure_id}
state: {self.state}
data: {self.data}
'''



    users_form_template_1 = relationship("UserFormTemplate1", backref="form_template_1")