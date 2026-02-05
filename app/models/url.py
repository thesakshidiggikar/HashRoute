from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from ..database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)

    # Adding explicit indexes as per industry standard for high-performance lookups
    __table_args__ = (
        Index("idx_short_code", "short_code"),
    )
