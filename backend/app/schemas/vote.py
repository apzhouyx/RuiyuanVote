from pydantic import BaseModel

class VoteCreate(BaseModel):
    unit_id: int

class VoteResponse(BaseModel):
    success: bool
    message: str 