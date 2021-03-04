from ORM.Model.User import User
from ORM.Model.FormStructure import FormStructure
from ORM.session import session
import hashlib
import json

user1 = User(
    first_name='Si Anh',
    last_name='Pham',
    user_name='phamsianh97',
    password=hashlib.sha256(('password').encode()).hexdigest(),
    email='phamsianh97@gmail.com',
    phone='739875282'
)
user2 = User(
    first_name='Si Anh',
    last_name='Pham',
    user_name='phamsianh1997',
    password=hashlib.sha256(('strongpassword').encode()).hexdigest(),
    email='phamsianh1997@gmail.com',
    phone='739875282'
)
user3 = User(
    first_name='Bao Tran',
    last_name='Bui',
    user_name='buibaotran1997',
    password=hashlib.sha256(('password').encode()).hexdigest(),
    email='buibaotran1997@gmail.com',
    phone='0935332882'
)

structure = [
    {
        "section_name": "data on the applicant",
        "permission": ['client', 'staff'],
        "fields": {
            "First name": "text",
            "Last name": "text",
            "Sex": "boolean",
            "Address": "text",
            "Email": "text",
            "Telephone": "integer",
            "Date of Birth": "date",
        },
        "description": "",
        "digital_signature": ["signature of client", "signature of staff"]

    },
    {
        "section_name": "declaration of the applicant",
        "permission": ['client'],
        "fields": {
            "Name of the school": "text"
        },
        "description": "",
        "digital_signature": ["signature of client"],
    }
]
structure_json = json.dumps(structure)

form_structure_1 = FormStructure(
    user_id = 1,
    name = "APPLICATION FOR ISSUE OF AN ISIC / ISIC SCHOLAR / ITIC LICENSE",
    structure = structure_json,
    admin_digital_signature = 'admin digital signature'
)

session.add_all([user1, user2, user3])
session.add_all([form_structure_1])
session.commit()
