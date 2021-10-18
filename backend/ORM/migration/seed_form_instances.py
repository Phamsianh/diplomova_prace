from ORM.session import session
from ORM.Model import Instance, InstanceField, User

psa = session.query(User).get(1)

instance_data = {
    "form_id": 1,
    "current_phase_id": 2,
    "creator_id": 1,
}
instance1 = Instance(**instance_data)
session.add(instance1)
session.commit()

instance_fields_data = [
    {
        "instance_id": instance1.id,
        "field_id": 1,
        "value": "Student Pham Si Anh initialized this form instance.",
        "creator_id": 1,
        "resolved": True
    },
    {
        "instance_id": instance1.id,
        "field_id": 2,
        "value": "Leading Teacher Alexandr Stefek participated this form instance.",
        "creator_id": 6,
        "resolved": True
    },
    {
        "instance_id": instance1.id,
        "field_id": 4,
        "value": "Consultant Alexandr Stefek participated this form instance.",
        "creator_id": 6,
        "resolved": True
    },
    {
        "instance_id": instance1.id,
        "field_id": 6,
        "value": "HoDoICO Petr Frantis participated this form instance.",
        "creator_id": 5,
        "resolved": True
    },
    {
        "instance_id": instance1.id,
        "field_id": 7,
        "value": "Dean of FMT Vlastimil Neumann participated this form instance.",
        "creator_id": 3,
        "resolved": True
    }
]

instance1.instances_fields = [
    InstanceField(**field) for field in instance_fields_data
]

session.commit()
