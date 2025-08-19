from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом")],
            [KeyboardButton(text="📝 Моя анкета"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="💖 Помочь проекту")]
        ],
        resize_keyboard=True
    )


def geo_kb():
    # Кнопка запроса гео + кнопка возврата в меню. Без one_time_keyboard, чтобы клавиатура не пряталась.
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
            [KeyboardButton(text="⬅️ Назад в меню")]
        ],
        resize_keyboard=True
    )

def intents_kb():
    names = [
        "🍷 Выпить бокал вина","💬 Поболтать","🛍️ Пошопиться","🚶 Прогуляться","🎬 Кино",
        "☕ Кофе","🍽️ Поужинать","🎮 Поиграть","🎶 Концерт","⚽ Спорт",
        "🎨 Музей","🌳 Парк","📚 Почитать","✈️ Обсудить путешествия","❓ Другое"
    ]
    rows = [[KeyboardButton(text=name)] for name in names]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def visibility_kb():
    rows = [
        [KeyboardButton(text="30 минут"), KeyboardButton(text="1 час")],
        [KeyboardButton(text="3 часа"), KeyboardButton(text="24 часа")]
    ]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)
