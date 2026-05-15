from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user, get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  db_application = Application(**application.model_dump(), user_id=current_user.id)
  db.add(db_application)
  db.commit()
  db.refresh(db_application)
  return db_application


@router.get("/", response_model=list[ApplicationResponse])
def get_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  return db.query(Application).filter(Application.user_id == current_user.id).all()


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  application = db.query(Application).filter(Application.id == application_id, Application.user_id == current_user.id).first()

  if not application:
    raise HTTPException(status_code=404, detail="Application not found")

  return application


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application_data: ApplicationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  application = db.query(Application).filter(Application.id == application_id, Application.user_id == current_user.id).first()

  if not application:
    raise HTTPException(status_code=404, detail="Application not found")

  update_data = application_data.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(application, key, value)

  db.commit()
  db.refresh(application)

  return application

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  application = db.query(Application).filter(Application.id == application_id, Application.user_id == current_user.id).first()

  if not application:
    raise HTTPException(status_code=404, detail="Application not found")

  db.delete(application)
  db.commit()

  return None