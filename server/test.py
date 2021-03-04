from ORM.ModelConstructor.FormTemplate import FormTemplateModelConstructor
from ORM.Model.FormStructure import FormStructure
from ORM.session import session
import json

form_structure = session.query(FormStructure).first()
# print(type(json.loads(structure)))

constructor = FormTemplateModelConstructor(form_structure)
constructor.create_table()