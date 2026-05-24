from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
  content: str


class NoteUpdate(BaseModel):
  content: Optional[str] = None


class NoteResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  application_id: int
  content: str
  created_at: datetime
  updated_at: datetime