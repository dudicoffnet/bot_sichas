from aiogram import Router, F
from aiogram.types import Message
from app.keyboards.main import ALIASES_SETTINGS

router = Router()

@router.message(F.text.func(lambda t: t and t.strip() in ALIASES_SETTINGS))
async def settings_handler(msg: Message):
    await msg.answer("Настройки пока минимальные. В следующей сборке добавим расширенное меню.")
