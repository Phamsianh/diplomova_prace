from datetime import date, datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

# The schema for POST, PATCH request is used for validating the input of user in request body,
# for checking the role and/or the ownership of the user on inserting and updating the resource instance.
# The schema for DELETE request is used only for checking the role and/or ownership of a user on deleting the resource instance
# The schema for response is used for filtering the data from database before the response is sent to the user.


class UserRegistration(BaseModel):
    """The request body for creating a new user is as follow"""
    first_name: str = Field(
        ...,
        max_length=100,
        regex=r"^[a-zA-Z\s]{1,100}$",
        description="First name of the user"
    )
    last_name: str = Field(
        ...,
        max_length=100,
        regex=r"^[a-zA-Z\s]{1,100}$",
        description="Last name of the user"
    )
    user_name: str = Field(
        ...,
        max_length=100,
        regex=r"^[a-zA-Z0-9\-_!@#$%^&*()?{}]{1,100}$",
        description="Username used to login to the system. "
                    "Must contain only uppercase or lowercase letter, space, number "
                    "and special character -_!@#$%^&*()?{}"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="password used to authenticate user"
                    "password must contain at least 8 characters, at least 1 uppercase letter, 1 lower letter, "
                    "1 number and can contain special character",
        # regular expression for password from https://regexr.com/3bfsi
        regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,100}$"
    )
    email: str = Field(
        ...,
        description="Email of the user. Must follow email naming schema",
        # regular expression for email from https://regexr.com/2rhq7
        regex=r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )
    phone: Optional[int] = Field(
        None,
        description="Phone number of the user"
    )
    birthdate: Optional[date] = Field(
        None,
        description="Birthdate of the user. Giving in format YYYY-mm-dd"
    )


class UserPostRequest(UserRegistration):
    class Config:
        orm_mode = True


class UserPatchRequest(BaseModel):
    """Request body for updating user is as follow"""

    first_name: Optional[str] = Field(
        None,
        max_length=100,
        regex=r"^[a-zA-Z\s]{1,100}$",
        description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None,
        max_length=100,
        regex=r"^[a-zA-Z\s]{1,100}$",
        description="Last name of the user"
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="password used to authenticate user. "
                    "password must contain at least 8 characters, at least 1 uppercase letter, 1 lower letter, "
                    "1 number and can contain special character",
        # regular expression for password from https://regexr.com/3bfsi
        regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,100}$"
    )
    email: Optional[str] = Field(
        None,
        description="Email of the user. Must follow email naming schema",
        # regular expression for email from https://regexr.com/2rhq7
        regex=r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )
    phone: Optional[int] = Field(
        None,
        description="Phone number of the user"
    )
    birthdate: Optional[date] = Field(
        None,
        description="Birthdate of the user. Giving in format YYYY-mm-dd"
    )

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
    """The request body schema for creating a group is follow:"""
    name: str = Field(
        ...,
        max_length=100,
        description="The name of the group."
    )
    address: Optional[str] = Field(
        None,
        max_length=100,
        description="The address of the group"
    )
    phone: Optional[str] = Field(
        None,
        regex="^[0-9]{8,20}$",
        description="The phone number of the group"
    )
    superior_group_id: Optional[int] = Field(
        None,
        description="The group id of the superior group"
    )

    class Config:
        orm_mode = True
        require_admin = True


class GroupPatchRequest(BaseModel):
    """The request body schema for updating the group is follow:"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the group."
    )
    address: Optional[str] = Field(
        None,
        max_length=100,
        description="The address of the group"
    )
    phone: Optional[int] = Field(
        None,
        description="The phone number of the group"
    )
    superior_group_id: Optional[int] = Field(
        None,
        description="The group id of the superior group"
    )

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
    """The request body for creating a role is follow:"""
    name: str = Field(
        ...,
        max_length=100,
        description="The name of the role"
    )
    role: RoleEnum = Field(
        ...,
        description="The role in the system. Enumeration of 'admin', 'handler', 'applicant'"
    )

    class Config:
        orm_mode = True
        require_admin = True


class RolePatchRequest(BaseModel):
    """The request body for updating the role is follow:"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the role"
    )
    role: Optional[RoleEnum] = Field(
        None,
        description="The role in the system. Enumeration of 'admin', 'handler', 'applicant'"
    )

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
    """The request schema for creating a position"""
    name: str = Field(
        ...,
        max_length=100,
        description="The name of position."
    )
    group_id: Optional[int] = Field(
        None,
        description="The id of group, which will have this position."
    )
    role_id: int = Field(
        ...,
        description="The id of the role, from which this position is derived from."
    )

    class Config:
        orm_mode = True
        require_admin = True


