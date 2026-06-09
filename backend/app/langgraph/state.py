from typing import Optional
from typing_extensions import TypedDict


class UserWorkflowState(TypedDict):
    thread_id: str
    intent: str
    workflow_name: Optional[str]
    current_step: Optional[str]
    last_user_message: Optional[str]
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    user_id: Optional[int]
    last_operation: Optional[dict]
    response: Optional[str]
    is_completed : Optional[bool]
