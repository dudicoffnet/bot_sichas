from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN","")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # Если есть заставка в assets/splash.png — отправим её
    splash_path = "assets/splash.png"
    if os.path.exists(splash_path):
        try:
            from aiogram.types import InputFile
            await message.answer_photo(InputFile(splash_path),
                                       caption="👋 Добро пожаловать! Меню ниже.")
        except Exception:
            await message.answer("👋 Добро пожаловать! (заставка не отправилась)")
    else:
        await message.answer("👋 Добро пожаловать!")

    await message.answer("Готово. Картинки ищутся в папке assets/.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
