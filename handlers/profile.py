
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

class Profile(StatesGroup):
    name = State()
    age = State()
    city = State()
    interests = State()

@router.message(lambda m: (m.text or '').strip() in {'📝 Моя анкета','Моя анкета','Анкета'})
async def profile_start(m: Message, state: FSMContext):
    await m.answer("Как тебя зовут?")
    await state.set_state(Profile.name)

@router.message(Profile.name)
async def profile_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text.strip())
    await m.answer("Сколько тебе лет?")
    await state.set_state(Profile.age)

@router.message(Profile.age)
async def profile_age(m: Message, state: FSMContext):
    await state.update_data(age=m.text.strip())
    await m.answer("В каком городе ты?")
    await state.set_state(Profile.city)

@router.message(Profile.city)
async def profile_city(m: Message, state: FSMContext):
    await state.update_data(city=m.text.strip())
    await m.answer("Интересы (через запятую):")
    await state.set_state(Profile.interests)

@router.message(Profile.interests)
async def profile_done(m: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await m.answer(f"Анкета сохранена:\nИмя: {data.get('name')}\nВозраст: {data.get('age')}\nГород: {data.get('city')}\nИнтересы: {m.text.strip()}")
