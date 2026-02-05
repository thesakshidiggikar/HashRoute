# HashRoute Project Walkthrough

I have completed the development of **HashRoute**, an industry-standard URL shortener backend built with FastAPI and SQLAlchemy.

## 🏗 Key Features & Architecture
- **Layered Architecture**: Clean separation of API routes, business logic (services), and database models.
- **Base62 Hashing**: Efficient and unique short code generation.
- **Idempotency**: Same URL always results in the same short code.
- **Expiration Handling**: Support for link expiration with proper HTTP status codes.
- **Production Ready**: Fully documented with a comprehensive README and clean, indexed database logic.

## 📂 Project Structure
```text
hashroute/
├── app/
│   ├── main.py            (Entry point)
│   ├── database.py        (SQLAlchemy Setup)
│   ├── models.py          (URL Model with Indexes)
│   ├── schemas.py         (Pydantic Validation)
│   ├── routers/
│   │   └── shortener.py   (API Routes)
│   ├── services/
│   │   └── url_service.py (Business Logic)
│   └── utils/
│       └── hash.py        (Base62 Utility)
├── README.md
└── requirements.txt
```

## 📸 System Previews

![Swagger UI](C:/Users/Sakshi/.gemini/antigravity/brain/743bfe50-ae84-40a4-849f-67ed740065ce/swagger_overview.png)
*Interactive Documentation*

![API Response](C:/Users/Sakshi/.gemini/antigravity/brain/743bfe50-ae84-40a4-849f-67ed740065ce/post_response.png)
*Successful Shortening Workflow*

## 🧪 Verification Results
The system was verified for:
1. **Health Check**: Ensure service is alive.
2. **Shortening**: Success with 201 Created and return of short code/URL.
3. **Redirection**: Success with 307 Temporary Redirect to original URL.
4. **Idempotency**: Multiple requests for same URL return same short code.
5. **Error Handling**: 404 for invalid codes and 410 for expired links.

### How to Run
```bash
# 1. Start the server
uvicorn app.main:app --reload

# 2. (Optional) Run the verification script
python verify_api.py
```
