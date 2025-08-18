from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.engine import SessionLocal, get_user_by_tg, get_or_create_prefs
from app.db.models import User

router = Router()

@router.message(lambda m: m.text == "⚙️ Настройки")
@router.message(Command("settings"))
async def settings_help(msg: Message):
    text = ("Настройки:\n"
            "• /toggle_ready — переключить статус «готов к общению»\n"
            "• /set_city_filter <город|any> — фильтр по городу\n"
            "• /set_age_filter <min> <max> — фильтр по возрасту")
    await msg.answer(text)

@router.message(Command("toggle_ready"))
async def toggle_ready(msg: Message):
    async with SessionLocal() as session:  # type: AsyncSession
        user = await get_user_by_tg(session, msg.from_user.id)
        if not user:
            user = User(tg_id=msg.from_user.id, is_available=True)
            session.add(user)
        else:
            user.is_available = not bool(user.is_available)
        await session.commit()
        await session.refresh(user)
        status = "готов к общению" if user.is_available else "не беспокоить"
        await msg.answer(f"Статус обновлён: {status}")

@router.message(Command("set_city_filter"))
async def set_city_filter(msg: Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        return await msg.answer("Укажи город или 'any'. Пример: /set_city_filter Минск")
    value = parts[1].strip()
    async with SessionLocal() as session:
        prefs = await get_or_create_prefs(session, msg.from_user.id)
        prefs.city_filter = None if value.lower() in ("any", "любой") else value[:64]
        await session.commit()
    await msg.answer(f"Фильтр города: {'любой' if value.lower() in ('any','любой') else value}")

@router.message(Command("set_age_filter"))
async def set_age_filter(msg: Message):
    parts = msg.text.split()
    if len(parts) != 3:
        return await msg.answer("Формат: /set_age_filter <мин> <макс>. Пример: /set_age_filter 25 40")
    try:
        amin = int(parts[1]); amax = int(parts[2])
    except Exception:
        return await msg.answer("Возраст должен быть числами, пример: /set_age_filter 25 40")
    if amin < 16 or amax < 16 or amin > amax:
        return await msg.answer("Укажи корректный диапазон (например, 18 99).")
    async with SessionLocal() as session:
        prefs = await get_or_create_prefs(session, msg.from_user.id)
        prefs.age_min = amin; prefs.age_max = amax
        await session.commit()
    await msg.answer(f"Фильтр возраста: {amin}-{amax}")
