from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from app.core.database import base

class WorkflowState(base):
    __tablename__ = "workflow_states"

    id = Column(Integer,primary_key=True,index=True)
    thread_id = Column(String(100), unique=True,nullable=False)
    workflow_name = Column(String(100),nullable=False)
    state_json = Column(Text,nullable=False)



