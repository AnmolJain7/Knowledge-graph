from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    thread_id : Optional[str] = None
    message : str


class ChatResponse(BaseModel):
    thread_id : str
    response : str
