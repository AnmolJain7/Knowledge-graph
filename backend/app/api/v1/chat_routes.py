import uuid

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.chat_service import chat_service
from app.services.workflow_service import workflow_service
from app.langgraph.graphs.create_user_graph import create_user_graph
from app.schemas.user import (
    UserCreate,
    UserUpdate
)
from app.services.user_service import service as user_service
from app.services.intent_service import intent_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):

    thread_id = payload.thread_id or str(uuid.uuid4())
    state = workflow_service.get_state(db, thread_id)

    if not state:
        state = {
            "thread_id" : thread_id,
            "intent" : None,
            "workflow_name": None,
            "current_step" : None,
            "last_user_message" : None,
            "name" : None,
            "age" : None,
            "gender" : None,
            "address" : None,
            "phone_number" : None,
            "user_id" : None,
            "last_operation": None,
            "response" : None,
            "is_completed" : False
        }

    if state.get("current_step"):
        state = chat_service.update_state_from_message(state, payload.message)

    if not state.get("intent") or state.get("is_completed"):
        state["intent"] = intent_service.detect_intent(payload.message)
        state["is_completed"] = False

    result = handle_intent(state, payload.message, db)

    workflow_name = result.get("workflow_name") or result.get("intent") or "unknown"
    workflow_service.save_state(db, thread_id, workflow_name, result)

    return{
        "thread_id" : thread_id,
        "response" : result["response"]
    }


def handle_intent(state: dict, message: str, db: Session) -> dict:
    intent = state.get("intent")

    if intent == "create_user":
        return handle_create_user(state, db)

    if intent == "list_users":
        users = user_service.get_all_users(db)
        state["workflow_name"] = "list_users"
        state["current_step"] = None
        state["is_completed"] = True
        state["last_operation"] = {
            "intent": "list_users",
            "user_count": len(users)
        }
        state["response"] = (
            "No users found."
            if not users
            else "Users: " + ", ".join(
                f"{user.id}-{user.name}-{user.phone_number}" for user in users
            )
        )
        return state

    if intent == "get_user":
        return handle_get_user(state, message, db)

    if intent == "delete_user":
        return handle_delete_user(state, message, db)

    if intent == "update_user":
        return handle_update_user(state, message, db)

    state["current_step"] = None
    state["is_completed"] = True
    state["workflow_name"] = "unknown"
    state["last_operation"] = {
        "intent": "unknown",
        "message": message
    }
    state["response"] = (
        "I can help with create, get, list, update, or delete user requests. "
        "Please tell me what you want to do."
    )
    return state


def handle_create_user(state: dict, db: Session) -> dict:
    if has_validation_error(state):
        return state

    result = create_user_graph.invoke(state)

    if not result["is_completed"]:
        return result

    duplicate = user_service.get_user_by_phone(db, result["phone_number"])
    if duplicate:
        result["response"] = "User already exists with this phone number."
        result["is_completed"] = True
        return reset_non_intent_state(
            result,
            workflow_name="create_user",
            last_operation={
                "intent": "create_user",
                "status": "duplicate_phone",
                "phone_number": result["phone_number"]
            }
        )

    user_payload = UserCreate(
        name=result["name"],
        age=result["age"],
        gender=result["gender"],
        address=result["address"],
        phone_number=result["phone_number"]
    )
    created_user = user_service.create_user(db, user_payload)

    result["response"] = f"User created successfully with id {created_user.id}."
    result["is_completed"] = True
    return reset_non_intent_state(
        result,
        workflow_name="create_user",
        last_operation={
            "intent": "create_user",
            "status": "created",
            "user_id": created_user.id,
            "phone_number": created_user.phone_number
        }
    )


def handle_get_user(state: dict, message: str, db: Session) -> dict:
    if has_validation_error(state):
        return state

    user_id = state.get("user_id") or intent_service.extract_user_id(message)
    if not user_id:
        state["current_step"] = "collect_user_id"
        state["response"] = "Please share the user id."
        return state

    user = user_service.get_user(db, user_id)
    state["user_id"] = user_id
    state["current_step"] = None
    state["is_completed"] = True
    state["workflow_name"] = "get_user"
    state["last_operation"] = {
        "intent": "get_user",
        "user_id": user_id,
        "status": "found" if user else "not_found"
    }
    state["response"] = (
        "User not found."
        if not user
        else f"User {user.id}: {user.name}, age {user.age}, gender {user.gender}, address {user.address}, phone {user.phone_number}."
    )
    return reset_non_intent_state(state, workflow_name="get_user", last_operation=state["last_operation"])


def handle_delete_user(state: dict, message: str, db: Session) -> dict:
    if has_validation_error(state):
        return state

    user_id = state.get("user_id") or intent_service.extract_user_id(message)
    if not user_id:
        state["current_step"] = "collect_user_id"
        state["response"] = "Please share the user id you want to delete."
        return state

    deleted = user_service.delete_user(db, user_id)
    state["user_id"] = user_id
    state["current_step"] = None
    state["is_completed"] = True
    state["workflow_name"] = "delete_user"
    state["last_operation"] = {
        "intent": "delete_user",
        "user_id": user_id,
        "status": "deleted" if deleted else "not_found"
    }
    state["response"] = "User deleted successfully." if deleted else "User not found."
    return reset_non_intent_state(state, workflow_name="delete_user", last_operation=state["last_operation"])


def handle_update_user(state: dict, message: str, db: Session) -> dict:
    if has_validation_error(state):
        return state

    user_id = state.get("user_id") or intent_service.extract_user_id(message)
    updates = intent_service.extract_update_fields(message)

    if not user_id:
        state["current_step"] = "collect_user_id"
        state["response"] = "Please share the user id you want to update."
        return state

    if not updates:
        state["current_step"] = None
        state["is_completed"] = True
        state["response"] = (
            "Please mention at least one field to update, for example: "
            "update user 4 age to 30."
        )
        return reset_non_intent_state(state)

    payload = UserUpdate(**updates)
    updated = user_service.update_user(db, user_id, payload)
    state["user_id"] = user_id
    state["current_step"] = None
    state["is_completed"] = True
    state["workflow_name"] = "update_user"
    state["last_operation"] = {
        "intent": "update_user",
        "user_id": user_id,
        "updates": updates,
        "status": "updated" if updated else "not_found"
    }
    state["response"] = "User updated successfully." if updated else "User not found."
    return reset_non_intent_state(state, workflow_name="update_user", last_operation=state["last_operation"])


def reset_non_intent_state(state: dict, workflow_name: str | None = None, last_operation: dict | None = None) -> dict:
    state["current_step"] = None
    state["last_user_message"] = None
    state["user_id"] = None
    state["workflow_name"] = workflow_name or state.get("workflow_name") or state.get("intent")
    state["intent"] = workflow_name or state.get("intent")
    state["last_operation"] = last_operation
    return state


def has_validation_error(state: dict) -> bool:
    response = state.get("response") or ""
    if not state.get("current_step"):
        return False
    return any(
        marker in response
        for marker in ("should be", "re-enter")
    )
