from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from app.config import get_settings

router = Router()
SET = get_settings()

@router.message(Command("donate"))
@router.message(lambda m: m.text == "💖 Помочь проекту")
async def donate(msg: Message):
    kb = []
    if SET.donate_url:
        kb.append([InlineKeyboardButton(text="ЮMoney", url=SET.donate_url)])
    if SET.boosty_url:
        kb.append([InlineKeyboardButton(text="Boosty", url=SET.boosty_url)])
    if SET.donatepay_url:
        kb.append([InlineKeyboardButton(text="DonatePay", url=SET.donatepay_url)])
    if not kb:
        await msg.answer("Ссылки на донат не настроены. Добавь в переменные окружения DONATE_URL/BOOSTY_URL/DONATEPAY_URL.")
        return
    await msg.answer("Поддержать проект:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
