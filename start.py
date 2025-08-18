import asyncio
import logging

from app.bot import bot, dp
from app.handlers.anketa import register_anketa_handlers
from app.handlers.menu import register_menu_handlers

async def main():
    logging.basicConfig(level=logging.INFO)
    register_anketa_handlers(dp)
    register_menu_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
