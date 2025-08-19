from aiogram import Router
from aiogram.types import Message, FSInputFile
from os import path

router = Router()

@router.message(lambda m: (m.text or "").strip() in {"💖 Помочь проекту", "Помочь проекту"})
async def donate(m: Message):
    text = (
        "Спасибо за поддержку!\n"
        "Можно перевести по QR ниже или по ссылке: https://pay.cloudtips.ru/\n"
        "Если QR не открылся — напиши сюда, пришлю напрямую."
    )
    for candidate in ["assets/qr.png", "assets/donate_qr.png"]:
        if path.exists(candidate):
            try:
                await m.answer_photo(FSInputFile(candidate), caption=text)
                return
            except Exception:
                pass
    await m.answer(text)
