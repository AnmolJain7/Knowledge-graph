from langgraph.graph import StateGraph
from langgraph.graph import END

from app.langgraph.state import UserWorkflowState

from app.langgraph.nodes.create_user_nodes import (
    route_missing_field,
    collect_name_node,
    collect_age_node,
    collect_gender_node,
    collect_address_node,
    collect_phone_node,
    create_user_node
)


builder = StateGraph(UserWorkflowState)

builder.add_node(
    "collect_name",
    collect_name_node
)

builder.add_node(
    "collect_age",
    collect_age_node
)

builder.add_node(
    "collect_gender",
    collect_gender_node
)

builder.add_node(
    "collect_address",
    collect_address_node
)

builder.add_node(
    "collect_phone",
    collect_phone_node
)

builder.add_node(
    "create_user",
    create_user_node
)

builder.set_conditional_entry_point(route_missing_field)


builder.add_edge(
    "collect_name",
    END
)

builder.add_edge(
    "collect_age",
    END
)

builder.add_edge(
    "collect_gender",
    END
)

builder.add_edge(
    "collect_address",
    END
)

builder.add_edge(
    "collect_phone",
    END
)

builder.add_edge(
    "create_user",
    END
)

create_user_graph = builder.compile()