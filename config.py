import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SEARCH_RADIUS_KM: float = float(os.getenv("SEARCH_RADIUS_KM", "50"))

settings = Settings()
