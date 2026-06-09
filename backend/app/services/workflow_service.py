import json

from app.repositories.workflow_repository import WorkflowRepository

repo = WorkflowRepository()

class WorkflowService:

    def get_state(self, db, thread_id):
        state = repo.get_state(db, thread_id)

        if not state:
            return None
        
        return json.loads(state.state_json)
    
    def save_state(self, db, thread_id, workflow_name, state):
        return repo.save_state(db, thread_id, workflow_name, state)
    

workflow_service = WorkflowService()