from app.langgraph.state import UserWorkflowState


def collect_name_node(state: UserWorkflowState):
    return {
        **state,
        "current_step": "collect_name",
        "response": "Please tell me your name."
    }

def collect_age_node(state: UserWorkflowState):
    return {
        **state,
        "current_step": "collect_age",
        "response": "Please tell me your age."
    }

def collect_gender_node(state: UserWorkflowState):
    return {
        **state,
        "current_step": "collect_gender",
        "response": "Please tell me your gender."
    }


def collect_address_node(state: UserWorkflowState):
    return {
        **state,
        "current_step": "collect_address",
        "response": "Please tell me your address."
    }


def collect_phone_node(state: UserWorkflowState):
    return {
        **state,
        "current_step": "collect_phone",
        "response": "Please tell me your phone number."
    }

def create_user_node(state: UserWorkflowState):
    return {
        **state,
        "is_completed": True,
        "current_step": None,
        "response": "I have all the details needed to create the user."
    }


def route_missing_field(state: UserWorkflowState):

    if not state.get("name"):
        return "collect_name"

    if not state.get("age"):
        return "collect_age"

    if not state.get("gender"):
        return "collect_gender"

    if not state.get("address"):
        return "collect_address"

    if not state.get("phone_number"):
        return "collect_phone"

    return "create_user"
