from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import ValidationError
from routes.dependencies.user import UserDependency
from routes.dependencies.db import get_session
from controller.InstanceController import InstanceController
from controller.CommitController import CommitController
from controller.FormController import FormController
from ORM.Model import Instance, Form, Phase, Section, Field, InstanceField, Envelope, TreeEnvelope, Tree, Commit, User, Receiver, Director, Position
from exceptions.ORMExceptions import ORMException
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased
from pydantic_models.Schema import InstanceResponse, FormResponse, PhaseResponse, SectionResponse, FieldResponse, InstanceFieldResponse, CommitResponse, EnvelopeResponse, PositionResponse, UserResponse

router = APIRouter()

@router.get("/forms/{form_id}/full_form")
def get_full_form(
    form_id: int = Path(..., description="The id of the form"),
    session = Depends(get_session),
    user_dependency: UserDependency = Depends(UserDependency),
):
    try:
        current_user = user_dependency.get_current_user()
        form_controller = FormController(session=session, current_user=current_user)
        form = form_controller.get_resource_instance(form_id)
        
        full_instance_1 = session.query(Form, Phase, Section, Field). \
        join(Form.phases). \
        join(Phase.sections). \
        join(Section.fields). \
        filter(Form.id == form_id). \
        order_by(Phase.order, Section.order, Field.order).all()

        form = FormResponse.from_orm(full_instance_1[0][0]).dict()
        phases = {
            'existed_phases': dict(),
            'phases': []
        }
        sections = {
            'phase_id_key': dict(),
            'section_id_key': dict()
        }
        for _, phase, section, field in full_instance_1:
            field = FieldResponse.from_orm(field).dict()
            if section.id not in sections['section_id_key']:
                section = SectionResponse.from_orm(section).dict()
                section['fields'] = [field]
                sections['section_id_key'][section['id']] = section
                if section['phase_id'] not in sections['phase_id_key']:
                    sections['phase_id_key'][section['phase_id']] = [section]
                else:
                    sections['phase_id_key'][section['phase_id']].append(section)
            else:
                sections['section_id_key'][section.id]['fields'].append(field)
            if phase.id not in phases['existed_phases']:
                phases['existed_phases'][phase.id] = phase.id
                phase = PhaseResponse.from_orm(phase).dict()
                phase['sections'] = sections['phase_id_key'][phase['id']]
                phases['phases'].append(phase)
    except (ORMException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    else:
        return {
            'form': form,
            'phases': phases['phases']
        }

@router.get("/forms/{form_id}/full_form_with_positions")
def get_full_form_with_positions(
    form_id: int = Path(..., description="The id of the form"),
    session = Depends(get_session),
    user_dependency: UserDependency = Depends(UserDependency),
):
    try:
        current_user = user_dependency.get_current_user()
        form_controller = FormController(session=session, current_user=current_user)
        form = form_controller.get_resource_instance(form_id)
        
        phases_positions = aliased(Position)
        sections_positions = aliased(Position)
        full_instance_1 = session.query(Form, Phase, phases_positions, Section, sections_positions, Field). \
        join(Form.phases). \
        join(phases_positions, phases_positions.id == Phase.position_id). \
        join(Phase.sections). \
        join(sections_positions, sections_positions.id == Section.position_id). \
        join(Section.fields). \
        filter(Form.id == form_id). \
        order_by(Phase.order, Section.order, Field.order).all()

        form = FormResponse.from_orm(full_instance_1[0][0]).dict()
        phases = {
            'existed_phases': dict(),
            'phases': []
        }
        sections = {
            'phase_id_key': dict(),
            'section_id_key': dict()
        }
        for _, phase, phase_position, section, section_position, field in full_instance_1:
            field = FieldResponse.from_orm(field).dict()
            if section.id not in sections['section_id_key']:
                section = SectionResponse.from_orm(section).dict()
                section_position = PositionResponse.from_orm(section_position).dict()
                section['fields'] = [field]
                section['position'] = section_position
                sections['section_id_key'][section['id']] = section
                if section['phase_id'] not in sections['phase_id_key']:
                    sections['phase_id_key'][section['phase_id']] = [section]
                else:
                    sections['phase_id_key'][section['phase_id']].append(section)
            else:
                sections['section_id_key'][section.id]['fields'].append(field)
            if phase.id not in phases['existed_phases']:
                phases['existed_phases'][phase.id] = phase.id
                phase = PhaseResponse.from_orm(phase).dict()
                phase_position = PositionResponse.from_orm(phase_position).dict()
                phase['sections'] = sections['phase_id_key'][phase['id']]
                phase['position'] = phase_position
                phases['phases'].append(phase)
    except (ORMException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    else:
        return {
            'form': form,
            'phases': phases['phases']
        }

@router.get("/instances/{instance_id}/full_instance")
def get_full_instance(
    instance_id: int = Path(..., description="The id of the instance"),
    session = Depends(get_session),
    user_dependency: UserDependency = Depends(UserDependency),
):
    try:
        current_user = user_dependency.get_current_user()
        instance_controller = InstanceController(session=session, current_user=current_user)
        instance = instance_controller.get_resource_instance(instance_id)
        
        full_instance_1 = session.query(Instance, Form, Phase, Section, Field, InstanceField). \
        join(Instance.form). \
        join(Form.phases). \
        join(Phase.sections). \
        join(Section.fields). \
        outerjoin(InstanceField, 
            or_(and_(InstanceField.field_id == Field.id, 
                InstanceField.instance_id == Instance.id), 
                InstanceField.id == None)). \
        filter(Instance.id == instance_id). \
        order_by(Phase.order, Section.order, Field.order).all()

        instance = InstanceResponse.from_orm(full_instance_1[0][0]).dict()
        form = FormResponse.from_orm(full_instance_1[0][1]).dict()
        phases = {
            'existed_phases': dict(),
            'phases': []
        }
        sections = {
            'phase_id_key': dict(),
            'section_id_key': dict()
        }
        for _, _, phase, section, field, instance_field in full_instance_1:
            instance_field = InstanceFieldResponse.from_orm(
                instance_field).dict() if instance_field else None
            field = FieldResponse.from_orm(field).dict()
            field['instance_field'] = instance_field
            if section.id not in sections['section_id_key']:
                section = SectionResponse.from_orm(section).dict()
                section['fields'] = [field]
                sections['section_id_key'][section['id']] = section
                if section['phase_id'] not in sections['phase_id_key']:
                    sections['phase_id_key'][section['phase_id']] = [section]
                else:
                    sections['phase_id_key'][section['phase_id']].append(section)
            else:
                sections['section_id_key'][section.id]['fields'].append(field)
            if phase.id not in phases['existed_phases']:
                phases['existed_phases'][phase.id] = phase.id
                phase = PhaseResponse.from_orm(phase).dict()
                phase['sections'] = sections['phase_id_key'][phase['id']]
                phases['phases'].append(phase)
    except (ORMException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    except:
        return {
            'instance': instance,
            'form': form,
            'phases': phases
        }

@router.get("/instances/{instance_id}/full_instance_with_positions_directors_receivers")
def get_full_instances_with_positions_directors_receivers(
    instance_id: int = Path(..., description="The id of the instance"),
    session = Depends(get_session),
    user_dependency: UserDependency = Depends(UserDependency),
):
    try:
        current_user = user_dependency.get_current_user()
        form_controller = FormController(session=session, current_user=current_user)
        form = form_controller.get_resource_instance(instance_id)

        phases_positions = aliased(Position)
        sections_positions = aliased(Position)
        directors_users = aliased(User)
        receivers_users = aliased(User)
        full_instance_1 = session.query(Instance, Form, Phase, phases_positions, directors_users, Section, sections_positions, receivers_users, Field, InstanceField). \
            join(Instance.form). \
            join(Form.phases). \
            join(phases_positions, phases_positions.id == Phase.position_id). \
            outerjoin(Director, or_(and_(Director.phase_id == Phase.id, Director.instance_id == Instance.id), Director.id == None)). \
            outerjoin(directors_users, or_(directors_users.id == Director.user_id, directors_users.id == None)). \
            join(Phase.sections). \
            join(sections_positions, sections_positions.id == Section.position_id). \
            outerjoin(Receiver, or_(and_(Receiver.section_id == Section.id, Receiver.instance_id == Instance.id), Receiver.id == None)). \
            outerjoin(receivers_users, or_(receivers_users.id == Receiver.user_id, receivers_users.id == None)). \
            join(Section.fields). \
            outerjoin(InstanceField, or_(and_(InstanceField.field_id == Field.id, InstanceField.instance_id == Instance.id), InstanceField.id == None)). \
            filter(Instance.id == 1). \
            order_by(Phase.order, Section.order, Field.order).all()

        instance = InstanceResponse.from_orm(full_instance_1[0][0]).dict()
        form = FormResponse.from_orm(full_instance_1[0][1]).dict()
        phases = {
            'existed_phases': dict(),
            'phases': []
        }
        sections = {
            'phase_id_key': dict(),
            'section_id_key': dict()
        }
        for _, _, phase, phase_position, director_user, section, section_position, receiver_user, field, instance_field in full_instance_1:
            instance_field = InstanceFieldResponse.from_orm(
                instance_field).dict() if instance_field else None
            field = FieldResponse.from_orm(field).dict()
            field['instance_field'] = instance_field
            if section.id not in sections['section_id_key']:
                section = SectionResponse.from_orm(section).dict()
                receiver_user = UserResponse.from_orm(receiver_user).dict() if receiver_user else None
                section_position = PositionResponse.from_orm(section_position).dict() if section_position else None
                section['fields'] = [field]
                section['receiver_user'] = receiver_user
                section['position'] = section_position
                sections['section_id_key'][section['id']] = section
                if section['phase_id'] not in sections['phase_id_key']:
                    sections['phase_id_key'][section['phase_id']] = [section]
                else:
                    sections['phase_id_key'][section['phase_id']].append(section)
            else:
                sections['section_id_key'][section.id]['fields'].append(field)

            if phase.id not in phases['existed_phases']:
                phases['existed_phases'][phase.id] = phase.id
                phase = PhaseResponse.from_orm(phase).dict()
                phase_position = PositionResponse.from_orm(phase_position).dict() if phase_position else None
                director_user = UserResponse.from_orm(director_user).dict() if director_user else None
                phase['sections'] = sections['phase_id_key'][phase['id']]
                phase['position'] = phase_position
                phase['director_user'] = director_user
                phases['phases'].append(phase)
    except (ORMException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    else:
        return {
            'instance': instance,
            'form': form,
            'phases': phases['phases']
        }

@router.get("/commits/{hash_commit}/full_instance")
def get_commits_full_instance(
    hash_commit: str = Path(..., description="The hash of commit"),
    session = Depends(get_session),
    user_dependency: UserDependency = Depends(UserDependency),
):
    try:
        current_user = user_dependency.get_current_user()
        commit_controller = CommitController(session=session, current_user=current_user)
        commit = commit_controller.get_resource_instance(hash_commit)

        query_envelopes = session.query(Envelope). \
            join(Commit.tree). \
            join(Tree.trees_envelopes). \
            join(TreeEnvelope.envelope). \
            filter(Commit.hash_commit == hash_commit).subquery()
        EnvelopeORM = aliased(Envelope, query_envelopes)
        full_instance_1 = session.query(Instance, Form, Phase, Section, Field, InstanceField, EnvelopeORM). \
            join(Commit.instance). \
            join(Instance.form). \
            join(Form.phases). \
            join(Phase.sections). \
            join(Section.fields). \
            outerjoin(InstanceField, 
                or_(and_(InstanceField.field_id == Field.id, InstanceField.instance_id == Instance.id), 
                InstanceField.id == None)). \
            outerjoin(query_envelopes, 
                or_(query_envelopes.c.instance_field_id == InstanceField.id, query_envelopes.c.hash_envelope == None)). \
            filter(Commit.hash_commit == hash_commit). \
            order_by(Phase.order, Section.order, Field.order).all()

        commit = CommitResponse.from_orm(commit)
        instance = InstanceResponse.from_orm(full_instance_1[0][0]).dict()
        form = FormResponse.from_orm(full_instance_1[0][1]).dict()
        phases = {
            'existed_phases': dict(),
            'phases': []
        }
        sections = {
            'phase_id_key': dict(),
            'section_id_key': dict()
        }
        for _, _, phase, section, field, instance_field, envelope in full_instance_1:
            envelope = EnvelopeResponse.from_orm(
                envelope).dict() if envelope else None
            instance_field = InstanceFieldResponse.from_orm(
                instance_field).dict() if instance_field else None
            field = FieldResponse.from_orm(field).dict()
            field['instance_field'] = instance_field
            field['envelope'] = envelope
            if section.id not in sections['section_id_key']:
                section = SectionResponse.from_orm(section).dict()
                section['fields'] = [field]
                sections['section_id_key'][section['id']] = section
                if section['phase_id'] not in sections['phase_id_key']:
                    sections['phase_id_key'][section['phase_id']] = [section]
                else:
                    sections['phase_id_key'][section['phase_id']].append(section)
            else:
                sections['section_id_key'][section.id]['fields'].append(field)
            if phase.id not in phases['existed_phases']:
                phases['existed_phases'][phase.id] = phase.id
                phase = PhaseResponse.from_orm(phase).dict()
                phase['sections'] = sections['phase_id_key'][phase['id']]
                phases['phases'].append(phase)
    except (ORMException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=e.message) 
    else:
        return {
            'commit': commit,
            'instance': instance,
            'form': form,
            'phases': phases['phases']
        }