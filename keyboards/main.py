
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
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
