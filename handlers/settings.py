from aiogram import Router
from aiogram.types import Message
from keyboards.main import main_kb, settings_kb, radius_kb, intents_kb
from utils.store import get_state

router = Router()

@router.message(lambda m: (m.text or "").strip() in {"⚙️ Настройки", "Настройки"})
async def open_settings(m: Message):
    await m.answer("Что настраиваем?", reply_markup=settings_kb)

@router.message(lambda m: (m.text or "").strip() in {"📍 Радиус поиска"})
async def open_radius(m: Message):
    st = get_state(m.from_user.id)
    await m.answer(f"Текущий радиус: {getattr(st, 'radius_km', 5)} км. Выбери новый:", reply_markup=radius_kb)

@router.message(lambda m: (m.text or "").strip() in {"1 км","3 км","5 км","10 км"})
async def set_radius(m: Message):
    st = get_state(m.from_user.id)
    st.radius_km = int(m.text.split()[0])
    await m.answer(f"Радиус поиска установлен: {st.radius_km} км.", reply_markup=settings_kb)

@router.message(lambda m: (m.text or "").strip() in {"🎯 Цели встречи"})
async def open_intents(m: Message):
    await m.answer("Выбери 1–3 цели (можно по очереди).", reply_markup=intents_kb)

INTENT_SET = {
    "🍷 Выпить бокал вина","💬 Поболтать","☕ Кофе","🛍️ Пошопиться вместе","🚶 Прогулка","🎬 Кино",
    "🏛️ Музей","💼 Коворкинг","🏋️ Спортзал","🏃 Пробежка","🎲 Настолки","📸 Фотопрогулка",
    "🗣️ Языковой обмен","📚 Учёба вместе","🧳 Путешествия/планы","🐕 Выгул собаки",
    "🎉 Вечеринка","🍽️ Поесть вместе"
}

@router.message(lambda m: (m.text or "").strip() in INTENT_SET)
async def save_intent(m: Message):
    st = get_state(m.from_user.id)
    intents = set(getattr(st, "intents", []))
    if len(intents) >= 3 and m.text not in intents:
        return await m.answer("У тебя уже выбрано 3 цели. Удали одну или вернись назад.", reply_markup=intents_kb)
    intents.add(m.text.strip())
    st.intents = list(intents)
    await m.answer(f"Сохранено: {m.text} ✓", reply_markup=intents_kb)

@router.message(lambda m: (m.text or "").strip() in {"⬅️ Назад в меню"})
async def back_to_menu(m: Message):
    await m.answer("Меню:", reply_markup=main_kb())
