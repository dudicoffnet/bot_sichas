from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import SessionLocal, get_user_by_tg, touch_last_seen, get_or_create_prefs
from app.db.models import User
import random

router = Router()

@router.message(F.text == "🔍 Найти рядом")
async def search_random(msg: Message):
    async with SessionLocal() as session:  # type: AsyncSession
        me = await get_user_by_tg(session, msg.from_user.id)
        await touch_last_seen(session, msg.from_user.id)

        # Базовый случайный подбор (не показываем самого себя и забаненных)
        prefs = await get_or_create_prefs(session, msg.from_user.id)
        conditions = [User.tg_id != msg.from_user.id, User.is_banned == False, User.is_available == True]
        if prefs.city_filter:
            conditions.append(User.city.ilike(prefs.city_filter))
        if prefs.age_min is not None:
            conditions.append(User.age >= prefs.age_min)
        if prefs.age_max is not None:
            conditions.append(User.age <= prefs.age_max)
        res = await session.execute(select(User).where(*conditions))
        users = res.scalars().all()
        if not users:
            return await msg.answer("Пока никого не нашли. Попробуй позже.")

        candidate = random.choice(users)
        # Показ анкеты
        parts = []
        if candidate.name: parts.append(f"<b>{candidate.name}</b>")
        if candidate.age: parts.append(f"{candidate.age} лет")
        if candidate.city: parts.append(candidate.city)
        if candidate.interests: parts.append(f"Интересы: {candidate.interests}")
        status = "онлайн" if candidate.last_seen else "офлайн"
        parts.append(f"статус: {status}")
        caption = " · ".join(parts) if parts else "Анкета"

        if candidate.photo_file_id:
            await msg.answer_photo(candidate.photo_file_id, caption=caption)
        else:
            await msg.answer(caption)
