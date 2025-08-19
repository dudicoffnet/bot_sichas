
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
import logging
import os

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔍 Найти рядом"))
    kb.add(KeyboardButton("📋 Моя анкета"))
    kb.add(KeyboardButton("⚙️ Настройки"))
    kb.add(KeyboardButton("💖 Помочь проекту"))
    kb.add(KeyboardButton("⬅️ Назад в меню"))
    return kb

@dp.message_handler(commands=["start", "menu"])
async def send_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_kb())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
