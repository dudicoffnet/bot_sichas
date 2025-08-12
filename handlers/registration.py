from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from states.registration import Reg
from keyboards.main import kb_main
from data.db import save_user, set_free, get_matches

ACTIVITIES = [
    "☕ Кофе", "🚶 Прогулка", "🎬 Кино", "🛍️ Шопинг", "🏒 Каток",
    "🎳 Боулинг", "🏞️ За город", "🏛️ Музей/выставка", "🍕 Готовка",
    "🎲 Настольные игры", "🚴 Велопрогулка", "📸 Фото-прогулка",
    "🏊 Аквапарк", "🍷 Бар/вино", "🏃 Спорт/йога"
]

def register_handlers_registration(dp: Dispatcher):
    @dp.message_handler(lambda m: m.text == "📝 Моя анкета")
    async def anketa_start(m: types.Message, state: FSMContext):
        await m.answer("Как тебя зовут?")
        await Reg.name.set()

    @dp.message_handler(state=Reg.name)
    async def reg_name(m: types.Message, state: FSMContext):
        await state.update_data(name=m.text.strip())
        await m.answer("Сколько тебе лет? (числом)")
        await Reg.age.set()

    @dp.message_handler(state=Reg.age)
    async def reg_age(m: types.Message, state: FSMContext):
        if not m.text.isdigit():
            await m.answer("Напиши возраст числом.")
            return
        await state.update_data(age=int(m.text))
        await m.answer("Твой пол? (м/ж)")
        await Reg.gender.set()

    @dp.message_handler(state=Reg.gender)
    async def reg_gender(m: types.Message, state: FSMContext):
        gender = m.text.lower().strip()
        if gender not in ["м", "ж", "m", "f"]:
            await m.answer("Укажи м или ж.")
            return
        await state.update_data(gender="м" if gender in ["м", "m"] else "ж")
        await m.answer("Где ты сейчас? (район/адрес коротко)")
        await Reg.location.set()

    @dp.message_handler(state=Reg.location)
    async def reg_location(m: types.Message, state: FSMContext):
        await state.update_data(location=m.text.strip())
        text = "Выбери активности (через запятую):\n" + ", ".join(ACTIVITIES)
        await m.answer(text)
        await Reg.activities.set()

    @dp.message_handler(state=Reg.activities)
    async def reg_activities(m: types.Message, state: FSMContext):
        chosen = [x.strip() for x in m.text.split(",") if x.strip()]
        data = await state.get_data()
        save_user(
            user_id=m.from_user.id,
            name=data.get("name"),
            age=data.get("age"),
            gender=data.get("gender"),
            location=data.get("location"),
            activities=", ".join(chosen)
        )
        await state.finish()
        await m.answer("Анкета сохранена ✅", reply_markup=kb_main)

    @dp.message_handler(lambda m: m.text == "🔔 Я свободен")
    async def i_am_free(m: types.Message):
        set_free(m.from_user.id, True)
        await m.answer("Ок, пометил тебя как свободного. Напиши название активности, кого ищешь (например, «Кофе»).")

    @dp.message_handler(lambda m: m.text == "💖 Помочь проекту")
    async def donate(m: types.Message):
        await m.answer("Поддержать проект: переводы на карту BYN **** **** **** **** или по QR. Спасибо!")

    @dp.message_handler(lambda m: m.text and not m.text.startswith("/"))
    async def search_activity(m: types.Message):
        q = m.text.strip()
        matches = get_matches(q)
        if not matches:
            await m.answer("Пока нет совпадений. Попробуй другую активность или позже.")
            return
        lines = []
        for uid, name, age, gender, loc, acts in matches[:10]:
            lines.append(f"• {name or 'Без имени'}, {age or '?'} ({gender or '?'}) — {loc or 'Локация не указана'}\nАктивности: {acts}")
        await m.answer("Нашёл людей:\n" + "\n\n".join(lines))
