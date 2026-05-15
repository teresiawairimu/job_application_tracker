from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UserResponse)
def get_user(current_user: User = Depends(get_current_user)):
  return current_user