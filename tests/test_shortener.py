from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use an in-memory database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_shorten_url():
    """Test creating a short URL."""
    response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["short_url"].endswith(data["short_code"])

def test_redirect_to_url():
    """Test the redirection flow."""
    # First, shorten a URL
    create_resp = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )
    short_code = create_resp.json()["short_code"]
    
    # Then, attempt to redirect
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.google.com/"

def test_short_code_not_found():
    """Test redirection with an invalid code."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short code not found"

def test_idempotency():
    """Test that shortening the same URL twice returns the same code."""
    url = "https://www.example.com"
    resp1 = client.post("/shorten", json={"original_url": url})
    resp2 = client.post("/shorten", json={"original_url": url})
    
    assert resp1.json()["short_code"] == resp2.json()["short_code"]
