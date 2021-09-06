from ORM.Model import User, Form


def get_all_available_phases_sections(u: User, f: Form):
    phases_groups_roles = get_all_phases_groups_roles(f)
    groups_roles = get_all_groups_roles(u)
    available_phases = []
    available_sections = []
    for p_g_r in phases_groups_roles:
        for g_r in groups_roles:
            if g_r.id == p_g_r.group_role_id:
                available_phases.append(p_g_r.phase)
                for s in p_g_r.sections:
                    available_sections.append(s)

    return {
        "available_phases": available_phases,
        "available_sections": available_sections
    }


def get_all_phases_groups_roles(f: Form):
    phases_groups_roles = []
    for p in f.phases:
        ps_gs_rs = p.phases_groups_roles
        for p_g_r in ps_gs_rs:
            phases_groups_roles.append(p_g_r)
    return phases_groups_roles


def get_all_groups_roles(u: User):
    g_r = []
    for u_g_r in u.users_groups_roles:
        g_r.append(u_g_r.group_role)
    return g_r



