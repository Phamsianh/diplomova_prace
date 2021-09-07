from ORM.Model import User, Form, GroupRole, UserGroupRole, Section, Phase
from ORM.session import session


def get_all_available_phases_sections(u: User, f: Form):
    f_sections = get_all_sections(f)
    u_groups_roles = get_all_groups_roles(u)
    available_phases = set()
    available_sections = []
    for s in f_sections:
        if s.group_role in u_groups_roles:
            available_sections.append(s)
            available_phases.add(s.phase)

    return {
        "available_phases": list(available_phases),
        "available_sections": available_sections
    }


def get_all_sections(f: Form) -> list[Section]:
    return session.query(Section) \
        .join(Section.phase) \
        .join(Phase.form) \
        .filter(Form.id == f.id).all()


def get_all_groups_roles(u: User) -> list[GroupRole]:
    return session.query(GroupRole) \
        .join(GroupRole.users_groups_roles) \
        .join(UserGroupRole.user).filter(User.id == u.id).all()
