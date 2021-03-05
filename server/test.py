from ORM.ModelConstructor.FormTemplate import FormTemplateModelConstructor
from ORM.ModelConstructor.UserFormTemplate import UserFormTemplateModelConstructor
from ORM.Model.FormStructure import FormStructure
from ORM.session import session

form_structure = session.query(FormStructure).first()
# print((json.loads(form_structure.structure)))

constructor = FormTemplateModelConstructor(form_structure.id)
constructor.create_model()

constructor = UserFormTemplateModelConstructor(form_structure.id)
constructor.create_model()