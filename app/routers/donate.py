from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from app.keyboards.main import ALIASES_DONATE
import os

router = Router()

def _donate_kb():
    buttons = []
    for key, text in [("DONATE_URL", "ЮMoney"), ("BOOSTY_URL", "Boosty"), ("DONATEPAY_URL", "DonatePay")]:
        url = os.getenv(key)
        if url:
            buttons.append([InlineKeyboardButton(text=text, url=url)])
    return InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

@router.message(F.text.func(lambda t: t and t.strip() in ALIASES_DONATE))
async def donate_handler(msg: Message):
    kb = _donate_kb()
    qr_path = os.path.join(os.getcwd(), "assets", "donate_qr.png")
    if os.path.exists(qr_path):
        await msg.answer_photo(FSInputFile(qr_path), caption="Поддержать проект:", reply_markup=kb)
        if not kb:
            await msg.answer("Можно добавить ссылки DONATE_URL/BOOSTY_URL/DONATEPAY_URL в переменные окружения.")
    else:
        if kb:
            await msg.answer("Поддержать проект:", reply_markup=kb)
        else:
            await msg.answer("Ссылки на донат не настроены и QR не найден. Положи assets/donate_qr.png или добавь DONATE_URL.")
