# check if user is a potential receiver of a section
# required inputs are user id, section id
check_user_potential_receiver = session.query(True). \
    join(Section.position). \
    join(Position.users_positions). \
    filter(Section.id == 1, UserPosition.user_id == 1).first()
session.close()
print(check_user_potential_receiver)