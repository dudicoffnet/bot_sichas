
import os
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()

def donate_kb():
    buttons = []
    for key, title in [("DONATE_URL","ЮMoney"), ("BOOSTY_URL","Boosty"), ("DONATEPAY_URL","DonatePay")]:
        url = os.getenv(key)
        if url:
            buttons.append([InlineKeyboardButton(text=title, url=url)])
    return InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

@router.message(lambda m: (m.text or "").strip() in {"💖 Помочь проекту","Помочь проекту","Донат","Поддержать"})
async def donate(m: Message):
    kb = donate_kb()
    qr = os.path.join(os.getcwd(), "assets", "donate_qr.png")
    if os.path.exists(qr):
        await m.answer_photo(FSInputFile(qr), caption="Поддержать проект:", reply_markup=kb)
    else:
        txt = "Поддержать проект"
        if kb:
            await m.answer(txt, reply_markup=kb)
        else:
            await m.answer("Добавь ссылки DONATE_URL/BOOSTY_URL/DONATEPAY_URL или положи assets/donate_qr.png")
