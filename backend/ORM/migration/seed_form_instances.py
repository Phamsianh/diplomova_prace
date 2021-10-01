from ORM.session import session
from ORM.Model import Instance, InstanceField, User

psa = session.query(User).get(1)

instance_data = {
    "form_id": 1,
    "current_phase_id": 1,
    "creator_id": 1,
    "current_state": "done",
}
instance1 = Instance(**instance_data)
session.add(instance1)
session.commit()

instance_fields_data = [
    {
        "instance_id": instance1.id,
        "field_id": 1,
        "value": "Student Pham Si Anh initialized this form instance.",
        "creator_id": 1
    },
    {
        "instance_id": instance1.id,
        "field_id": 2,
        "value": "Leading Teacher Alexandr Stefek participated this form instance.",
        "creator_id": 6
    },
    {
        "instance_id": instance1.id,
        "field_id": 3,
        "value": "Consultant Alexandr Stefek participated this form instance.",
        "creator_id": 6
    },
    {
        "instance_id": instance1.id,
        "field_id": 5,
        "value": "HoDoICO Petr Frantis participated this form instance.",
        "creator_id": 5
    },
    {
        "instance_id": instance1.id,
        "field_id": 6,
        "value": "Dean of FMT Vlastimil Neumann participated this form instance.",
        "creator_id": 3
    }
]

instance1.instances_fields = [
    InstanceField(**field) for field in instance_fields_data
]

session.commit()
