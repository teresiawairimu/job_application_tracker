from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
  name: str
  website: Optional[str] = None


class CompanyUpdate(BaseModel):
  name: Optional[str] = None
  website: Optional[str] = None


class CompanyResponse(BaseModel):
  id: int
  name: str
  website: Optional[str]
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True