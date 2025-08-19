
import math, os
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from keyboards.main import geo_kb

router = Router()

OPTIONS = [
    "🍷 Выпить бокал вина","💬 Поболтать","🛍️ Пошопиться","🚶 Прогуляться","🎬 Кино",
    "☕ Кофе","🍽️ Поужинать","🎮 Поиграть","🎶 Концерт","⚽ Спорт",
    "🎨 Музей","🌳 Парк","📚 Почитать","✈️ Обсудить путешествия","❓ Другое"
]

def options_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in OPTIONS:
        kb.add(KeyboardButton(text=name))
    return kb

@router.message(lambda m: (m.text or "").strip() in {"🔍 Найти рядом","Найти рядом","Поиск рядом"})
async def search_entry(m: Message):
    await m.answer("Отправь геопозицию, чтобы я показал людей поблизости.", reply_markup=geo_kb())

@router.message(lambda m: m.location is not None)
async def got_location(m: Message):
    await m.answer("Геопозиция получена. Что хочешь сделать сейчас?", reply_markup=options_kb())
