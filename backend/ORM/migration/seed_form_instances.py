from ORM.session import session
from ORM.Model import FormInstance, FormInstanceField, User

psa = session.query(User).get(1)

form_instance_data = {
    "form_id": 1,
    "current_phase_id": 1,
    "creator_id": 1,
    "current_state": "done",
}
form_instance1 = FormInstance(**form_instance_data)
session.add(form_instance1)
session.commit()

form_instance_fields_data = [
    {
        "form_instance_id": form_instance1.id,
        "field_id": 1,
        "value": "Student Pham Si Anh initialized this form instance.",
        "creator_id": 1
    },
    {
        "form_instance_id": form_instance1.id,
        "field_id": 2,
        "value": "Leading Teacher Alexandr Stefek participated this form instance.",
        "creator_id": 6
    },
    {
        "form_instance_id": form_instance1.id,
        "field_id": 3,
        "value": "Consultant Alexandr Stefek participated this form instance.",
        "creator_id": 6
    },
    {
        "form_instance_id": form_instance1.id,
        "field_id": 5,
        "value": "HoDoICO Petr Frantis participated this form instance.",
        "creator_id": 5
    },
    {
        "form_instance_id": form_instance1.id,
        "field_id": 6,
        "value": "Dean of FMT Vlastimil Neumann participated this form instance.",
        "creator_id": 3
    }
]

form_instance1.form_instances_fields = [
    FormInstanceField(**field) for field in form_instance_fields_data
]

session.commit()
