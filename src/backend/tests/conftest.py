import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from types import SimpleNamespace
from app.main import app
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.application import Application
from app.models.company import Company
from app.models.note import Note
from app.database import Base


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
  raise RuntimeError("TEST_DATABASE_URL is not set")

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=test_engine
)
def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

def override_get_current_user():
  return SimpleNamespace(
    id=1,
    name="Test User",
    email="test@example.com"
  )

@pytest.fixture
def client():

  Base.metadata.create_all(bind=test_engine)

  db = TestingSessionLocal()

  test_user = User(
    name="Test User",
    email="test@example.com",
    hashed_password="fakehashedpassword"
  )

  db.add(test_user)
  db.commit()
  db.close()

  app.dependency_overrides[get_db] = override_get_db
  app.dependency_overrides[get_current_user] = override_get_current_user

  with TestClient(app) as test_client:
    yield test_client

  app.dependency_overrides.clear()
  Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def unauthenticated_client():
  Base.metadata.create_all(bind=test_engine)
  app.dependency_overrides[get_db] = override_get_db

  with TestClient(app) as test_client:
    yield test_client

  app.dependency_overrides.clear()
  Base.metadata.drop_all(bind=test_engine)
  app.dependency_overrides.clear()
  Base.metadata.drop_all(bind=test_engine)
