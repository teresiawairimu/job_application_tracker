
def test_company_is_created_when_application_is_created(client):
  response = client.post("/applications/", json={
    "company_name": "Microsoft",
    "role_title": "Software Engineer",
    "status": "applied",
    "job_link": None,
    "salary_range": 90000,
    "applied_date": "2026-05-22",
    "follow_up_date": None
  })

  assert response.status_code == 200 or response.status_code == 201

  data = response.json()
  assert data["company_id"] is not None

def test_user_can_get_companies(client):
  client.post("/applications/", json={
    "company_name": "Microsoft",
    "role_title": "Software Engineer",
    "status": "applied",
    "job_link": None,
    "salary_range": 90000,
    "applied_date": "2026-05-22",
    "follow_up_date": None
  })

  response = client.get("/companies/")

  assert response.status_code == 200
  assert isinstance(response.json(), list)

def test_user_can_get_single_company(client):
  create_response = client.post("/applications/", json={
    "company_name": "Microsoft",
    "role_title": "Software Engineer",
    "status": "applied",
    "job_link": None,
    "salary_range": 90000,
    "applied_date": "2026-05-22",
    "follow_up_date": None
  })

  company_id = create_response.json()["company_id"]

  response = client.get(f"/companies/{company_id}")

  assert response.status_code == 200
  assert response.json()["id"] == company_id