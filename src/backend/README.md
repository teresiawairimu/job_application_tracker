# Job Application Tracker

A backend application for tracking job application, companies, notes, and application statuses.

## Features

- User registration and login
- Create, view, update, and delete job applications
- Track companies connected to applications
- Add notes to applications
- Prevent duplicate user emails
- PostgreSQL database integration
- Alembic database migrations
- Backend testing with pytest

## Tech Stack

- Backend Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Database migrations: Alembic
- Testing: Pytest
- Containerized development: Docker

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/job_application_tracker.git
cd job_application_tracker/src/backend
```
Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://database_user:password@localhost:5432/database_name
TEST_DATABASE_URL=postgresql://database_user:password@localhost:5432/test_database_name
```

## Database Migrations

Run migrations with Alembic:

```bash
alembic upgrade head
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## Running Tests

```bash
PYTHONPATH=. pytest
```
