
def test_user_can_create_note_for_application(client):
  create_response = client.post("/applications/", json={
    "company_name": "Amazon",
    "role_title": "DevOps Engineer",
    "status": "applied",
    "job_link": None,
    "salary_range": 110000,
    "applied_date": "2026-05-22",
    "follow_up_date": None
  })

  application_id = create_response.json()["id"]

  response = client.post(f"/applications/{application_id}/notes", json={
    "content": "Followed up with recruiter"
  })

  assert response.status_code == 200 or response.status_code == 201
  assert response.json()["content"] == "Followed up with recruiter"

def test_user_can_get_notes_for_application(client):
  create_response = client.post("/applications/", json={
    "company_name": "Amazon",
    "role_title": "DevOps Engineer",
    "status": "applied",
    "job_link": None,
    "salary_range": 110000,
    "applied_date": "2026-05-22",
    "follow_up_date": None
  })

  application_id = create_response.json()["id"]

  client.post(f"/applications/{application_id}/notes", json={
    "content": "Followed up with recruiter"
  })

  response = client.get(f"/applications/{application_id}/notes")

  assert response.status_code == 200
  assert isinstance(response.json(), list)
  assert len(response.json()) >= 1

def test_cannot_create_note_for_missing_application(client):
  response = client.post("/applications/99999/notes", json={
    "content": "This should fail"
  })

  assert response.status_code == 404