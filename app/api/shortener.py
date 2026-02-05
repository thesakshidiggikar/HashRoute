from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import url as schemas
from ..services.url_service import URLService
from datetime import datetime

router = APIRouter()

@router.post("/shorten", response_model=schemas.ShortenResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(url_request: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    """
    Endpoint to shorten a long URL.
    """
    try:
        db_url = URLService.create_url(db, url_request)
        # Construct the full short URL
        base_url = str(request.base_url)
        short_url = f"{base_url}{db_url.short_code}"
        
        return schemas.ShortenResponse(
            short_url=short_url,
            short_code=db_url.short_code
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """
    Endpoint to redirect from a short code to the original URL.
    """
    db_url = URLService.get_url_by_code(db, short_code)
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )
    
    # Check if expired
    if db_url.expires_at and db_url.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Short code has expired"
        )
        
    return RedirectResponse(url=db_url.original_url)
