from ORM.Model.FormStructure import FormStructure
from ORM.session import session
from ORM.ModelConstructor.FormTemplate import FormTemplateModelConstructor

form_structure = session.query(FormStructure).first()

table_constructor = FormTemplateModelConstructor(form_structure)
table_constructor.create_table()
table_constructor.add_rel_to_FormStructure()
