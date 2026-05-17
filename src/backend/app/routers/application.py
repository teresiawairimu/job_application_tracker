from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user, get_db
from app.models.application import Application
from app.models.user import User
from app.models.company import Company
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  company = db.query(Company).filter(Company.name == application.company_name).first()
  
  if not company:
    company = Company(name=application.company_name)
    db.add(company)
    db.commit()
    db.refresh(company)

  db_application = Application(
    user_id=current_user.id,
    company_id=company.id,
    role_title=application.role_title,
    status=application.status,
    job_link=application.job_link,
    salary_range=application.salary_range,
    applied_date=application.applied_date,
    follow_up_date=application.follow_up_date,
  )
  
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


  if "company_name" in update_data:
    company_name = update_data.pop("company_name")

    company = db.query(Company).filter(Company.name == company_name).first()

    if not company:
      company = Company(name=company_name)
      db.add(company)
      db.commit()
      db.refresh(company)

    application.company_id = company.id

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