import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "7583232552:AAGDMqbLFbFRMxmqOTJQELm33phhdxmtyPM"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

from handlers import start, profile, search, donate, settings, admin
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(search.router)
dp.include_router(settings.router)
dp.include_router(donate.router)
dp.include_router(admin.router)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
