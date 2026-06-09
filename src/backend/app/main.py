import os
from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.routers import auth, application, company, note, user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

#Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

cors_origins = os.getenv(
  "CORS_ORIGINS",
  "http://localhost:3000, http://localhost:5173"
).split(",")

app.add_middleware(
  CORSMiddleware,
  allow_origins=[origin.strip() for origin in cors_origins],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=[""],
)

app.include_router(auth.router)
app.include_router(application.router)
app.include_router(company.router)
app.include_router(note.router)
app.include_router(user.router)

@app.get("/health")
def health_check():
  return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
  return RedirectResponse(url="/docs")

