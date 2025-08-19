# aiogram v3 entrypoint with webhook turn-off to ensure polling works
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import start as h_start
from handlers import anketa as h_anketa
from handlers import donate as h_donate
from handlers import settings as h_settings

logging.basicConfig(level=logging.INFO)

def _get_token() -> str:
    for key in ("BOT_TOKEN", "TOKEN", "TELEGRAM_TOKEN"):
        val = os.getenv(key)
        if val and val.strip():
            return val.strip()
    token_file = "token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    raise RuntimeError("Не найден токен бота. Установи BOT_TOKEN/TOKEN/TELEGRAM_TOKEN или token.txt.")

async def main() -> None:
    token = _get_token()
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # IMPORTANT: disable any old webhook to receive messages via polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        pass

    dp.include_router(h_start.router)
    dp.include_router(h_anketa.router)
    dp.include_router(h_donate.router)
    dp.include_router(h_settings.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
