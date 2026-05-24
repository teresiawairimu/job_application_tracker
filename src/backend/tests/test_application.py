
def test_user_can_create_application(client):
  response = client.post("/applications/", json={
    "company_name": "Google",
    "role_title": "Backend Developer",
    "status": "applied",
    "job_link": "https://example.com/job",
    "salary_range": 100000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-29"
  })

  assert response.status_code == 200 or response.status_code == 201
  data = response.json()
  assert data["role_title"] =="Backend Developer"
  assert data["status"] == "applied"

def test_user_can_get_applications(client):
  client.post("/applications/", json={
    "company_name": "Google",
    "role_title": "Backend Developer",
    "status": "applied",
    "job_link": "https://example.com/job",
    "salary_range": 100000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-29"
  })

  response = client.get("/applications/")

  assert response.status_code == 200
  data = response.json()
  assert isinstance(data, list)
  assert len(data) >= 1

def test_user_can_get_single_application(client):
  create_response = client.post("/applications/", json={
    "company_name": "Google",
    "role_title": "Backend Developer",
    "status": "applied",
    "job_link": "https://example.com/job",
    "salary_range": 100000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-29"
  })

  application_id = create_response.json()["id"]

  response = client.get(f"/applications/{application_id}")

  assert response.status_code == 200
  assert response.json()["id"] == application_id

def test_user_can_update_application(client):
  create_response = client.post("/applications/", json={
    "company_name": "Google",
    "role_title": "Backend Developer",
    "status": "applied",
    "job_link": "https://example.com/job",
    "salary_range": 100000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-29"
  })

  application_id = create_response.json()["id"]

  response = client.put(f"/applications/{application_id}", json={
    "company_name": "Google",
    "role_title": "Senior Backend Developer",
    "status": "interview",
    "job_link": "https://example.com/job",
    "salary_range": 120000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-30"
  })

  assert response.status_code == 200
  assert response.json()["role_title"] == "Senior Backend Developer"
  assert response.json()["status"] == "interview"


def test_user_can_delete_application(client):
  create_response = client.post("/applications/", json={
    "company_name": "Google",
    "role_title": "Backend Developer",
    "status": "applied",
    "job_link": "https://example.com/job",
    "salary_range": 100000,
    "applied_date": "2026-05-22",
    "follow_up_date": "2026-05-29"
  })

  application_id = create_response.json()["id"]

  delete_response = client.delete(f"/applications/{application_id}")
  assert delete_response.status_code == 200 or delete_response.status_code == 204

  get_response = client.get(f"/applications/{application_id}")
  assert get_response.status_code == 404