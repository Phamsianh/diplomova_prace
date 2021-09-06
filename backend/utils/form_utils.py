from ORM.session import session
from ORM.Model import Form, Phase, Transition, PhaseGroupRole, Section, Field


def create_form_structure(form_structure):
    form = Form(
        name=form_structure["name"],
        creator_id=form_structure["creator_id"]
    )
    session.add(form)
    session.commit()
    phases_id = []
    for p in form_structure["workflow"]["phases"]:
        phases_id.append(create_phase(p, form.id).id)

    # form is now is a Form instance contain phases. We can access phases of form
    for t in form_structure["workflow"]["transitions"]:
        create_transition(
            name=t["name"],
            fp_id=phases_id[t["from_phase"]-1],
            tp_id=phases_id[t["to_phase"]-1],
        )


def create_phase(p, f_id: int):
    phase = Phase(
        form_id=f_id,
        name=p["name"] if "name" in p else None,
        description=p["description"] if "description" in p else None,
        group_role_id=p["group_role_id"],
        phase_type=p["phase_type"]
    )
    session.add(phase)
    session.commit()

    for p_g_r in p["phases_groups_roles"]:
        create_phase_group_role(p_g_r, phase.id)

    return phase


def create_phase_group_role(p_g_r: PhaseGroupRole, p_id: int):
    phase_group_role = PhaseGroupRole(
        phase_id=p_id,
        group_role_id=p_g_r["group_role_id"]
    )
    session.add(phase_group_role)
    session.commit()

    for s in p_g_r["sections"]:
        create_section(s, phase_group_role.id)

    return phase_group_role


def create_section(s, p_g_r_id: int):
    section = Section(
        name=s["name"],
        phase_group_role_id=p_g_r_id
    )
    session.add(section)
    session.commit()
    for f in s["fields"]:
        create_field(f, section.id)

    return section


def create_field(f, s_id: int):
    field = Field(
        name=f["name"],
        section_id=s_id
    )
    session.add(field)
    session.commit()

    return field


def create_transition(name, fp_id, tp_id):
    transition = Transition(
        name=name,
        from_phase_id=fp_id,
        to_phase_id=tp_id
    )
    session.add(transition)
    session.commit()
    return transition
