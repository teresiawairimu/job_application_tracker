from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.email == user_data.email).first()

  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already registered"
    )
  
  new_user = User(
    email=user_data.email,
    hashed_password=hash_password(user_data.password)
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == credentials.email).first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password"
    )
  
  if not verify_password(credentials.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password"
    )
  
  token = create_access_token({"sub": str(user.id)})

  return {
    "access_token": token,
    "token_type": "bearer"
  }