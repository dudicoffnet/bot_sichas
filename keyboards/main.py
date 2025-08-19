from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🔍 Найти рядом")],
        [KeyboardButton("📝 Моя анкета")],
        [KeyboardButton("⚙️ Настройки")],
        [KeyboardButton("💖 Помочь проекту")],
        [KeyboardButton("📍 Отправить геолокацию")]
    ],
    resize_keyboard=True
)

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📍 Радиус поиска")],
        [KeyboardButton("🎯 Цели встречи")],
        [KeyboardButton("⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

radius_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("1 км"), KeyboardButton("3 км")],
        [KeyboardButton("5 км"), KeyboardButton("10 км")],
        [KeyboardButton("⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

intents_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🍷 Выпить бокал вина"), KeyboardButton("💬 Поболтать")],
        [KeyboardButton("☕ Кофе"), KeyboardButton("🛍️ Пошопиться вместе")],
        [KeyboardButton("🚶 Прогулка"), KeyboardButton("🎬 Кино")],
        [KeyboardButton("🏛️ Музей"), KeyboardButton("💼 Коворкинг")],
        [KeyboardButton("🏋️ Спортзал"), KeyboardButton("🏃 Пробежка")],
        [KeyboardButton("🎲 Настолки"), KeyboardButton("📸 Фотопрогулка")],
        [KeyboardButton("🗣️ Языковой обмен"), KeyboardButton("📚 Учёба вместе")],
        [KeyboardButton("🧳 Путешествия/планы"), KeyboardButton("🐕 Выгул собаки")],
        [KeyboardButton("🎉 Вечеринка"), KeyboardButton("🍽️ Поесть вместе")],
        [KeyboardButton("⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

INTENT_SET = {
    "🍷 Выпить бокал вина","💬 Поболтать","☕ Кофе","🛍️ Пошопиться вместе","🚶 Прогулка","🎬 Кино",
    "🏛️ Музей","💼 Коворкинг","🏋️ Спортзал","🏃 Пробежка","🎲 Настолки","📸 Фотопрогулка",
    "🗣️ Языковой обмен","📚 Учёба вместе","🧳 Путешествия/планы","🐕 Выгул собаки",
    "🎉 Вечеринка","🍽️ Поесть вместе"
}
