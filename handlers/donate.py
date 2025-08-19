
import os
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()

def donate_kb():
    buttons = []
    mapping = [("DONATE_URL","ЮMoney"), ("BOOSTY_URL","Boosty"), ("DONATEPAY_URL","DonatePay")]
    for env, title in mapping:
        url = os.getenv(env)
        if url:
            buttons.append([InlineKeyboardButton(text=title, url=url)])
    return InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

@router.message(lambda m: (m.text or '').strip() in {'💖 Помочь проекту','Помочь проекту','Донат','Поддержать'})
async def donate(m: Message):
    kb = donate_kb()
    qr_path = os.path.join(os.getcwd(), "assets", "donate_qr.png")
    if os.path.exists(qr_path):
        await m.answer_photo(FSInputFile(qr_path), caption="Поддержать проект:", reply_markup=kb)
    else:
        await m.answer("Поддержать проект:", reply_markup=kb)
