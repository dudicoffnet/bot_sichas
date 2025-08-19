from aiogram import Router
from aiogram.types import Message, FSInputFile
import os

router = Router()

@router.message(lambda m: (m.text or "").strip() in {"💖 Помочь проекту", "Помочь проекту"})
async def donate(m: Message):
    text = (
        "Спасибо за поддержку!\n"
        "Можно перевести по QR ниже или по ссылке: https://pay.cloudtips.ru/\n"
        "Если QR не открылся — напиши сюда, пришлю напрямую."
    )
    qr = os.path.join("assets", "qr.png")
    if os.path.exists(qr):
        try:
            await m.answer_photo(FSInputFile(qr), caption=text)
            return
        except Exception:
            pass
    await m.answer(text)
