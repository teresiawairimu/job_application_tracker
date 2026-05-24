from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
  name: str
  website: Optional[str] = None


class CompanyUpdate(BaseModel):
  name: Optional[str] = None
  website: Optional[str] = None


class CompanyResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  name: str
  website: Optional[str]
  created_at: datetime
  updated_at: datetime