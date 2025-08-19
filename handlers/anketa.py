from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.main import main_kb, intents_kb, radius_kb
from utils.store import get_state

router = Router()

class Anketa(StatesGroup):
    name = State()
    age = State()
    city = State()
    intents = State()
    radius = State()

@router.message(lambda m: (m.text or "").strip() in {"📝 Моя анкета"})
async def start_anketa(m: types.Message, state: FSMContext):
    await m.answer("Как тебя зовут?")
    await state.set_state(Anketa.name)

@router.message(Anketa.name)
async def anketa_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text.strip())
    await m.answer("Сколько тебе лет? (14–100)")
    await state.set_state(Anketa.age)

@router.message(Anketa.age)
async def anketa_age(m: types.Message, state: FSMContext):
    if not m.text.isdigit() or not (14 <= int(m.text) <= 100):
        return await m.answer("Введи число от 14 до 100.")
    await state.update_data(age=int(m.text))
    await m.answer("Из какого ты города?")
    await state.set_state(Anketa.city)

@router.message(Anketa.city)
async def anketa_city(m: types.Message, state: FSMContext):
    await state.update_data(city=m.text.strip())
    await m.answer("Выбери 1–3 цели встречи:", reply_markup=intents_kb)
    await state.set_state(Anketa.intents)

@router.message(Anketa.intents)
async def anketa_intents(m: types.Message, state: FSMContext):
    data = await state.get_data()
    intents = data.get("intents", [])
    if len(intents) >= 3 and m.text not in intents:
        return await m.answer("Уже выбрано 3 цели. Можно убрать одну в настройках.")
    intents.append(m.text)
    await state.update_data(intents=intents)
    if len(intents) >= 1:
        await m.answer("Теперь выбери радиус поиска:", reply_markup=radius_kb)
        await state.set_state(Anketa.radius)

@router.message(Anketa.radius)
async def anketa_radius(m: types.Message, state: FSMContext):
    if not m.text.replace(" км","").isdigit():
        return await m.answer("Выбери радиус из списка.")
    km = int(m.text.split()[0])
    await state.update_data(radius=km)
    data = await state.get_data()
    txt = (f"Анкета сохранена:\n"
           f"Имя: {data['name']}\n"
           f"Возраст: {data['age']}\n"
           f"Город: {data['city']}\n"
           f"Цели: {', '.join(data.get('intents', []))}\n"
           f"Радиус: {data['radius']} км")
    st = get_state(m.from_user.id)
    st.name, st.age, st.city, st.intents, st.radius_km = data['name'], data['age'], data['city'], data['intents'], data['radius']
    await m.answer(txt, reply_markup=main_kb())
    await state.clear()
