import jwt
import os
from  datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from typing import Annotated
from jwt.exceptions import InvalidTokenError

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
  os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

pwd_context = CryptContext(
  schemes=["argon2"],
  deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
  payload = data.copy()

  expire = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
  )

  payload.update({
    "exp": expire
  })

  return jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
  )


def verify_token(token: str):
  return jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM]
  )

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
  )

  try:
    payload = verify_token(token)

    user_id = payload.get("sub")

    if user_id is None:
      raise credentials_exception
    
  except InvalidTokenError:
    raise credentials_exception
  
  user = db.query(User).filter(User.id == int(user_id)).first()

  if user is None:
    raise credentials_exception
  
  return user
