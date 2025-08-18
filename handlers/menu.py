from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from app.keyboards.common import main_menu_kb
from app.services.db import get_profile, find_match_for, init_db
from app.config import settings
import os, re

router = Router()

def norm(text: str) -> str:
    t = re.sub(r"[\W_]+", " ", text, flags=re.UNICODE).strip().lower()
    return t

PROFILE_ALIASES = {"мой профиль", "profile", "profil"}
FIND_ALIASES = {"найти рядом", "найти собеседника", "find nearby", "find"}
SETTINGS_ALIASES = {"настройки", "settings"}
DONATE_ALIASES = {"поддержать проект", "донат", "support", "поддержать"}

@router.message(F.text.func(lambda t: norm(t) in PROFILE_ALIASES))
async def show_profile(message: Message):
    await init_db()
    profile = await get_profile(message.from_user.id)
    if not profile:
        return await message.answer("У тебя ещё нет анкеты. Напиши /start, чтобы создать её.")
    text = (
        f"👤 Имя: {profile.get('name')}\n"
        f"🎂 Возраст: {profile.get('age')}\n"
        f"🚻 Пол: {profile.get('gender')}\n"
        f"📍 Город: {profile.get('city')}\n"
        f"👫 Ищет: {profile.get('search')}\n"
        f"✍️ О себе: {profile.get('about')}\n"
        f"📷 Фото: {'есть' if profile.get('photo_file_id') else 'нет'}\n"
        f"📍 Локация: {'указана' if (profile.get('lat') is not None and profile.get('lon') is not None) else 'не указана'}"
    )
    if profile.get("photo_file_id"):
        await message.answer_photo(profile["photo_file_id"], caption=text, reply_markup=main_menu_kb())
    else:
        await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text.func(lambda t: norm(t) in FIND_ALIASES))
async def find_match(message: Message):
    await init_db()
    me = await get_profile(message.from_user.id)
    if not me:
        return await message.answer("Сначала создай анкету: /start")
    candidate = await find_match_for(message.from_user.id, me, settings.SEARCH_RADIUS_KM)
    if not candidate:
        return await message.answer("Пока никого не нашлось поблизости. Попробуй позже.", reply_markup=main_menu_kb())
    text = (
        f"Нашёл кандидата:\n\n"
        f"👤 {candidate.get('name')}, {candidate.get('age')}\n"
        f"🚻 {candidate.get('gender')}\n"
        f"📍 {candidate.get('city')}\n"
        f"✍️ {candidate.get('about')}"
    )
    if candidate.get("photo_file_id"):
        await message.answer_photo(candidate["photo_file_id"], caption=text, reply_markup=main_menu_kb())
    else:
        await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text.func(lambda t: norm(t) in SETTINGS_ALIASES))
async def settings_menu(message: Message):
    await message.answer("Раздел настроек в разработке", reply_markup=main_menu_kb())

@router.message(F.text.func(lambda t: norm(t) in DONATE_ALIASES))
async def donate(message: Message):
    msg = "Спасибо за поддержку!\n📲 Отсканируй QR или используй номер карты вручную."
    await message.answer(msg, reply_markup=main_menu_kb())
    qr_path = os.path.join("assets", "donate_qr.png")
    if os.path.exists(qr_path):
        await message.answer_photo(FSInputFile(qr_path), caption="QR для доната")
    # Можно дополнить номер карты текстом ниже, когда пришлёшь

@router.message(F.text == "/menu")
async def show_menu_cmd(message: Message):
    await message.answer("Меню:", reply_markup=main_menu_kb())

@router.message(F.text == "/reset")
async def reset_cmd(message: Message):
    await message.answer("Сброс анкеты: напиши /start, чтобы заполнить заново.", reply_markup=main_menu_kb())

def register_menu_handlers(dp):
    dp.include_router(router)
