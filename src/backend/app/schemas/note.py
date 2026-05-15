from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
  content: str


class NoteUpdate(BaseModel):
  content: Optional[str] = None


class NoteResponse(BaseModel):
  id: int
  application_id: int
  content: str
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True