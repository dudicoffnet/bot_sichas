from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.keyboards.main import ALIASES_SEARCH

router = Router()

OPTIONS = [
    "🍷 Выпить бокал вина",
    "☕ Поболтать за кофе",
    "🛍️ Пошопиться вместе",
    "🍔 Поесть фастфуд",
    "🎬 Сходить в кино",
    "🎶 На концерт",
    "⚽ Спорт",
    "🚶 Прогуляться",
    "📚 Почитать вместе",
    "🎮 Поиграть",
    "✈️ Обсудить путешествия",
    "🍕 Заказать пиццу",
    "🎨 В музей",
    "🌳 В парк",
    "❓ Другое"
]

def options_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in OPTIONS:
        kb.add(KeyboardButton(text=opt))
    return kb

@router.message(F.text.func(lambda t: t and t.strip() in ALIASES_SEARCH))
async def search_handler(message: Message):
    await message.answer("Что хочешь сделать сейчас?", reply_markup=options_kb())
