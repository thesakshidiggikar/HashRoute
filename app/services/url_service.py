from sqlalchemy.orm import Session
from datetime import datetime
from ..models import url as models
from ..schemas import url as schemas
from ..utils.hash import generate_short_code

class URLService:
    @staticmethod
    def get_url_by_code(db: Session, short_code: str):
        """Fetches a URL record by its short code and increments click count."""
        db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
        if db_url:
            db_url.click_count += 1
            db.commit()
            db.refresh(db_url)
        return db_url

    @staticmethod
    def create_url(db: Session, url_create: schemas.URLCreate):
        """
        Processes URL shortening.
        Check if URL already exists, handle collisions, and store new record.
        """
        # 1. Check if the original URL already exists (idempotency)
        existing_url = db.query(models.URL).filter(
            models.URL.original_url == str(url_create.original_url)
        ).first()

        if existing_url:
            return existing_url

        # 2. Generate short code and handle potential (though rare) collisions
        short_code = generate_short_code(str(url_create.original_url))
        
        # Collision check loop
        attempts = 0
        while db.query(models.URL).filter(models.URL.short_code == short_code).first():
            attempts += 1
            # Add salt to change the hash if collision occurs
            short_code = generate_short_code(str(url_create.original_url), salt=str(attempts))
            if attempts > 5:
                # Fallback or error if multiple collisions (statistically unlikely with md5/base62)
                raise Exception("Failed to generate a unique short code")

        # 3. Create new record
        db_url = models.URL(
            original_url=str(url_create.original_url),
            short_code=short_code,
            expires_at=url_create.expires_at
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        return db_url
