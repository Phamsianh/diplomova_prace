from ORM.session import session
from ORM.Model import User, Form, Phase, Transition, Position, Section, Field

phamsianh = session.query(User).filter_by(user_name="phamsianh97").first()

student = session.query(Position).filter_by(name="Student").first()
leading_teacher = session.query(Position).filter_by(name="Leading Teacher").first()
consultant = session.query(Position).filter_by(name="Consultant").first()
head_of_department = session.query(Position).filter_by(name="Head of Department").first()
vice_dean = session.query(Position).filter_by(name="Vice Dean").first()
dean = session.query(Position).filter_by(name="Dean").first()
guarantor = session.query(Position).filter_by(name="Guarantor").first()


form1 = Form(
    name="Application for approval of the proposal topic of the final thesis",
    creator_id=phamsianh.id,
    public=True
)

# ----------------------PHASE---------------------
phase_for_student = Phase(
    name="Phase for student",
    phase_type="begin",
    form=form1,
    position=student,
)
phase_for_head_of_department = Phase(
    name="Phase for Head of Department",
    form=form1,
    position=head_of_department,
    phase_type="transit"
)
phase_for_vice_dean = Phase(
    name="Phase For Vice Dean",
    form=form1,
    position=vice_dean,
    phase_type="transit"
)
phase_for_guarantor = Phase(
    name="Phase for Guarantor",
    form=form1,
    position=guarantor,
    phase_type="end"
)

# ---------------------TRANSITION--------------------
student_to_head_of_department = Transition(
    name="From Student to Head of Department",
    from_phase=phase_for_student,
    to_phase=phase_for_head_of_department,
)
head_of_department_to_student = Transition(
    name="From Head of Department to Student",
    from_phase=phase_for_head_of_department,
    to_phase=phase_for_student,
)
student_to_vice_dean = Transition(
    name="From Student to Vice-Dean",
    from_phase=phase_for_student,
    to_phase=phase_for_vice_dean,
)
vice_dean_to_guarantor = Transition(
    name="From Vice-Dean to Guarantor",
    from_phase=phase_for_vice_dean,
    to_phase=phase_for_guarantor,
)

# ---------------------SECTION----------------------
section_for_student = Section(
    name="Section for student",
    phase=phase_for_student,
    position=student,
    order=1,
)
section_for_leading_teacher = Section(
    name="Section for leading teacher",
    phase=phase_for_student,
    position=leading_teacher,
    order=2,
)
section_for_head_of_department = Section(
    name="Section for Head of Department",
    phase=phase_for_head_of_department,
    position=head_of_department,
    order=1
)
section_for_dean = Section(
    name="Section for Dean",
    phase=phase_for_vice_dean,
    position=dean
)
section_for_guarantor = Section(
    name="Section for Guarantor",
    phase=phase_for_guarantor,
    position=guarantor,
)
# ------------------FIELD--------------------------
name_and_surname = Field(
    name="Name and surname (title, rank):",
    section=section_for_student,
    order=1
)
date_place_of_birth = Field(
    name="Day, month, year and place of birth:",
    section=section_for_student,
    order=2
)
address = Field(
    name="Permanent address:",
    section=section_for_student,
    order=3
)
study_program = Field(
    name="Study program:",
    section=section_for_student,
    order=4
)
study_specialization = Field(
    name="Study specialization:",
    section=section_for_student,
    order=5
)
study_group = Field(
    name="Study group:",
    section=section_for_student,
    order=6
)
administrative_body = Field(
    name="Administrative body:",
    section=section_for_student,
    order=7
)
application_body = Field(
    name="Application body:",
    section=section_for_student,
    order=8
)
wording = Field(
    name="The wording of the proposed topic of the final thesis:",
    section=section_for_student,
    order=9
)
aim = Field(
    name="Aim of the final work:",
    section=section_for_student,
    order=10
)
description = Field(
    name="Description of solved problems:",
    section=section_for_student,
    order=11
)
rationale = Field(
    name="Rationale for the selected topic of the final thesis:",
    section=section_for_student,
    order=12
)
signature_of_leading_teacher = Field(
    name="Signature of the leading teacher:",
    section=section_for_leading_teacher,
    order=1
)
statement_of_hod = Field(
    name="Statement of the head of the department:",
    section=section_for_head_of_department,
    order=1
)
statement_of_guarantor = Field(
    name="Statement of the guarantor of the study program:",
    section=section_for_guarantor,
    order=1
)
statement_of_dean = Field(
    name="Statement of the Dean of the Faculty:",
    section=section_for_dean,
    order=1
)

session.add(form1)
session.commit()
