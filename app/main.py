from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
import logging
import os

from app.routers import start, search, admin, donate, settings

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Роутеры
dp.include_router(start.router)
dp.include_router(search.router)
dp.include_router(admin.router)

def run_bot():
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
