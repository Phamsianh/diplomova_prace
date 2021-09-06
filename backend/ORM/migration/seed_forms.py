from ORM.migration.seed_data.form1_structure import form1_structure
from utils.form_utils import create_form_structure

create_form_structure(form1_structure)

# from ORM.session import session
# from ORM.Model1 import User, Form, Phase, Transition,\
# GroupRole, PhaseGroupRole, Section, Field, FormInstance, FormInstanceField
#
# phamsianh = session.query(User).filter_by(user_name="phamsianh97").first()
#
# student_of_CIT = session.query(GroupRole).filter_by(name="Student of 2-CIT-C").first()
# leading_teacher = session.query(GroupRole).filter_by(name="Leading Teacher").first()
# consultant = session.query(GroupRole).filter_by(name="Consultant").first()
# head_of_DoICO = session.query(GroupRole).filter_by(name="Head of Department of\
# Informatics and Cyber Operations").first()
# vice_dean_FMT = session.query(GroupRole).filter_by(name="Vice Dean of FMT").first()
# dean_FMT = session.query(GroupRole).filter_by(name="Dean of FMT (GrAdmin)").first()
#
#
# form1 = Form(name="NÁVRH TÉMATU ZÁVĚREČNÉ PRÁCE", creator_id=phamsianh.id)
# form2 = Form(name="Form 2", creator_id=phamsianh.id)
# session.add_all([form1, form2])
# session.commit()
#
# phase1 = Phase(
#     name="phase1",
#     form_id=form1.id,
#     group_role_id=student_of_CIT.id,
#     phase_type="begin"
# )
# phase2 = Phase(
#     name="phase2",
#     form_id=form1.id,
#     group_role_id=leading_teacher.id,
#     phase_type="transit"
# )
# phase3 = Phase(
#     name="phase3",
#     form_id=form1.id,
#     group_role_id=vice_dean_FMT.id,
#     phase_type="transit"
# )
# phase4 = Phase(
#     name="phase4",
#     form_id=form1.id,
#     group_role_id=head_of_DoICO.id,
#     phase_type="transit"
# )
# phase5 = Phase(
#     name="phase5",
#     form_id=form1.id,
#     group_role_id=dean_FMT.id,
#     phase_type="end"
# )
# session.add_all([phase1, phase2, phase3, phase4, phase5])
# session.commit()
#
# transition1 = Transition(
#     name="From 1 to 2",
#     from_phase_id=phase1.id,
#     to_phase_id=phase2.id,
# )
# transition2 = Transition(
#     name="From 1 to 3",
#     from_phase_id=phase2.id,
#     to_phase_id=phase4.id,
# )
# transition3 = Transition(
#     name="From 2 to 4",
#     from_phase_id=phase1.id,
#     to_phase_id=phase2.id,
# )
# transition4 = Transition(
#     name="From 3 to 5",
#     from_phase_id=phase1.id,
#     to_phase_id=phase2.id,
# )
# transition5 = Transition(
#     name="From 4 to 5",
#     from_phase_id=phase1.id,
#     to_phase_id=phase2.id,
# )
# session.add_all([transition1, transition2, transition3, transition4, transition5])
# session.commit()
#
# phase1_student_CIT = PhaseGroupRole(phase_id=phase1.id, group_role_id=student_of_CIT.id)
# phase2_leading_teacher = PhaseGroupRole(phase_id=phase2.id, group_role_id=leading_teacher.id)
# phase2_consultant = PhaseGroupRole(phase_id=phase2.id, group_role_id=consultant.id)
# phase3_vice_dean_FMT = PhaseGroupRole(phase_id=phase3.id, group_role_id=vice_dean_FMT.id)
# phase4_head_of_DoICO = PhaseGroupRole(phase_id=phase4.id, group_role_id=head_of_DoICO.id)
# phase5_dean_FMT = PhaseGroupRole(phase_id=phase2.id, group_role_id=dean_FMT.id)
# session.add_all([
#     phase1_student_CIT,
#     phase2_leading_teacher,
#     phase2_consultant,
#     phase3_vice_dean_FMT,
#     phase4_head_of_DoICO,
#     phase5_dean_FMT
# ])
# session.commit()
#
# section1 = Section(
#     name="Section for student of 2-CIT-C",
#     phase_group_role_id=phase1_student_CIT.id
# )
# section2 = Section(
#     name="Section for Leading Teacher",
#     phase_group_role_id=phase2_leading_teacher.id
# )
# section3 = Section(
#     name="Section for Consultant",
#     phase_group_role_id=phase2_consultant.id
# )
# section4 = Section(
#     name="Section for Head of Department of ICO",
#     phase_group_role_id=phase4_head_of_DoICO.id
# )
# section5 = Section(
#     name="Section for Vice Dean of FMT",
#     phase_group_role_id=phase3_vice_dean_FMT.id
# )
# section6 = Section(
#     name="Section for Dean of FMT",
#     phase_group_role_id=phase5_dean_FMT.id
# )
#
# session.add_all([section1, section2, section3, section4, section5, section6])
# session.commit()
#
# field1 = Field(
#     name="Field for student of 2-CIT-C",
#     section_id=section1.id
# )
# field2 = Field(
#     name="Field for Leading Teacher",
#     section_id=section2.id
# )
# field3 = Field(
#     name="Field for Consultant",
#     section_id=section3.id
# )
# field4 = Field(
#     name="Field for Head of Department of ICO",
#     section_id=section4.id
# )
# field5 = Field(
#     name="Field Vice Dean of FMT",
#     section_id=section5.id
# )
# field6 = Field(
#     name="Field for Dean of FMT",
#     section_id=section6.id
# )
# session.add_all([field1, field2, field3, field4, field5, field6])
# session.commit()
# session.close()
