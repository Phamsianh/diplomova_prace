import json
import os


class FormTemplateModelConstructor:
    def __init__(self, form_structure):
        self.form_structure = form_structure
        self.structure = json.loads(form_structure.structure)
        self.form_structure_id = form_structure.id
        self.file_name = "FormTemplate" + str(self.form_structure_id) + ".py"
        self.file_path = "ORM/Model/" + self.file_name
        self.string = ''

    def create_table(self):
        self.create_file()
        if self.execute_file():
            print('Model created')
            self.add_rel_to_FormStructure()
            self.clean_up()
            print('Model is created sucessfully')
        else:
            print('Fail to create model')

    def create_file(self):
        self.add_import()
        self.add_class()
        # self.add_dynamic_section()
        self.add__repr__()
        self.add_create_all_command()
        f = open(self.file_path, 'w')
        f.write(self.string)
        f.close()
        print(self.string)

    def add_import(self):
        self.string = '''from sqlalchemy import Column, String, TIMESTAMP, BigInteger, Integer, text, JSON, ForeignKey
from ORM.Base import Base
from ORM.engine import engine\n
'''

    def add_class(self):
        self.string += f'''
class FormTemplate{self.form_structure_id}(Base):
    __tablename__ = "form_template_{self.form_structure_id}"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    form_structure_id = Column(BigInteger, ForeignKey('form_structures.id'))   
    state = Column(String(20), default=text('init'))
    data = Column(JSON)
'''

#     def add_dynamic_section(self):
#         for i in range(1, len(self.structure)):
#             self.string += f'''
#     section_{i}_name = Column(String, default=text('{self.structure[i]['section_name']}'))
#     section_{i}_fields = Column(JSON)
#     section_{i}_description = Column(String)
#     section_{i}_digital_signature = Column(JSON)
# '''

    def add__repr__(self):
        self.string += '''
    def __repr__(self):
        return f\'\'\''''

        self.string += f'''
FormTemplate{self.form_structure_id}('''

        self.string += '''
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_structure_id: {self.form_structure_id}
state: {self.state}
data: {self.data}'''
        # for i in range(1, len(self.structure)):
        #     self.string += f'\nsection_{i}_name: ' + '{self.section_' + str(i) + '_name}'
        #     self.string += f'\nsection_{i}_fields: ' + '{self.section_' + str(i) + '_fields}'
        #     self.string += f'\nsection_{i}_description: ' + '{self.section_' + str(i) + '_description}'
        #     self.string += f'\nsection_{i}_admin_digital_signature: ' + '{self.section_' + str(i) + '_admin_digital_signature}'

        self.string += "\n\'\'\'\n\n"

    def add_create_all_command(self):
        self.string += '''
if __name__ == "__main__":
    from ORM.Model.FormStructure import FormStructure
    Base.metadata.create_all(engine)'''

    def execute_file(self):
        command = 'python ' + self.file_path
        print("command executed: " + command)
        return not(os.system(command))

    def add_rel_to_FormStructure(self):
        f = open('ORM/Model/FormStructure.py', 'r')
        string = f.read()

        add_import = f'from ORM.Model.FormTemplate{self.form_structure_id} import FormTemplate{self.form_structure_id}\n'
        string = string[:0] + add_import + string[0:]

        if 'from sqlalchemy.orm import relationship' not in string:
            add_import = 'from sqlalchemy.orm import relationship\n'
            string = string[:0] + add_import + string[0:]

        add_relationship = f'''
    
    form_template_{self.form_structure_id} = relationship("FormTemplate{self.form_structure_id}", backref='form_structure')'''

        string += add_relationship

        f = open('ORM/Model/FormStructure.py', 'w')
        f.write(string)
        f.close()
        print(string)

    def clean_up(self):
        f = open(self.file_path, 'r')
        string = f.read()
        f.close()

        index = string.index('''
if __name__ == "__main__":
    from ORM.Model.FormStructure import FormStructure
    Base.metadata.create_all(engine)''')

        string = string[0:index]
        f = open(self.file_path, 'w')
        f.write(string)
        f.close()
        print(string)
