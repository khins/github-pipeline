# GitHub Data Pipeline

A Python-based data pipeline that extracts, transforms, and analyzes GitHub user data.

## 🚀 Features
- Fetch GitHub user data via API
- Retrieve and analyze repositories
- Filter and sort repositories by popularity
- Sync users and repositories to Postgres via `/sync/{username}`

## 🧱 Project Structure

## 🐘 Postgres Setup
1. Start Postgres:
   `docker compose up -d db`
2. Copy env file:
   `cp .env.example .env`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run API:
   `uvicorn src.app:app --reload`

On startup, tables are auto-created from SQLAlchemy models.

## 🔄 Sync Endpoint
- `POST /sync/{username}`
- Example:
  `curl -X POST http://127.0.0.1:8000/sync/octocat`
