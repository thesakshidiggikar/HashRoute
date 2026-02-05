from fastapi import FastAPI
from .database import engine, Base
from .routers import shortener

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HashRoute API",
    description="A high-performance, industry-standard URL shortener backend.",
    version="1.0.0"
)

# Include routers
app.include_router(shortener.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "HashRoute"}