class PositionPatchRequest(BaseModel):
    """The request schema for updating the position"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of position."
    )
    group_id: Optional[int] = Field(
        None,
        description="The id of group, which will have this position."
    )
    role_id: Optional[int] = Field(
        None,
        description="The id of the role, from which this position is derived from."
    )

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
    """The request body schema for creating a user position is follow:"""
    user_id: int = Field(
        ...,
        description="The id of user, who is assigned for the position."
    )
    position_id: int = Field(
        ...,
        description="The id of position, which is assigned the user."
    )

    class Config:
        orm_mode = True
        require_admin = True


class UserPositionPatchRequest(BaseModel):
    """The request body schema for updating the user position is follow:"""
    user_id: Optional[int] = Field(
        ...,
        description="The id of user, who is assigned for the position."
    )
    position_id: Optional[int] = Field(
        ...,
        description="The id of position, which is assigned the user."
    )

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
    name: str = Field(
        ...,
        max_length=100,
        description="The name of the form."
    )

    class Config:
        orm_mode = True
        require_admin = True


class FormPatchRequest(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the form."
    )
    public: Optional[bool] = Field(
        None,
        description="The public state of the form. "
                    "Set to ``true`` to public the form. "
                    "Only public form can be instantiated. "
                    "Private form cannot be searched. "
                    "Public form cannot be update or delete."
    )
    obsolete: Optional[bool] = Field(
        None,
        description="The obsolete state of the form. Set to ``true`` to deprecate the form. "
                    "Only public form can be deprecated. "
                    "Obsolete form can be searched. "
                    "Obsolete form cannot be instantiated. "
                    "Obsolete form cannot be updated or deleted."
    )

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
    # phases: List
    # sections: List
    # fields: List
    # positions: List

    class Config:
        orm_mode = True


class PhaseTypeEnum(str, Enum):
    begin = "begin"
    transit = "transit"
    end = "end"


class PhasePostRequest(BaseModel):
    """The request body for creating a phase is follow:"""
    form_id: int = Field(
        ...,
        description="The id of the form, which contains this phase."
    )
    name: str = Field(
        ...,
        max_length=100,
        description="The name of the phase."
    )
    position_id: int = Field(
        ...,
        description="The position id, which is designated for this phase."
    )
    phase_type: Optional['PhaseTypeEnum'] = Field(
        'transit',
        description="The type of the phase. Enumeration of 'begin', 'transit', 'end'. Default value is 'transit'"
    )
    order: Optional[int] = Field(
        1,
        description="The order number, which is used to arranged the order of the phase and its section in the form its instances."
    )
    description: Optional[str] = Field(
        None,
        description="The phase description, which is used to give the user more information about the phase."
    )

    class Config:
        orm_mode = True
        require_admin = True


class PhasePatchRequest(BaseModel):
    """The request body for updating the phase is follow"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the phase."
    )
    position_id: Optional[int] = Field(
        None,
        description="The position id, which is designated for this phase."
    )
    phase_type: Optional['PhaseTypeEnum'] = Field(
        None,
        description="The type of the phase. Enumeration of 'begin', 'transit', 'end'. Default value is 'transit'"
    )
    order: Optional[int] = Field(
        None,
        description="The order number, which is used to arranged the order of the phase and its section in the form its instances."
    )
    description: Optional[str] = Field(
        None,
        description="The phase description, which is used to give the user more information about the phase."
    )

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
    order: int

    class Config:
        orm_mode = True


