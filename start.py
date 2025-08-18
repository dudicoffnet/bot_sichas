import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import get_settings
from app.db.engine import init_db
from app.handlers import start as h_start
from app.handlers import profile as h_profile
from app.handlers import search as h_search
from app.handlers import donate as h_donate
from app.handlers import settings as h_settings
from app.handlers import admin as h_admin
from app.handlers import fallback as h_fallback

logging.basicConfig(level=logging.INFO)

def build_dp() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(h_start.router)
    dp.include_router(h_profile.router)
    dp.include_router(h_search.router)
    dp.include_router(h_donate.router)
    dp.include_router(h_settings.router)
    dp.include_router(h_admin.router)
    dp.include_router(h_fallback.router)
    return dp

async def main():
    settings = get_settings()
    if not settings.bot_token or settings.bot_token.startswith("000000"):
        raise RuntimeError("Заполни BOT_TOKEN в .env")
    if not settings.db_url:
        raise RuntimeError("Заполни DATABASE_URL в .env")

    await init_db()
    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    dp = build_dp()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
