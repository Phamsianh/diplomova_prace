from ORM.session import session
from ORM.Model import User, GroupRole

phamsianh = session.query(User).filter_by(user_name="phamsianh97").first()

student_of_CIT = session.query(GroupRole).filter_by(name="Student of 2-CIT-C").first()
leading_teacher = session.query(GroupRole).filter_by(name="Leading Teacher").first()
consultant = session.query(GroupRole).filter_by(name="Consultant").first()
head_of_DoICO = session.query(GroupRole).filter_by(name="Head of Department of \
Informatics and Cyber Operations").first()
vice_dean_FMT = session.query(GroupRole).filter_by(name="Vice Dean of FMT").first()
dean_FMT = session.query(GroupRole).filter_by(name="Dean of FMT (GrAdmin)").first()

# Example of request
form1_structure = {
    "name": "NÁVRH TÉMATU ZÁVĚREČNÉ PRÁCE",
    "creator_id": phamsianh.id,
    "workflow": {
        "phases": [
            {
                "name": "phase1",
                "group_role_id": student_of_CIT.id,
                "phase_type": "begin",
                "phases_groups_roles": [{
                    "group_role_id": student_of_CIT.id,
                    "sections": [
                        {
                            "name": "Section for student of 2-CIT-C",
                            "phase_group_role_id": 1,
                            "fields": [
                                {
                                    "name": "Field for student of 2-CIT-C"
                                }
                            ]
                        }
                    ]
                }]
            },
            {
                "name": "phase2",
                "group_role_id": leading_teacher.id,
                "phase_type": "transit",
                "phases_groups_roles": [
                    {
                        "group_role_id": leading_teacher.id,
                        "sections": [
                            {
                                "name": "Section for Leading Teacher",
                                "fields": [
                                    {
                                        "name": "Field for Leading Teacher"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "group_role_id": consultant.id,
                        "sections": [
                            {
                                "name": "Section for Consultant",
                                "fields": [
                                    {
                                        "name": "Field for Consultant"
                                    }
                                ]
                            }
                        ]
                    },
                ]
            },
            {
                "name": "phase3",
                "group_role_id": vice_dean_FMT.id,
                "phase_type": "transit",
                "phases_groups_roles": [{
                    "group_role_id": vice_dean_FMT.id,
                    "sections": [
                        {
                            "name": "Section for Vice Dean of FMT",
                            "fields": [
                                {
                                    "name": "Field for Vice Dean of FMT"
                                }
                            ]
                        }
                    ]
                }]
            },
            {
                "name": "phase4",
                "group_role_id": head_of_DoICO.id,
                "phase_type": "transit",
                "phases_groups_roles": [{
                    "group_role_id": head_of_DoICO.id,
                    "sections": [
                        {
                            "name": "Section for Head of Department of ICO",
                            "fields": [
                                {
                                    "name": "Field for Head of Department of ICO"
                                }
                            ]
                        }
                    ]
                }]
            },
            {
                "name": "phase5",
                "group_role_id": dean_FMT.id,
                "phase_type": "end",
                "phases_groups_roles": [{
                    "group_role_id": dean_FMT.id,
                    "sections": [
                        {
                            "name": "Section for Dean of FMT",
                            "fields": [
                                {
                                    "name": "Field for Dean of FMT"
                                }
                            ]
                        }
                    ]
                }]
            },
        ],
        "transitions": [
            {
                "name": "transition 1",
                "from_phase": 1,
                "to_phase": 2
            },
            {
                "name": "transition 2",
                "from_phase": 1,
                "to_phase": 3
            },
            {
                "name": "transition 3",
                "from_phase": 2,
                "to_phase": 4
            },
            {
                "name": "transition 4",
                "from_phase": 3,
                "to_phase": 5
            },
            {
                "name": "transition 5",
                "from_phase": 4,
                "to_phase": 5
            }
        ]
    }
}
