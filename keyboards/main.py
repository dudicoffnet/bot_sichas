from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню: 5 кнопок списком
def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом")],
            [KeyboardButton(text="📝 Моя анкета")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="💖 Помочь проекту")],
            [KeyboardButton(text="📍 Отправить геолокацию")]
        ],
        resize_keyboard=True
    )

# Меню настроек
settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Радиус поиска")],
        [KeyboardButton(text="🎯 Цели встречи")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Радиус
radius_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 км"), KeyboardButton(text="3 км")],
        [KeyboardButton(text="5 км"), KeyboardButton(text="10 км")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# 15+ целей
intents_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍷 Выпить бокал вина"), KeyboardButton(text="💬 Поболтать")],
        [KeyboardButton(text="☕ Кофе"), KeyboardButton(text="🛍️ Пошопиться вместе")],
        [KeyboardButton(text="🚶 Прогулка"), KeyboardButton(text="🎬 Кино")],
        [KeyboardButton(text="🏛️ Музей"), KeyboardButton(text="💼 Коворкинг")],
        [KeyboardButton(text="🏋️ Спортзал"), KeyboardButton(text="🏃 Пробежка")],
        [KeyboardButton(text="🎲 Настолки"), KeyboardButton(text="📸 Фотопрогулка")],
        [KeyboardButton(text="🗣️ Языковой обмен"), KeyboardButton(text="📚 Учёба вместе")],
        [KeyboardButton(text="🧳 Путешествия/планы"), KeyboardButton(text="🐕 Выгул собаки")],
        [KeyboardButton(text="🎉 Вечеринка"), KeyboardButton(text="🍽️ Поесть вместе")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)
