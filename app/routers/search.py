from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(lambda m: m.text == "Найти рядом")
async def search_handler(message: Message):
    options = [
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
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(text=opt))
    await message.answer("Что хочешь сделать сейчас?", reply_markup=kb)
