from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.config import get_settings
from app.db.engine import SessionLocal
from app.db.models import User, Ban
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = Router()
SET = get_settings()

def is_admin(user_id: int) -> bool:
    return user_id in SET.admins

@router.message(Command("admin"))
async def admin_menu(msg: Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Команда доступна только админам.")
    await msg.answer("/users — список пользователей\n/ban <tg_id> — бан\n/unban <tg_id> — разбан")

@router.message(Command("users"))
async def users_list(msg: Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Только для админов.")
    async with SessionLocal() as session:  # type: AsyncSession
        res = await session.execute(select(User).order_by(User.id.desc()).limit(50))
        users = res.scalars().all()
        if not users:
            return await msg.answer("Пользователей нет.")
        lines = [f"{u.id}) {u.tg_id} — {u.name or '-'}; {u.age or '-'}; {u.city or '-'}; banned={u.is_banned}" for u in users]
        await msg.answer("\n".join(lines))

@router.message(Command("ban"))
async def ban_user(msg: Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Только для админов.")
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("Использование: /ban <tg_id> [причина]")
    try:
        target = int(parts[1])
    except ValueError:
        return await msg.answer("tg_id должен быть числом.")
    reason = " ".join(parts[2:]) if len(parts) > 2 else None
    async with SessionLocal() as session:  # type: AsyncSession
        res = await session.execute(select(User).where(User.tg_id == target))
        u = res.scalar_one_or_none()
        if not u:
            return await msg.answer("Пользователь не найден.")
        u.is_banned = True
        session.add(Ban(tg_id=target, reason=reason, banned_by=msg.from_user.id))
        await session.commit()
    await msg.answer(f"Пользователь {target} забанен.")

@router.message(Command("unban"))
async def unban_user(msg: Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Только для админов.")
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("Использование: /unban <tg_id>")
    try:
        target = int(parts[1])
    except ValueError:
        return await msg.answer("tg_id должен быть числом.")
    async with SessionLocal() as session:  # type: AsyncSession
        res = await session.execute(select(User).where(User.tg_id == target))
        u = res.scalar_one_or_none()
        if not u:
            return await msg.answer("Пользователь не найден.")
        u.is_banned = False
        await session.commit()
    await msg.answer(f"Пользователь {target} разбанен.")
