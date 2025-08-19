from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ALIASES_SEARCH = {"🔍 Найти рядом","Найти рядом","Поиск","Поиск рядом","Поиск поблизости"}
ALIASES_PROFILE = {"📝 Моя анкета","Моя анкета","Анкета"}
ALIASES_SETTINGS = {"⚙️ Настройки","Настройки"}
ALIASES_DONATE = {"💖 Помочь проекту","Помочь проекту","Донат","Поддержать"}

def main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом")],
            [KeyboardButton(text="📝 Моя анкета"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="💖 Помочь проекту")]
        ],
        resize_keyboard=True
    )
