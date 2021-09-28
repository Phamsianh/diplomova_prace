from pprint import pprint
from ORM.Model import Base

all_models = dict()
sup_resource = []
sub_resource = []
ass_resource = []

for m in Base.registry.mappers:
    r_1_to_m = dict()
    r_m_to_1 = dict()
    for r in m.relationships:
        sub_rsc_name = r.entity.class_.__tablename__
        rel_name = r.key
        if r.direction.name == "ONETOMANY":
            r_1_to_m[f"{sub_rsc_name}"] = rel_name
        elif r.direction.name == "MANYTOONE":
            r_m_to_1[f"{sub_rsc_name}"] = rel_name
    rsc_name = m.class_.__tablename__
    all_models[f"{rsc_name}"] = {
        "model": m.class_,
        "relationships": {
            "ONETOMANY": r_1_to_m,
            "MANYTOONE": r_m_to_1
        }
    }
    if r_1_to_m:
        sup_resource.append(rsc_name)
    else:
        ass_resource.append(rsc_name)
    if r_m_to_1:
        sub_resource.append(rsc_name)


if __name__ == "__main__":
    pprint(all_models)

    print("superior resources are:")
    pprint(sup_resource)

    print("subordinate resources are:")
    pprint(sub_resource)

    print("association resources are:")
    pprint(ass_resource)
