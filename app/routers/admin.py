from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda m: m.text == "Админ")
async def admin_handler(message: Message):
    await message.answer("🔧 Панель администратора. (Пока базовая версия).")
