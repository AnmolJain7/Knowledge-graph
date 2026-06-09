from fastapi import FastAPI

from app.core.database import base
from app.core.database import engine

from app.api.v1.user_routes import router as user_router
from app.api.v1.chat_routes import router as chat_router

from app.models.user import User
from app.models.workflow_state import WorkflowState

base.metadata.create_all(bind=engine)

app = FastAPI(title = "Knoweldge Graph Demo")

app.include_router(user_router)
app.include_router(chat_router)

@app.get("/")
def health():
    return {
        "message":"Application Running"
    }



