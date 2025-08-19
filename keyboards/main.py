from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню: 5 кнопок (каждая в своей строке)
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

# Отдельная клавиатура с настоящей кнопкой запроса гео
geo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Заглушки на будущее (если где-то импортируются)
intents_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]], resize_keyboard=True)
visibility_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]], resize_keyboard=True)
