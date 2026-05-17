from pydantic import BaseModel, field_validator
from enum import Enum
from datetime import date, datetime
from typing import Optional
from app.schemas.company import CompanyResponse

class ApplicationStatus(str, Enum):
  APPLIED = "applied"
  SCREENING = "screening"
  INTERVIEW = "interview"
  OFFER = "offer"
  REJECTED = "rejected"

  
class ApplicationCreate(BaseModel):
  company_name: str
  role_title: str
  status: ApplicationStatus
  job_link: Optional[str] = None
  salary_range: Optional[int] = None
  applied_date: date
  follow_up_date: Optional[date] = None

  @field_validator("applied_date")
  @classmethod
  def applied_date_cannot_be_future(cls, value):
    if value is not None and value > date.today():
      raise ValueError("Applied date cannot be in the future")
    return value
  
  @field_validator("follow_up_date")
  @classmethod
  def follow_up_date_cannot_be_past(cls, value):
    if value is not None and value < date.today():
      raise ValueError("Follow-up date cannot be in the past")
    return value


class ApplicationUpdate(BaseModel):
  company_name: Optional[str] = None
  role_title: Optional[str] = None
  status: Optional[ApplicationStatus] = None
  job_link: Optional[str] = None
  salary_range: Optional[int] = None
  applied_date: date
  follow_up_date: Optional[date] = None

  @field_validator("applied_date")
  @classmethod
  def applied_date_cannot_be_future(cls, value):
    if value is not None and value > date.today():
      raise ValueError("Applied date cannot be in the future")
    return value
  
  @field_validator("follow_up_date")
  @classmethod
  def follow_up_date_cannot_be_past(cls, value):
    if value is not None and value < date.today():
      raise ValueError("Follow-up date cannot be in the past")
    return value

class ApplicationResponse(BaseModel):
  id: int
  user_id: int
  company_id: int
  company: CompanyResponse
  role_title: str
  status: ApplicationStatus
  job_link: Optional[str] = None
  salary_range: Optional[int] = None
  applied_date: date
  follow_up_date: Optional[date] = None
  created_at: datetime
  updated_at: Optional[datetime] = None

  class Config:
    from_attributes = True

