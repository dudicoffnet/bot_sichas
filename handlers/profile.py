
from aiogram import Router
from aiogram.types import Message
from keyboards.main import main_kb
from utils.store import get_state

router = Router()

@router.message(lambda m: (m.text or "").strip() in {"📝 Моя анкета", "Моя анкета"})
async def show_profile(m: Message):
    st = get_state(m.from_user.id)
    # Безопасно достаём поля (могут быть пустыми)
    name = getattr(st, "name", "—")
    age = getattr(st, "age", "—")
    city = getattr(st, "city", "—")
    intents = getattr(st, "intents", [])
    radius = getattr(st, "radius_km", 5)

    intents_str = " / ".join(intents) if intents else "не выбраны"
    text = (
        "Твоя анкета:\n"
        f"• Имя: {name}\n"
        f"• Возраст: {age}\n"
        f"• Город: {city}\n"
        f"• Цели: {intents_str}\n"
        f"• Радиус поиска: {radius} км\n\n"
        "Чтобы изменить цели — зайди в ⚙️ Настройки → 🎯 Цели встречи."
    )
    await m.answer(text, reply_markup=main_kb())
