import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SEARCH_RADIUS_KM: float = float(os.getenv("SEARCH_RADIUS_KM", "10"))

settings = Settings()
