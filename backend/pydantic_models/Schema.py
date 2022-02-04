from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date, datetime


class UserPostRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_name: str
    email: Optional[str]
    phone: Optional[int]
    public_key: Optional[str]
    birthdate: Optional[date]
    password: str

    class Config:
        orm_mode = True


class UserPatchRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[int]
    public_key: Optional[str]
    birthdate: Optional[date]
    password: Optional[str]

    class Config:
        orm_mode = True
        require_ownership = True


class UserDeleteRequest(BaseModel):
    class Config:
        require_ownership = True


class UserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    user_name: str
    email: Optional[str]
    phone: Optional[int]
    public_key: Optional[str]
    birthdate: Optional[date]
    disabled: Optional[bool]

    class Config:
        orm_mode = True


class GroupPostRequest(BaseModel):
    name: str
    address: Optional[str]
    phone: Optional[int]
    superior_group_id: Optional[int]
    creator_id: int

    class Config:
        orm_mode = True
        require_admin = True


class GroupPatchRequest(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[int]
    superior_group_id: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class GroupDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class GroupResponse(BaseModel):
    id: int
    name: str
    address: Optional[str]
    phone: Optional[int]
    creator_id: int
    superior_group_id: Optional[int]

    class Config:
        orm_mode = True


class RoleEnum(str, Enum):
    admin = "admin"
    group_admin = "group_admin"
    handler = "handler"
    applicant = "applicant"


class RolePostRequest(BaseModel):
    name: str
    role: RoleEnum
    creator_id: int

    class Config:
        orm_mode = True
        require_admin = True


class RolePatchRequest(BaseModel):
    name: Optional[str]
    role: Optional[RoleEnum]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class RoleDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class RoleResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    role: RoleEnum
    creator_id: int

    class Config:
        orm_mode = True


class PositionPostRequest(BaseModel):
    name: str
    group_id: Optional[int]
    role_id: int
    creator_id: int

    class Config:
        orm_mode = True
        require_admin = True


class PositionPatchRequest(BaseModel):
    name: Optional[str]
    group_id: Optional[int]
    role_id: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class PositionDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class PositionResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    group_id: Optional[int]
    role_id: int
    creator_id: int

    class Config:
        orm_mode = True


class UserPositionPostRequest(BaseModel):
    creator_id: int
    user_id: int
    position_id: int

    class Config:
        orm_mode = True
        require_admin = True


class UserPositionPatchRequest(BaseModel):
    user_id: Optional[int]
    position_id: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True


class UserPositionDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class UserPositionResponse(BaseModel):
    id: int
    created_at: datetime
    creator_id: int
    user_id: int
    position_id: int

    class Config:
        orm_mode = True


class FormPostRequest(BaseModel):
    name: str
    creator_id: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True


class FormPatchRequest(BaseModel):
    name: Optional[str]
    public: Optional[bool]
    obsolete: Optional[bool]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class FormDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class FormResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    creator_id: int
    public: bool
    obsolete: bool

    class Config:
        orm_mode = True


class PhaseTypeEnum(str, Enum):
    begin = "begin"
    transit = "transit"
    end = "end"


class PhasePostRequest(BaseModel):
    form_id: int
    name: str
    description: Optional[str]
    position_id: int
    phase_type: Optional['PhaseTypeEnum'] = 'transit'

    class Config:
        orm_mode = True
        require_admin = True


class PhasePatchRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    position_id: Optional[int]
    phase_type: Optional['PhaseTypeEnum']

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class PhaseDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class PhaseResponse(BaseModel):
    id: int
    created_at: datetime
    form_id: int
    name: str
    description: Optional[str]
    position_id: int
    phase_type: 'PhaseTypeEnum'
    # sections: Optional[List['Section']]

    class Config:
        orm_mode = True


class TransitionPostRequest(BaseModel):
    name: Optional[str]
    from_phase_id: int
    to_phase_id: int
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.name:
            self.name = f"{self.from_phase_id}to{self.to_phase_id}"


class TransitionPatchRequest(BaseModel):
    name: Optional[str]
    from_phase_id: Optional[int]
    to_phase_id: Optional[int]
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class TransitionDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class TransitionResponse(BaseModel):
    id: int
    created_at: datetime
    from_phase_id: int
    to_phase_id: int
    name: Optional[str]
    order: Optional[int]

    class Config:
        orm_mode = True


class SectionPostRequest(BaseModel):
    name: str
    phase_id: int
    position_id: int
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True


class SectionPatchRequest(BaseModel):
    name: Optional[str]
    phase_id: Optional[int]
    position_id: Optional[int]
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class SectionDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class SectionResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    phase_id: Optional[int]
    position_id: Optional[int]
    order: Optional[int]

    class Config:
        orm_mode = True


class FieldPostRequest(BaseModel):
    name: str
    section_id: int
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True


class FieldPatchRequest(BaseModel):
    name: Optional[str]
    order: Optional[int]

    class Config:
        orm_mode = True
        require_admin = True
        require_ownership = True


class FieldDeleteRequest(BaseModel):
    class Config:
        require_admin = True
        require_ownership = True


class FieldResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    section_id: int
    order: Optional[int]

    class Config:
        orm_mode = True


class InstanceCurrentStateEnum(str, Enum):
    initialized = "initialized"
    pending = "pending"
    partial_received = "partial received"
    full_received = "full received"
    partial_received_partial_resolved = "partial received & partial resolved"
    full_received_partial_resolved = "full received & partial resolved"
    full_resolved = "full resolved"
    done = "done"


class InstancePostRequest(BaseModel):
    form_id: int
    # current_phase_id: Optional[int]
    # creator_id: int

    class Config:
        orm_mode = True


class InstanceReceivers(BaseModel):
    section_id: int
    receiver_id: int


class InstanceTransit(BaseModel):
    current_phase_id: int
    # receivers: List['InstanceReceivers']
    receivers: Optional[Dict[int, int]]  # { section_id : user_id, }
    director_id: Optional[int]


class InstancePatchRequest(BaseModel):
    transit: Optional['InstanceTransit']
    handle: Optional[bool]  # Optional[List[int]]  # List of section id

    class Config:
        orm_mode = True
        # require_ownership = True


class InstanceDeleteRequest(BaseModel):
    class Config:
        require_ownership = True


class InstanceResponse(BaseModel):
    id: int
    created_at: datetime
    form_id: int
    current_phase_id: Optional[int]
    creator_id: int
    current_state: InstanceCurrentStateEnum

    class Config:
        orm_mode = True


class InstanceFieldPostRequest(BaseModel):
    instance_id: int
    field_id: int
    creator_id: int
    value: Optional[str]

    class Config:
        orm_mode = True
        require_position = True


class InstanceFieldPatchRequest(BaseModel):
    value: Optional[str]
    resolved: Optional[bool]

    class Config:
        orm_mode = True
        # require_position = True
        require_ownership = True


class InstanceFieldDeleteRequest(BaseModel):
    class Config:
        require_ownership = True


class InstanceFieldResponse(BaseModel):
    id: int
    created_at: datetime
    instance_id: int
    field_id: int
    creator_id: int
    value: Optional[str]
    resolved: bool

    class Config:
        orm_mode = True


class ReceiverPostRequest(BaseModel):
    instance_id: int
    section_id: int
    receiver_id: int

    class Config:
        orm_mode: True


class ReceiverPatchRequest(BaseModel):
    receiver_id: int

    class Config:
        orm_mode: True


class ReceiverDeleteRequest(BaseModel):
    pass


class ReceiverResponse(BaseModel):
    id: int
    created_at: datetime
    instance_id: int
    section_id: int
    user_id: int
    received: bool

    class Config:
        orm_mode = True


class DirectorResponse(BaseModel):
    id: int
    created_at: datetime
    instance_id: int
    phase_id: int
    user_id: int

    class Config:
        orm_mode = True


class CommitPostRequest(BaseModel):
    pass


class CommitPatchRequest(BaseModel):
    pass


class CommitDeleteRequest(BaseModel):
    pass


class CommitResponse(BaseModel):
    hash_commit: str
    prev_hash_commit: str = None
    hash_tree:  str
    creator_id:  int
    instance_id:  int
    created_at:  datetime
    current_phase_id:  int

    class Config:
        orm_mode = True
        require_ownership = True
        require_admin = True


class EnvelopeResponse(BaseModel):
    hash_envelope: str
    encrypted_content: str
    digital_signature: str
    field_id: str
    creator_id: int
    resolved: bool

    class Config:
        orm_mode = True


class HeadResponse(BaseModel):
    id: int
    name: str = None
    instance_id: int
    last_hash_commit: str

    class Config:
        orm_mode = True
