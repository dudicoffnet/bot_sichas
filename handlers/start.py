from aiogram import Router, types
from aiogram.types import FSInputFile
from os import path
from keyboards.main import main_kb

router = Router()

@router.message(commands=["start", "menu"])
async def cmd_start(message: types.Message):
    splash = "assets/splash.png"
    if path.exists(splash):
        try:
            await message.answer_photo(FSInputFile(splash), caption="👋 Привет! Это бот знакомств «Сейчас».")
        except Exception:
            await message.answer("👋 Привет! Это бот знакомств «Сейчас».")
    else:
        await message.answer("👋 Привет! Это бот знакомств «Сейчас».")
    await message.answer("Меню:", reply_markup=main_kb())
