from sqlalchemy import Column, String, TIMESTAMP, BigInteger, Integer, text, JSON, ForeignKey
from ORM.Base import Base
from ORM.engine import engine


class FormTemplate1(Base):
    __tablename__ = "form_template_1"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    form_structure_id = Column(BigInteger, ForeignKey('form_structures.id'))        

    section_1_name = Column(String, default=text('data on the applicant'))
    section_1_fields = Column(JSON)
    section_1_description = Column(String)
    section_1_digital_signature = Column(JSON)

    section_2_name = Column(String, default=text('declaration of the applicant'))
    section_2_fields = Column(JSON)
    section_2_description = Column(String)
    section_2_digital_signature = Column(JSON)

    def __repr__(self):
        return f'''
FormTemplate1(
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_structure_id: {self.form_structure_id}
section_1_name: {self.section_1_name}
section_1_fields: {self.section_1_fields}
section_1_description: {self.section_1_description}
section_1_admin_digital_signature: {self.section_1_admin_digital_signature}
section_2_name: {self.section_2_name}
section_2_fields: {self.section_2_fields}
section_2_description: {self.section_2_description}
section_2_admin_digital_signature: {self.section_2_admin_digital_signature}
'''


if __name__ == '__main__':
    Base.metadata.create_all(engine)