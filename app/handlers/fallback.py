from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def fallback(msg: Message):
    await msg.answer("Хм, не понял команду. Попробуй ещё раз через меню /menu.")
