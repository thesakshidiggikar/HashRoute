from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    expires_at: Optional[datetime] = None

class URLInfo(URLBase):
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    click_count: int

    class Config:
        from_attributes = True

class ShortenResponse(BaseModel):
    short_url: str
    short_code: str
