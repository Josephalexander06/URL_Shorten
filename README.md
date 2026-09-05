# URL Shortener

A full-stack URL shortener built as a backend engineering learning project. Authenticated users can create and manage short links from a React dashboard; the FastAPI service redirects visitors efficiently while tracking basic usage data.

This project explores API design, authentication, relational data modelling, database migrations, Redis-backed caching and rate limiting, and a TypeScript frontend.

## Highlights

- Create short links from long URLs with deterministic Base62-style slugs
- Choose a validated custom alias (`3–50` letters, numbers, `_`, or `-`)
- Register and sign in with hashed passwords and JWT bearer tokens
- Keep each user's links separate in their dashboard
- Redirect short links with HTTP `307 Temporary Redirect`
- Set a seven-day expiry for newly created links
- Record a link's click count, last visitor IP, user agent, and access time
- Cache redirect targets in Redis for one hour
- Apply Redis-backed IP rate limiting to public and auth routes
- Generate and download a PNG QR code for every link
- Manage the PostgreSQL schema with Alembic

## Tech stack

| Area | Technology |
| --- | --- |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL, Alembic |
| Caching / limits | Redis |
| Authentication | JWT, OAuth2 password flow, pwdlib |
| Frontend | React, TypeScript, Vite, Axios |
| Extras | Pydantic Settings, `qrcode`, `user-agents` |

## Architecture

```text
React + Vite dashboard
        │ HTTP + Bearer token
        ▼
FastAPI API ─────────────► PostgreSQL
   │                         users and URL records
   └─────────────────────► Redis
                             redirect cache and rate-limit counters
```

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 20+
- PostgreSQL
- Redis running locally on port `6379`

### 1. Configure the backend

Create `backend/.env`. It is intentionally ignored by Git—never commit real credentials.

```env
DB_URL=postgresql+psycopg2://postgres:your-password@localhost:5432/url_shortener
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

Install the Python dependencies in a virtual environment:

```bash
python -m venv backend/.venv
# Create the virtual-environment folder once
python -m venv backend/.venv

# Activate it every time you open a new terminal
source backend/.venv/bin/activate
pip install -r backend/requiremnts.txt
```

> The second command lists runtime packages currently used by the application that should be consolidated into `backend/requiremnts.txt` as part of the cleanup checklist below.

Apply the database migration from the repository root:

```bash
alembic upgrade head
```

Start the API:

```bash
cd backend
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`, create an account, then create your first link.

## API overview

| Method | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| `POST` | `/user/register` | No | Create an account |
| `POST` | `/user/login` | No | Receive a JWT access token (OAuth2 form data) |
| `POST` | `/url/` | Yes | Create a short link or custom alias |
| `GET` | `/url/` | Yes | List the signed-in user's links |
| `GET` | `/url/{short}` | No | Redirect a visitor to the original URL |
| `POST` | `/url/{short}/qr` | No | Download a QR-code PNG |

## Project structure

```text
.
├── alembic/                  # Database migration environment and revisions
├── backend/
│   ├── core/                 # Application settings and JWT/password helpers
│   ├── router/               # Authentication and URL route handlers
│   ├── utilis/               # Shared dependencies, including rate limiting
│   ├── database.py           # SQLAlchemy engine and session dependency
│   ├── models.py             # User and URL database models
│   └── schema.py             # Request validation models
└── frontend/src/
    ├── pages/                # Landing, auth, and dashboard screens
    └── api.ts                # Axios client and JWT request interceptor
```

## Implementation status

### Complete

- [x] JWT registration and login
- [x] User-owned links and custom aliases
- [x] Redis redirect caching and rate limiting
- [x] Link expiry and basic click tracking
- [x] QR-code generation
- [x] Alembic initial migration
- [x] React dashboard

### Next to complete

- [ ] Add update and delete link endpoints plus dashboard controls
- [ ] Add automated API and frontend tests
- [ ] Check expiry before serving a Redis cache hit and invalidate cache on changes
- [ ] Store visits in a separate analytics table instead of overwriting the latest visitor
- [ ] Replace MD5-derived slugs with securely random, collision-safe IDs
- [ ] Move Redis configuration to environment settings and handle Redis outages gracefully
- [ ] Consolidate all backend runtime packages in `backend/requiremnts.txt`
- [ ] Add Docker Compose for API, PostgreSQL, and Redis
- [ ] Add `.env.example`, screenshots, and deployment instructions
- [ ] Deploy a live demo and add its URL here

## Notes and current limitations

- Links are globally unique; creating the same original URL returns the existing mapping.
- Expiry is currently fixed at seven days when a link is created.
- The analytics fields represent the latest visit and total click count, rather than a full visit history.
- The frontend API URL is currently fixed to `http://localhost:8000`; make it an environment variable before deployment.

## Learning goals

This repository was built to practice production-relevant backend concepts—not only CRUD endpoints. The next steps above are intentionally focused on reliability, security, testing, and deployment: the work that turns a finished learning project into a stronger portfolio project.
