from ORM.session import session
from ORM.Model import Form, Phase, Transition, Section, Field


def create_form_structure(form_structure):
    form = Form(
        name=form_structure["name"],
        creator_id=form_structure["creator_id"],
        public=form_structure["public"],
        obsolete=form_structure["obsolete"]
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
        position_id=p["position_id"],
        phase_type=p["phase_type"]
    )

    for s in p["sections"]:
        phase.sections.append(create_section(s))

    return phase


# def create_phase_position(p_g_r: PhaseGroupRole, p_id: int):
#     phase_position = PhaseGroupRole(
#         phase_id=p_id,
#         position_id=p_g_r["position_id"]
#     )
#     session.add(phase_position)
#     session.commit()
#
#     for s in p_g_r["sections"]:
#         create_section(s, phase_position.id)
#
#     return phase_position


def create_section(s):
    section = Section(
        name=s["name"],
        position_id=s["position_id"]
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
