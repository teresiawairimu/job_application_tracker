from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.routers import auth, application, company, note, user

#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

app.include_router(auth.router)
app.include_router(application.router)
app.include_router(company.router)
app.include_router(note.router)
app.include_router(user.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}


