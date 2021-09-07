from ORM.session import session
from ORM.Model import Form, Phase, Transition, Section, Field


def create_form_structure(form_structure):
    form = Form(
        name=form_structure["name"],
        creator_id=form_structure["creator_id"]
    )

    for p in form_structure["workflow"]["phases"]:
        phase = create_phase(p)
        form.phases.append(phase)

    # form is now is a Form instance contain phases. We can access phases of form
    for t in form_structure["workflow"]["transitions"]:
        create_transition(
            name=t["name"],
            fp=form.phases[t["from_phase"]-1],
            tp=form.phases[t["to_phase"]-1],
        )
        session.add(form)
        session.commit()
    return form


def create_phase(p):
    phase = Phase(
        name=p["name"] if "name" in p else None,
        description=p["description"] if "description" in p else None,
        group_role_id=p["group_role_id"],
        phase_type=p["phase_type"]
    )

    for s in p["sections"]:
        phase.sections.append(create_section(s))

    return phase


# def create_phase_group_role(p_g_r: PhaseGroupRole, p_id: int):
#     phase_group_role = PhaseGroupRole(
#         phase_id=p_id,
#         group_role_id=p_g_r["group_role_id"]
#     )
#     session.add(phase_group_role)
#     session.commit()
#
#     for s in p_g_r["sections"]:
#         create_section(s, phase_group_role.id)
#
#     return phase_group_role


def create_section(s):
    section = Section(
        name=s["name"],
        group_role_id=s["group_role_id"]
    )
    for f in s["fields"]:
        section.fields.append(create_field(f))
    return section


def create_field(f):
    field = Field(
        name=f["name"],
    )
    return field


def create_transition(name, fp: Phase, tp: Phase):
    transition = Transition(
        name=name,
    )
    transition.from_phase = fp
    transition.to_phase = tp
    return transition
