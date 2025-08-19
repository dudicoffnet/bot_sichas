from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    splash = FSInputFile("assets/splash.png")
    await message.answer_photo(splash,
        caption=(
            "Приглашаю Вас в новый формат встреч «Здесь и сейчас» — онлайн, без договоренностей.\n"
            "Запуск новой платформы. Далее будет приложение. Удачи!"
        )
    )
    kb = [
        [types.KeyboardButton(text="📅 Найти встречу")],
        [types.KeyboardButton(text="📝 Заполнить анкету")],
        [types.KeyboardButton(text="💖 Помочь проекту")],
        [types.KeyboardButton(text="ℹ️ О проекте")],
        [types.KeyboardButton(text="⚙️ Настройки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите действие:", reply_markup=keyboard)
