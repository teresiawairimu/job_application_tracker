from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth import get_current_user, get_db
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  
  db_company = Company(**company.model_dump())
  db.add(db_company)
  db.commit()
  db.refresh(db_company)
  return db_company


@router.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  return db.query(Company).all()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  company = db.query(Company).filter(Company.id == company_id).first()

  if not company:
    raise HTTPException(status=404, detail="Company not found")
  
  return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_data: CompanyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  company = db.query(Company).filter(Company.id == company_id).first()

  if not company:
    raise HTTPException(status=404, details="Company not found")
  
  update_data = company_data.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(company, key, value)

  db.commit()
  db.refresh(company)
  
  return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  company = db.query(Company).filter(Company.id == company_id).first()

  if not company:
    raise HTTPException(status=404, details="Company not found")
  
  db.delete(company)
  db.commit()

  return None