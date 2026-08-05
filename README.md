# 🔗 URL Shortener Service (FastAPI + PostgreSQL)

A lightweight, high-performance RESTful API service built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** to convert long URLs into compact, unique short links with Base62 encoding and HTTP redirects.

---

## 📌 Project Overview

This project was built as a backend web development learning exercise to understand:
- REST API design with **FastAPI**
- Database ORM modeling using **SQLAlchemy**
- Unique hash & encoding algorithms (**Base62**)
- Environment variable management using **Pydantic Settings**
- Automatic interactive API documentation with **Swagger UI**

---

## 🛠️ Tech Stack

* **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
* **Database**: PostgreSQL
* **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
* **Data Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings`
* **Server**: Uvicorn
* **Hashing & Encoding**: Python `hashlib` (MD5) + Custom Base62 Encoder

---

## ✨ Features Implemented

- [x] **URL Shortening (`POST /url/`)**: Takes a long original URL, checks if it already exists in the database, and if not, generates a unique Base62 slug.
- [x] **Collision Handling**: Automatically resolves hash collisions by appending timestamps if a slug conflict occurs.
- [x] **HTTP Redirection (`GET /url/{short}`)**: Seamlessly redirects the user from the short URL slug to the original destination with a `307 Temporary Redirect`.
- [x] **List All URLs (`GET /url/`)**: Fetches all shortened URL mappings from the database.
- [x] **📊 Click Analytics & Visitor Tracking**: Tracks click count per URL and records visitor IP address (`X-Forwarded-For` aware) and User-Agent browser/OS metadata.
- [x] **Environment Configuration**: Safe credential handling using `.env` files parsed by `pydantic-settings`.

---

## 🚀 Pending Features & Future Roadmap

These are features planned to enhance the project further:
- [ ] **✏️ Custom URL Aliases**:
  - Allow users to specify custom short slugs (e.g., `/url/my-custom-name`).
- [ ] **⏱️ URL Expiration / TTL**:
  - Set optional expiration dates for short links (e.g. valid for 7 days).
- [ ] **🔐 User Authentication (JWT)**:
  - Add user registration & login (OAuth2 / JWT).
  - Restrict link management so logged-in users can view, update, or delete their created links.
- [ ] **⚡ Caching Layer (Redis)**:
  - Cache short-to-long URL mappings in Redis for near-instant redirects without querying the database every time.
- [ ] **📱 QR Code Generation**:
  - Automatically generate downloadable QR codes for created short links.
- [ ] **🛑 Rate Limiting & Anti-Abuse**:
  - Protect endpoints against spam and malicious requests using Redis-backed rate limiting.
- [ ] **💻 Frontend Interface**:
  - Build a sleek UI using React/Vite or HTML/CSS to allow easy link shortening and analytics display.

---

## 📁 Directory Structure

```text
url-shorten/
├── README.md               # Project Documentation
└── backend/
    ├── .env                # Environment variables (database URL, secret keys)
    ├── main.py             # FastAPI entry point
    ├── models.py           # SQLAlchemy database tables
    ├── requiremnt.txt      # Python dependencies
    ├── router/
    │   └── url.py          # API route handlers (/url endpoints)
    └── utils/
        ├── config.py       # Pydantic BaseSettings config
        ├── database.py     # Database engine & session setup
        └── schema.py       # Pydantic request/response schemas
```

## 📑 API Endpoints Summary

| Method | Endpoint | Description | Sample Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/url/` | Create a shortened URL | `{"org_url": "https://example.com/very/long/url"}` |
| `GET` | `/url/` | Retrieve all shortened URLs | *None* |
| `GET` | `/url/{short}` | Redirect to original URL | *None* |

Interactive API Documentation (Swagger UI) is available at: **`http://127.0.0.1:8000/docs`**

---

## 📝 Personal Study Note

This repository is developed for **personal learning and backend practice**.

