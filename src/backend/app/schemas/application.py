from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime
from typing import Optional

class ApplicationStatus(str, Enum):
  APPLIED = "applied"
  SCREENING = "screening"
  INTERVIEW = "interview"
  OFFER = "offer"
  REJECTED = "rejected"

  
class ApplicationCreate(BaseModel):
  company_id: int
  role_title: str
  status: ApplicationStatus
  job_link: Optional[str] = None
  salary_range: Optional[int] = None
  applied_date: date
  follow_up_date: Optional[date] = None


class ApplicationUpdate(BaseModel):
  company_id: Optional[int] = None
  role_title: Optional[str] = None
  status: Optional[ApplicationStatus] = None
  job_link: Optional[str] = None
  salary_range: Optional[int] = None
  applied_date: Optional[date] = None
  follow_up_date: Optional[date] = None

class ApplicationResponse(BaseModel):
  id: int
  user_id: int
  company_id: int
  role_title: str
  status: ApplicationStatus
  job_link: Optional[str]
  salary_range: Optional[int]
  applied_date: date
  follow_up_date: Optional[date]
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True

