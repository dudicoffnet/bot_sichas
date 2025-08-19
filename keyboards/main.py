
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
