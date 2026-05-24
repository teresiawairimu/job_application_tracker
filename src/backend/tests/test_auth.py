from app.models.user import User
from tests.conftest import TestingSessionLocal, unauthenticated_client

def test_user_can_register_and_is_stored_in_db(client):
  response = client.post(
    "auth/signup",
    json={
      "name": "New User",
      "email": "newuser@example.com",
      "password": "password123"
    }
  )

  assert response.status_code == 201

  db = TestingSessionLocal()
  user = db.query(User).filter(User.email == "newuser@example.com").first()
  db.close()

  assert user is not None
  assert user.name == "New User"
  assert user.email == "newuser@example.com"


def test_user_cannot_register_with_duplicate_email(client):
  user_payload = {
    "name": "Test User",
    "email": "duplicate@example.com",
    "password": "password123"
  }

  first_response = client.post("/auth/signup", json=user_payload)
  assert first_response.status_code == 201

  second_response = client.post("/auth/signup", json=user_payload)
  assert second_response.status_code == 400

  data = second_response.json()
  assert "detail" in data

def test_user_can_login(client):
  user_payload = {
    "name": "Test User",
    "email": "login@example.com",
    "password": "password456"
  }

  first_response = client.post("/auth/signup", json=user_payload)
  assert first_response.status_code == 201

  second_response = client.post("/auth/login", data={
    "username":"login@example.com",
    "password":"password456"
  })
  assert second_response.status_code == 200

  data = second_response.json()
  assert "access_token" in data
  assert data["token_type"] == "bearer"

def test_login_fails_with_wrong_password(client):
  user_payload = {
    "name": "Test User",
    "email": "wrongpassword@example.com",
    "password": "password"
  }

  first_response = client.post("/auth/signup", json=user_payload)
  assert first_response.status_code == 201

  second_response = client.post("/auth/login", data={
    "username": "wrongpassword@example.com",
    "password": "wrongpassword"
  })


  assert second_response.status_code == 401
  assert second_response.json()
  ["detail"] == "invalid email or password"

 
def test_protected_route_fails_without_token(unauthenticated_client):
  response = unauthenticated_client.get("/applications")
  assert response.status_code == 401

 