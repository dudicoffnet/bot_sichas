from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from app.keyboards.main import main_kb
import os

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    splash_path = os.path.join(os.getcwd(), "assets", "splash.png")
    if os.path.exists(splash_path):
        await message.answer_photo(FSInputFile(splash_path), caption="👋 Привет! Это бот «Сейчас».", reply_markup=main_kb())
    else:
        await message.answer("👋 Привет! Это бот «Сейчас».", reply_markup=main_kb())

@router.message(Command("menu"))
async def menu_handler(message: Message):
    await message.answer("Меню открыто.", reply_markup=main_kb())
