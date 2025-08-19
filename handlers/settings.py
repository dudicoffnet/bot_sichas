
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(lambda m: (m.text or "").strip() in {"⚙️ Настройки","Настройки"})
async def settings(m: Message):
    await m.answer("Настройки профиля и видимости (в разработке).")
