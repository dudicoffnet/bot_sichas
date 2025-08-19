from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb():
    # 5 кнопок списком
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

# Отдельная клавиатура для реального запроса гео, если понадобится
geo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Заглушки (если где-то импортируются)
intents_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]], resize_keyboard=True)
visibility_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]], resize_keyboard=True)