class TransitionPostRequest(BaseModel):
    """The request body schema for creating a transition is follow:"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the transition. Default value is in format '<from_phase_id>to<to_phase_id>.'"
    )
    from_phase_id: int = Field(
        ...,
        description="The id of the phase, which is the source."
    )
    to_phase_id: int = Field(
        ...,
        description="The id of the phase, which is the target."
    )
    order: Optional[int] = Field(
        1,
        description="The order of the transition, which is used to arranged the appearance of transition in the form."
    )

    class Config:
        orm_mode = True
        require_admin = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.name:
            self.name = f"{self.from_phase_id}_to_{self.to_phase_id}"


class TransitionPatchRequest(BaseModel):
    """The request body schema for updating the transition is follow:"""
    name: Optional[str] = Field(
        None,
        max_length=100,
        description="The name of the transition. Default value is in format '<from_phase_id>to<to_phase_id>.'"
    )
    from_phase_id: Optional[int] = Field(
        None,
        description="The id of the phase, which is the source."
    )
    to_phase_id: Optional[int] = Field(
        None,
        description="The id of the phase, which is the target."
    )
    order: Optional[int] = Field(
        None,
        description="The order of the transition, which is used to arranged the appearance of transition in the form."
    )

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
    """The request body for creating a section is as follow"""
    name: str = Field(
        ...,
        max_length=100,
        description="The name of the section"
    )
    phase_id: int = Field(
        ...,
        description="The id of the phase, which contains this section"
    )
    position_id: int = Field(
        ...,
        description="The id of position assigned for handling this section"
    )
    order: Optional[int] = Field(
        1,
        description="The order of the section in the form or instance."
    )

    class Config:
        orm_mode = True
        require_admin = True


class SectionPatchRequest(BaseModel):
    """The request body for updating the section is follow"""
    name: Optional[str] = Field(
        None,
        description="The name of the section."
    )
    phase_id: Optional[int] = Field(
        None,
        description="The id of the phase, which contains the section."
                    "The new phase must be in the same form of the old phase."
    )
    position_id: Optional[int] = Field(
        None,
        description="The id of position assigned for handling this section."
    )
    order: Optional[int] = Field(
        None,
        description="The order of the section, "
                    "which is used to arrange the order of the section in the form or instance."
    )

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
    """The request body for creating field is follow:"""
    name: str = Field(
        ...,
        description="The name of the field."
    )
    section_id: int = Field(
        ...,
        description="The id of the section containing the field."
    )
    order: Optional[int] = Field(
        1,
        description="The order of the field in the section."
    )

    class Config:
        orm_mode = True
        require_admin = True


class FieldPatchRequest(BaseModel):
    """The request body for updating field is follow:"""
    name: Optional[str] = Field(
        None,
        description="The name of the field"
    )
    section_id: Optional[int] = Field(
        None,
        description="The id of the section containing the field."
    )
    order: Optional[int] = Field(
        None,
        description="The order of the field in the section."
    )

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
    """The request body for creating an instance is follow"""
    form_id: int = Field(
        ...,
        description="The id of the form, from which the instance is instantiated."
    )

    class Config:
        orm_mode = True


class InstanceReceivers(BaseModel):
    section_id: int
    receiver_id: int


class InstanceTransit(BaseModel):
    """InstanceTransit object schema:"""
    current_phase_id: int = Field(
        ...,
        description="The id of next phase."
    )
    receivers: Dict[int, int] = Field(
        None,
        description="An object, which contains key as the id of section of next phase, "
                    "value as the id of user, who is the handler(reciever) of section for the next phase. "
                    "For example: {'1': 2} mean specified the section with id 1 will be handled by the user with id 2."
    )
    director_id: int = Field(
        None,
        description="Id of the user, who will be director of the next phase."
    )
    message: Optional[str] = Field(
        '',
        description="The message for the commit in commit history."
    )


class InstancePatchRequest(BaseModel):
    """Request body for updating the instance must follow schema:"""
    transit: Optional['InstanceTransit'] = Field(
        None,
        description="Object for specified information when transit an instance. Please refer to InstanceTransit schema"
    )
    handle: Optional[bool] = Field(
        None,
        description="Set this field to true if authenticated user is the handler(receiver) of the next phase"
    )
    done: Optional[bool] = Field(
        None,
        description="The state of the instance when it is complete handle and reach the end phase. "
                    "Mark this field to true to change the state of the instance to done."
                    "The instance at state 'done' cannot be modified."
    )
    class Config:
        orm_mode = True
        # require_ownership = True


class InstanceDeleteRequest(BaseModel):
    class Config:
        require_ownership = True


class InstanceResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    form_id: int
    current_phase_id: Optional[int]
    creator_id: int
    # current_state: InstanceCurrentStateEnum
    done: bool

    class Config:
        orm_mode = True


class InstanceFieldPostRequest(BaseModel):
    class Config:
        orm_mode = True
        require_position = True


class InstanceFieldPatchRequest(BaseModel):
    """The request body for updating the content (instance field) must follow schema:"""
    value: Optional[str] = Field(
        None,
        description="The value of the content."
    )
    resolved: Optional[bool] = Field(
        None,
        description="The resolved state of the instance field, used for evaluate the ``current_state`` of instance"
    )

    class Config:
        orm_mode = True
        # Don't require ownership, because the director can change the receiver of the content.
        # Then this content can be updated by different handler.
        # The user must be the receiver of this content. Refer the InstanceFieldController.path_resource_instance() method.
        # require_ownership = True


class InstanceFieldDeleteRequest(BaseModel):
    class Config:
        require_ownership = True


class InstanceFieldResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    instance_id: int
    field_id: int
    creator_id: int
    value: Optional[str]
    resolved: bool

    class Config:
        orm_mode = True
        required_ownership = True


class ReceiverPostRequest(BaseModel):
    """The request body for creating a receiver is as follow:"""
    instance_id: int = Field(
        ...,
        description="Id of the instance"
    )
    section_id: int = Field(
        ...,
        description="Id of the section."
    )
    user_id: int = Field(
        ...,
        description="Id of the user, who will become a receiver for the section of the instance."
    )

    class Config:
        orm_mode: True


class ReceiverPatchRequest(BaseModel):
    """The request body for updating the receiver is as follow:"""
    user_id: int = Field(
        ...,
        description="Id of the user, who will become the receiver for the section of the instance."
    )

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
    message: str

    class Config:
        orm_mode = True
        require_ownership = True
        require_admin = True


class EnvelopeResponse(BaseModel):
    hash_envelope: str
    instance_field_id: str
    creator_id: int
    content_value: str
    updated_at: datetime

    class Config:
        orm_mode = True


class HeadResponse(BaseModel):
    id: int
    name: str = None
    instance_id: int
    last_hash_commit: str

    class Config:
        orm_mode = True
