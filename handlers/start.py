from utils.menu_log import _dbg_menu_log
import os
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from keyboards.main import main_kb
from utils.store import log

router = Router()

@router.message(CommandStart())
async def cmd_start(m: Message):
    _dbg_menu_log("start"); await m.answer("👋 Привет! Это бот «Сейчас».", reply_markup=main_kb())
    log(f"/start by {m.from_user.id}")

@router.message(Command("menu"))
async def cmd_menu(m: Message):
    _dbg_menu_log("menu"); await m.answer("Меню:", reply_markup=main_kb())

