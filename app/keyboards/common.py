from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом")],
            [KeyboardButton(text="👤 Мой профиль")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="💖 Поддержать проект")]
        ],
        resize_keyboard=True
    )

def gender_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужчина")],
            [KeyboardButton(text="Женщина")]
        ],
        resize_keyboard=True
    )

def search_target_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужчину")],
            [KeyboardButton(text="Женщину")],
            [KeyboardButton(text="Без разницы")]
        ],
        resize_keyboard=True
    )

def photo_skip_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )

def location_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить локацию", request_location=True)],
            [KeyboardButton(text="Пропустить")]
        ],
        resize_keyboard=True
    )

def confirm_profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_profile")],
            [InlineKeyboardButton(text="✏️ Редактировать имя", callback_data="edit_name")],
            [InlineKeyboardButton(text="✏️ Редактировать возраст", callback_data="edit_age")],
            [InlineKeyboardButton(text="✏️ Редактировать пол", callback_data="edit_gender")],
            [InlineKeyboardButton(text="✏️ Редактировать город", callback_data="edit_city")],
            [InlineKeyboardButton(text="✏️ Редактировать цель поиска", callback_data="edit_search")],
            [InlineKeyboardButton(text="✏️ Редактировать о себе", callback_data="edit_about")],
            [InlineKeyboardButton(text="✏️ Заменить фото", callback_data="edit_photo")],
            [InlineKeyboardButton(text="✏️ Изменить локацию", callback_data="edit_location")]
        ]
    )
