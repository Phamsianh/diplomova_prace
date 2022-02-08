from ORM.session import session
from ORM.Model import User, Position

phamsianh = session.query(User).filter_by(user_name="phamsianh97").first()

student_of_CIT = session.query(Position).filter_by(name="Student of 2-CIT-C").first()
leading_teacher = session.query(Position).filter_by(name="Leading Teacher").first()
consultant = session.query(Position).filter_by(name="Consultant").first()
head_of_DoICO = session.query(Position).filter_by(name="Head of Department of \
Informatics and Cyber Operations").first()
vice_dean_FMT = session.query(Position).filter_by(name="Vice Dean of FMT").first()
dean_FMT = session.query(Position).filter_by(name="Dean of FMT (GrAdmin)").first()

# Example of instance
form1_structure = {
    "name": "NÁVRH TÉMATU ZÁVĚREČNÉ PRÁCE",
    "creator_id": phamsianh.id,
    "public": True,
    "obsolete": False,
    "workflow": {
        "phases": [
            {
                "name": "phase1",
                "position_id": student_of_CIT.id,
                "phase_type": "begin",
                "order": 1,
                "sections": [
                    {
                        "name": "Section for student of 2-CIT-C",
                        "position_id": student_of_CIT.id,
                        "order": 1,
                        "fields": [
                            {
                                "name": "Field for student of 2-CIT-C",
                                "order": 1,
                            }
                        ]
                    }
                ]
            },
            {
                "name": "phase2",
                "position_id": leading_teacher.id,
                "phase_type": "transit",
                "order": 2,
                "sections": [
                    {
                        "name": "Section for Leading Teacher",
                        "position_id": leading_teacher.id,
                        "order": 1,
                        "fields": [
                            {
                                "name": "First Field for Leading Teacher",
                                "order": 1,
                            },
                            {
                                "name": "Second Field for Leading Teacher",
                                "order": 2,
                            }
                        ]
                    },
                    {
                        "name": "Section for Consultant",
                        "position_id": consultant.id,
                        "order": 2,
                        "fields": [
                            {
                                "name": "Field for Consultant",
                                "order": 1,
                            }
                        ]
                    }
                ]
            },
            {
                "name": "phase3",
                "position_id": vice_dean_FMT.id,
                "phase_type": "transit",
                "order": 3,
                "sections": [
                    {
                        "name": "Section for Vice Dean of FMT",
                        "position_id": vice_dean_FMT.id,
                        "order": 1,
                        "fields": [
                            {
                                "name": "Field for Vice Dean of FMT",
                                "order": 1,
                            }
                        ]
                    }
                ]
            },
            {
                "name": "phase4",
                "position_id": head_of_DoICO.id,
                "phase_type": "transit",
                "order": 4,
                "sections": [
                    {
                        "name": "Section for Head of Department of ICO",
                        "position_id": head_of_DoICO.id,
                        "order": 1,
                        "fields": [
                            {
                                "name": "Field for Head of Department of ICO",
                                "order": 1,
                            }
                        ]
                    }
                ]
            },
            {
                "name": "phase5",
                "position_id": dean_FMT.id,
                "phase_type": "end",
                "order": 5,
                "sections": [
                    {
                        "name": "Section for Dean of FMT",
                        "position_id": dean_FMT.id,
                        "order": 1,
                        "fields": [
                            {
                                "name": "Field for Dean of FMT",
                                "order": 1,
                            }
                        ]
                    }
                ]
            },
        ],
        "transitions": [
            {
                "name": "transition 1 to 2",
                "from_phase": 1,
                "to_phase": 2
            },
            {
                "name": "transition 2 to 1",
                "from_phase": 2,
                "to_phase": 1
            },
            {
                "name": "transition 1 to 3",
                "from_phase": 1,
                "to_phase": 3
            },
            {
                "name": "transition 3 to 1",
                "from_phase": 3,
                "to_phase": 1
            },
            {
                "name": "transition 2 to 4",
                "from_phase": 2,
                "to_phase": 4
            },
            {
                "name": "transition 4 to 2",
                "from_phase": 4,
                "to_phase": 2
            },
            {
                "name": "transition 3 to 5",
                "from_phase": 3,
                "to_phase": 5
            },
            {
                "name": "transition 5 to 3",
                "from_phase": 5,
                "to_phase": 3
            },
            {
                "name": "transition 4 to 5",
                "from_phase": 4,
                "to_phase": 5
            },
            {
                "name": "transition 5 to 4",
                "from_phase": 5,
                "to_phase": 4
            },
        ]
    }
}
