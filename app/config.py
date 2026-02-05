import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "HashRoute")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hashroute.db")
    
    # Shortener Settings
    SHORT_CODE_LENGTH: int = 7

settings = Settings()
