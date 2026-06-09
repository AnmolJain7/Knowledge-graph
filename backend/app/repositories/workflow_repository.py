import json

from sqlalchemy.orm import Session

from app.models.workflow_state import WorkflowState

class WorkflowRepository:

    def get_state(self, db: Session, thread_id: str):
        
        return (
            db.query(WorkflowState)
            .filter(
                WorkflowState.thread_id == thread_id
            )
            .first()
        )
    
    def save_state(self, db: Session, thread_id: str, workflow_name: str, state: dict):

        existing = self.get_state(db, thread_id)

        if existing:
            existing.workflow_name = workflow_name
            existing.state_json = json.dumps(state)
            db.commit()
            db.refresh(existing)
            return existing

        record = WorkflowState(
            thread_id=thread_id,
            workflow_name=workflow_name,
            state_json=json.dumps(state)
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record
