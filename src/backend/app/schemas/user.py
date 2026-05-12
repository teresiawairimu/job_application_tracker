from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
  name: str
  email: EmailStr
  password: str


