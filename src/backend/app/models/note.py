from sqlalchemy import (Column, Integer, String, ForeignKey, DateTime)
from sqlalchemy.sql import func
from app.database import Base


class Note(Base):
  __tablename__ = "notes"
  id = Column(Integer, primary_key=True, index=True)
  application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
  content = Column(String, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())