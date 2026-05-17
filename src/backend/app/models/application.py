from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Application(Base):
  __tablename__ = "applications"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
  role_title = Column(String, nullable=False)
  status = Column(String, nullable=False)
  job_link = Column(String, nullable=True)
  salary_range = Column(Integer, nullable=True)
  applied_date = Column(Date, nullable=False)
  follow_up_date = Column(Date, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  company = relationship("Company", back_populates="applications")
  user = relationship("User", back_populates="applications")
