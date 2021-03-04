from ORM.Model.FormTemplate1 import FormTemplate1
from sqlalchemy.orm import relationship
from ORM.Base import Base
from sqlalchemy import Column, String, TIMESTAMP, BigInteger, text, JSON, ForeignKey


class FormStructure(Base):
    __tablename__ = "form_structures"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    name = Column(String, unique=True)
    structure = Column(JSON)
    admin_digital_signature = Column(String)

    def __repr__(self):
        return f'''
FormStructure(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
user_id: {self.user_id}
name: {self.name}
structure: {self.structure}
admin_digital_signature: {self.admin_digital_signature}
)
'''


    
    form_template_1 = relationship("FormTemplate1", backref='form_structure')