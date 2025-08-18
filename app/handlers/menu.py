from aiogram import Router, F
from aiogram.types import Message
from app.keyboards.common import main_menu_kb
from app.services.db import get_profile, find_match_for, init_db
from app.config import settings

router = Router()

@router.message(F.text == "👤 Мой профиль")
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

@router.message(F.text == "🔍 Найти рядом")
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

@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: Message):
    await message.answer("Раздел настроек в разработке", reply_markup=main_menu_kb())

@router.message(F.text == "💖 Поддержать проект")
async def donate(message: Message):
    await message.answer("Спасибо за поддержку! Скоро добавим удобные способы доната.", reply_markup=main_menu_kb())

def register_menu_handlers(dp):
    dp.include_router(router)
