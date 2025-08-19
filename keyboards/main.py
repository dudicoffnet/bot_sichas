from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню: 5 кнопок списком (каждая в своей строке)
def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти рядом")],
            [KeyboardButton(text="📝 Моя анкета")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="💖 Помочь проекту")],
            [KeyboardButton(text="📍 Отправить геолокацию")]  # без request_location — так меню не ломается в Desktop
        ],
        resize_keyboard=True
    )

# Клавиатура запроса геолокации (отправляется отдельным шагом)
geo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить геолокацию", request_location=True)],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Выбор целей (15+ позиций) — оставляем на будущее; при необходимости можно скрыть/показать
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
        [KeyboardButton(text="🍽️ Поесть вместе"), KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Выбор длительности видимости геолокации
visibility_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="15 мин"), KeyboardButton(text="1 час")],
        [KeyboardButton(text="24 часа"), KeyboardButton(text="выкл")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)
