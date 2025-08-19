from aiogram import Router
from aiogram.types import Message, FSInputFile
from keyboards.main import main_kb
import os

router = Router()

INTRO_TEXT = (
    "Приглашаю Вас в новый формат встреч «Здесь и сейчас» — онлайн, без договоренностей.\n"
    "Запуск новой платформы. Далее будет приложение. Удачи!"
)

@router.message(lambda m: m.text and m.text.startswith("/start"))
async def cmd_start(m: Message):
    splash = os.path.join("assets", "splash.png")
    if os.path.exists(splash):
        try:
            await m.answer_photo(FSInputFile(splash), caption=INTRO_TEXT)
        except Exception:
            await m.answer(INTRO_TEXT)
    else:
        await m.answer(INTRO_TEXT)
    await m.answer("Меню:", reply_markup=main_kb())

@router.message(lambda m: m.text and m.text.startswith("/menu"))
async def cmd_menu(m: Message):
    await m.answer("Меню:", reply_markup=main_kb())
