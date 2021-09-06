import os
from ORM.Model import User, Form
from ORM.session import session
from utils.form_authorization import get_all_available_phases_sections

os.system("python -m ORM.migration.migration")

phamsianh = session.query(User).filter_by(user_name="phamsianh97").first()
alexandrstefek = session.query(User).filter_by(user_name="alexandrstefek").first()
f1 = session.query(Form).get(1)

print(get_all_available_phases_sections(u=alexandrstefek, f=f1))
print(get_all_available_phases_sections(u=phamsianh, f=f1))
