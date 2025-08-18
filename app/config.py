from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    bot_token: str
    db_url: str
    search_radius_km: int
    admins: list[int]
    donate_url: str | None
    boosty_url: str | None
    donatepay_url: str | None

def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "")
    db_url = os.getenv("DATABASE_URL", "")
    sr = int(os.getenv("SEARCH_RADIUS_KM", "10"))
    admins_raw = os.getenv("ADMINS", "").strip()
    admins = []
    if admins_raw:
        for part in admins_raw.split():
            try:
                admins.append(int(part))
            except ValueError:
                pass
    donate_url = os.getenv("DONATE_URL")
    boosty_url = os.getenv("BOOSTY_URL")
    donatepay_url = os.getenv("DONATEPAY_URL")
    return Settings(
        bot_token=token,
        db_url=db_url,
        search_radius_km=sr,
        admins=admins,
        donate_url=donate_url,
        boosty_url=boosty_url,
        donatepay_url=donatepay_url,
    )
