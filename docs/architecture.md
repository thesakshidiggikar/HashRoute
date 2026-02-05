# Implementation Plan - URL Shortener API

Build a production-grade URL shortener service using FastAPI and SQLAlchemy, focusing on clean architecture and scalability.

## Proposed Changes

### Project Structure
Organize the code into a clean, modular structure:
`hashroute/`
├── `app/`
│   ├── `main.py` (Entry point)
│   ├── `database.py` (DB connection/session)
│   ├── `models.py` (SQLAlchemy models)
│   ├── `schemas.py` (Pydantic models)
│   ├── `routers/`
│   │   └── `shortener.py` (API routes only)
│   ├── `services/`
│   │   └── `url_service.py` (Business logic)
│   └── `utils/`
│       └── `hash.py` (Base62 / hashing utilities)
├── `README.md`
└── `requirements.txt`

### Database Design
- **Table**: `urls`
- **Fields**:
    - `id`: Primary Key (Integer)
    - `original_url`: The long URL (String, indexed)
    - `short_code`: Unique identifier (String, unique index)
    - `created_at`: Timestamp
    - `expires_at`: Optional expiration timestamp
    - `click_count`: Number of times the link was accessed

### Short-Code Generation Strategy
- I will use a **Base62 encoding** approach. 
- To handle collisions and ensure uniqueness:
    1. Generate a hash (e.g., MD5) of the original URL.
    2. Take a portion of the hash and encode it in Base62.
    3. If a collision occurs (rare with 6-8 chars), append a salt or use an incremental ID approach (or just retry with a different hash slice).
- *Alternative*: Use a counter-based approach (distributed counter for scale) but for this project, a hash-based or random-code with collision retry is cleaner to demonstrate.

### API Endpoints
- `POST /shorten`: Accepts a long URL, returns the short code.
- `GET /{short_code}`: Redirects to the original URL.

## Verification Plan

### Automated Tests
- I will write a simple test script using `httpx` or `requests` to verify:
    - URL shortening works.
    - Redirection works.
    - Invalid short codes return 404.
    - Duplicate URLs return the same short code (idempotency).

### Manual Verification
- Use `curl` or FastAPI's `/docs` (Swagger UI) to manual test the endpoints.
