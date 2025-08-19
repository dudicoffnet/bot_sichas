
import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.store import profiles, states, banned

router = Router()
ADMIN_IDS = {int(x) for x in (os.getenv("ADMINS") or "").replace(",", " ").split() if x.isdigit()}

def is_admin(uid:int)->bool:
    return uid in ADMIN_IDS

@router.message(Command("stats"))
async def stats(m: Message):
    if not is_admin(m.from_user.id):
        return
    await m.answer(f"Профилей: {len(profiles)}, состояний: {len(states)}, банов: {len(banned)}")

@router.message(Command("ban"))
async def ban(m: Message):
    if not is_admin(m.from_user.id):
        return
    parts = m.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await m.answer("/ban <user_id>")
        return
    uid = int(parts[1])
    banned[uid] = True
    await m.answer(f"Пользователь {uid} забанен.")

@router.message(Command("unban"))
async def unban(m: Message):
    if not is_admin(m.from_user.id):
        return
    parts = m.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await m.answer("/unban <user_id>")
        return
    uid = int(parts[1])
    banned.pop(uid, None)
    await m.answer(f"Пользователь {uid} разбанен.")
