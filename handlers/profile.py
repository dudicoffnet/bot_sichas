from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.store import get_profile, log

router = Router()

class ProfileFSM(StatesGroup):
    name = State()
    age = State()
    city = State()
    interests = State()

@router.message(lambda m: (m.text or '').strip() in {'📝 Моя анкета','Моя анкета','Анкета'})
async def profile_start(m: Message, state: FSMContext):
    await m.answer("Как тебя зовут?")
    await state.set_state(ProfileFSM.name)

@router.message(ProfileFSM.name)
async def profile_name(m: Message, state: FSMContext):
    p = get_profile(m.from_user.id)
    p.name = (m.text or '').strip()
    await m.answer("Сколько тебе лет?")
    await state.set_state(ProfileFSM.age)

@router.message(ProfileFSM.age)
async def profile_age(m: Message, state: FSMContext):
    p = get_profile(m.from_user.id)
    p.age = (m.text or '').strip()
    await m.answer("В каком городе ты?")
    await state.set_state(ProfileFSM.city)

@router.message(ProfileFSM.city)
async def profile_city(m: Message, state: FSMContext):
    p = get_profile(m.from_user.id)
    p.city = (m.text or '').strip()
    await m.answer("Интересы (через запятую):")
    await state.set_state(ProfileFSM.interests)

@router.message(ProfileFSM.interests)
async def profile_interests(m: Message, state: FSMContext):
    p = get_profile(m.from_user.id)
    p.interests = (m.text or '').strip()
    await state.clear()
    await m.answer(f"Анкета сохранена!\nИмя: {p.name}\nВозраст: {p.age}\nГород: {p.city}\nИнтересы: {p.interests}")
    log(f"profile saved for {m.from_user.id}")
