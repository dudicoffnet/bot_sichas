from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from app.keyboards.main import main_kb
from app.db.engine import SessionLocal, get_user_by_tg, touch_last_seen
from app.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Update/ensure user in DB
    async with SessionLocal() as session:  # type: AsyncSession
        user = await get_user_by_tg(session, message.from_user.id)
        if not user:
            user = User(tg_id=message.from_user.id, name=message.from_user.full_name or None)
            session.add(user)
            await session.commit()
        await touch_last_seen(session, message.from_user.id)

    splash_path = os.path.join(os.getcwd(), "assets", "splash.png")
    if os.path.exists(splash_path):
        await message.answer_photo(
            FSInputFile(splash_path),
            caption="Добро пожаловать в «Сейчас».",
            reply_markup=main_kb()
        )
    else:
        await message.answer("Добро пожаловать в «Сейчас».", reply_markup=main_kb())

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Меню открыто.", reply_markup=main_kb())
