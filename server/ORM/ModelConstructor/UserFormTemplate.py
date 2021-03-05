import os


class UserFormTemplateModelConstructor:
    def __init__(self, form_structure_id):
        self.form_structure_id = form_structure_id
        self.file_path = f"ORM/Model/UserFormTemplate{form_structure_id}.py"
        self.string = ''

    def create_model(self):
        print('-'*10 + f'CREATE {self.file_path}' +'-'*10)
        self.create_file()
        print('-' * 10 + f'EXECUTE {self.file_path}' + '-' * 10)
        if self.execute_file():
            print('-' * 10 + f'EXECUTED {self.file_path}' + '-' * 10)
            # print('-' * 10 + f'MODEL UserFormTemplate{self.form_structure_id} CREATED' + '-' * 10)
        else:
            print('-' * 10 + f'FAILED TO CREATE MODEL UserFormTemplate{self.form_structure_id}' + '-' * 10)
        print('-' * 10 + f'ADD relationship to model User' + '-' * 10)
        self.add_rel_to_User()
        print('-' * 10 + f'ADD relationship to model User' + '-' * 10)
        self.add_rel_to_FormTemplate()
        print('-' * 10 + f'CLEAN UP' + '-' * 10)
        self.clean_up()

    def create_file(self):
        self.add_import()
        self.add_class()
        self.add__repr__()
        self.add_create_all_command()
        f = open(self.file_path, 'w')
        print(self.string)
        f.write(self.string)
        f.close()

    def add_import(self):
        self.string = '''from sqlalchemy import Column, TIMESTAMP, BigInteger, text, ForeignKey
from ORM.Base import Base\n
'''

    def add_class(self):
        self.string += f'''
class UserFormTemplate{self.form_structure_id}(Base):
    __tablename__ = "users_form_template_{self.form_structure_id}"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    form_template_{self.form_structure_id}_id = Column(BigInteger, ForeignKey('form_template_{self.form_structure_id}.id'))
    user_id = Column(BigInteger, ForeignKey("users.id"))
'''

    def add__repr__(self):
        self.string += '''
    def __repr__(self):
        return f\'\'\''''

        self.string += f'''
UserFormTemplate{self.form_structure_id}('''

        self.string += '''
id: {self.id}
created_at: {self.created_at}
updated_at: {self.updated_at}
form_template_''' + f'{self.form_structure_id}' + 'id: {self.form_template' + f'{self.form_structure_id}' + '''_id}
user_id: {self.user_id}'''

        self.string += "\n\'\'\'\n\n"

    def add_create_all_command(self):
        self.string += f'''
if __name__ == "__main__":
    from ORM.Model.FormTemplate{self.form_structure_id} import FormTemplate{self.form_structure_id}
    from ORM.Model.User import User
    from ORM.engine import engine
    Base.metadata.create_all(engine)'''

    def execute_file(self):
        command = f'python {self.file_path}'
        print(f"command executed: {command}")
        return not os.system(command)

    def add_rel_to_User(self):
        file_path = 'ORM/Model/User.py'
        f = open(file_path, 'r')
        string = f.read()
        f.close()

        add_import = f'from ORM.Model.UserFormTemplate{self.form_structure_id} import UserFormTemplate{self.form_structure_id}\n'
        if add_import not in string:
            string = string[:0] + add_import + string[0:]
        else: print(f'UserFormTemplate{self.form_structure_id} already imported in {file_path}')

        if 'from sqlalchemy.orm import relationship' not in string:
            add_import = 'from sqlalchemy.orm import relationship\n'
            string = string[:0] + add_import + string[0:]
        else: print(f'relationship from sqlalchemy already imported in {file_path}')

        add_rel = f'''
    users_form_template_{self.form_structure_id} = relationship("UserFormTemplate{self.form_structure_id}", backref="users")'''
        if add_rel not in string:
            string += add_rel
        else: print(f'relationship users_form_template_{self.form_structure_id} already existed in {file_path}')

        f = open('ORM/Model/User.py', 'w')
        f.write(string)
        print(string)
        f.close()

    def add_rel_to_FormTemplate(self):
        file_path = f'ORM/Model/FormTemplate{self.form_structure_id}.py'
        f = open(file_path, 'r')
        string = f.read()
        f.close()

        add_import = f'from ORM.Model.UserFormTemplate{self.form_structure_id} import UserFormTemplate{self.form_structure_id}\n'
        if add_import not in string:
            string = string[:0] + add_import + string[0:]
        else: print(f'UserFormTemplate{self.form_structure_id} already imported in {file_path}')

        if 'from sqlalchemy.orm import relationship' not in string:
            add_import = 'from sqlalchemy.orm import relationship\n'
            string = string[:0] + add_import + string[0:]
        else: print(f'relationship from sqlalchemy already imported in {file_path}')

        add_rel = f'''
    users_form_template_{self.form_structure_id} = relationship("UserFormTemplate{self.form_structure_id}", backref="form_template_{self.form_structure_id}")'''
        if add_rel not in string:
            string += add_rel
        else: print(f'relationship users_form_template_{self.form_structure_id} already existed in {file_path}')

        f = open(f'ORM/Model/FormTemplate{self.form_structure_id}.py', 'w')
        f.write(string)
        print(string)
        f.close()

    def clean_up(self):
        f = open(self.file_path, 'r')
        string = f.read()
        f.close()

        index = string.index('if __name__ == "__main__":')
        string = string[0:index]
        print(string)

        f = open(self.file_path, 'w')
        f.write(string)
        f.close()