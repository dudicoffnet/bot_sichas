import os
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from keyboards.main import main_kb
from utils.store import log

router = Router()

@router.message(CommandStart())
async def cmd_start(m: Message):
    splash = os.path.join(os.getcwd(), "assets", "splash.png")
    if os.path.exists(splash):
        await m.answer_photo(FSInputFile(splash), caption="👋 Привет! Это бот «Сейчас».", reply_markup=ReplyKeyboardRemove())
    await m.answer("...", reply_markup=ReplyKeyboardRemove())
    await m.answer("Меню:", reply_markup=main_kb())
    else:
        await m.answer("👋 Привет! Это бот «Сейчас».", reply_markup=ReplyKeyboardRemove())
        await m.answer("...", reply_markup=ReplyKeyboardRemove())
    await m.answer("Меню:", reply_markup=main_kb())
    log(f"/start by {m.from_user.id}")

@router.message(Command("menu"))
async def cmd_menu(m: Message):
    await m.answer("...", reply_markup=ReplyKeyboardRemove())
    await m.answer("Меню:", reply_markup=main_kb())


@router.message(lambda m: (m.text or '').strip() in {'⬅️ Назад в меню','Назад','В меню'})
async def back_to_menu(m: Message):
    from keyboards.main import main_kb
    await m.answer("...", reply_markup=ReplyKeyboardRemove())
    await m.answer("Меню:", reply_markup=main_kb())
