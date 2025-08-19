
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb():
    # Всегда показываем все основные кнопки И кнопку геолокации в одном меню
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом"), KeyboardButton(text="📝 Моя анкета")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="💖 Помочь проекту")],
            [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]
        ],
        resize_keyboard=True
    )


# --- Extra keyboards (added by fix) ---
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Request location keyboard
geo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Поделиться локацией", request_location=True)],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Intent selection (basic set)
intents_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍷 Выпить бокал вина"), KeyboardButton(text="💬 Поболтать")],
        [KeyboardButton(text="🛍️ Пошопиться"), KeyboardButton(text="🚶 Прогулка")],
        [KeyboardButton(text="🎬 Кино"), KeyboardButton(text="🐕 Выгул собаки")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Visibility duration selection
visibility_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="15 мин"), KeyboardButton(text="1 час")],
        [KeyboardButton(text="24 часа"), KeyboardButton(text="выкл")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)


# Updated intents keyboard (15+ precise options)
intents_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍷 Выпить бокал вина"), KeyboardButton(text="💬 Поболтать")],
        [KeyboardButton(text="🛍️ Пошопиться вместе"), KeyboardButton(text="☕ Кофе")],
        [KeyboardButton(text="🚶 Прогулка"), KeyboardButton(text="🎬 Кино")],
        [KeyboardButton(text="🏛️ Музей"), KeyboardButton(text="💼 Коворкинг")],
        [KeyboardButton(text="🏋️ Спортзал"), KeyboardButton(text="🏃 Пробежка")],
        [KeyboardButton(text="🎲 Настолки"), KeyboardButton(text="📸 Фотопрогулка")],
        [KeyboardButton(text="🗣️ Языковой обмен"), KeyboardButton(text="📚 Учёба вместе")],
        [KeyboardButton(text="🧳 Путешествия/планы"), KeyboardButton(text="🐕 Выгул собаки")],
        [KeyboardButton(text="🎉 Вечеринка"), KeyboardButton(text="💻 Поработать за ноутбуком")],
        [KeyboardButton(text="🍽️ Поесть вместе"), KeyboardButton(text="⬅️ Назад в меню")],
    ],
    resize_keyboard=True
)
