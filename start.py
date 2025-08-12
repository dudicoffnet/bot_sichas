import logging
import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from keyboards.main import kb_main
from handlers.registration import register_handlers_registration
from data.db import init_db

API_TOKEN = "7583232552:AAFr8NsGn0uSEyU_J-C4RUno8oC4q3BumnA"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# DB init
init_db()

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    welcome = (
        "👋 Привет! Это бот «Сейчас» — для моментальных встреч без лишней переписки.\n"
        "Нажми кнопки ниже. Начни с заполнения анкеты."
    )
    await message.answer(welcome, reply_markup=kb_main)

def main():
    register_handlers_registration(dp)
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
