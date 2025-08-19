from aiogram import Router, types
from aiogram.types import FSInputFile

router = Router()

@router.message(lambda m: m.text == "💖 Помочь проекту")
async def donate(message: types.Message):
    qr = FSInputFile("assets/qr.png")
    await message.answer_photo(qr, caption="Спасибо за поддержку проекта! 🙏")
