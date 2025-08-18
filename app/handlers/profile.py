from aiogram import Router, F
from aiogram.types import Message, PhotoSize
from aiogram.fsm.context import FSMContext
from app.states.profile import ProfileFSM
from app.db.engine import SessionLocal, get_user_by_tg, touch_last_seen
from app.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(F.text == "📝 Моя анкета")
async def my_profile(msg: Message, state: FSMContext):
    await state.set_state(ProfileFSM.name)
    await msg.answer("Как тебя зовут? (имя)")

@router.message(ProfileFSM.name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip()[:64])
    await state.set_state(ProfileFSM.age)
    await msg.answer("Сколько тебе лет? (число)")

@router.message(ProfileFSM.age)
async def set_age(msg: Message, state: FSMContext):
    try:
        age = int(msg.text.strip())
    except Exception:
        return await msg.answer("Укажи возраст числом.")
    await state.update_data(age=age)
    await state.set_state(ProfileFSM.city)
    await msg.answer("Твой город?")

@router.message(ProfileFSM.city)
async def set_city(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text.strip()[:64])
    await state.set_state(ProfileFSM.interests)
    await msg.answer("Коротко об интересах (через запятую).")

@router.message(ProfileFSM.interests)
async def set_interests(msg: Message, state: FSMContext):
    await state.update_data(interests=msg.text.strip())
    await state.set_state(ProfileFSM.photo)
    await msg.answer("Хочешь добавить фото профиля? Пришли фото или напиши «пропустить».")

@router.message(ProfileFSM.photo, F.text.casefold() == "пропустить")
async def skip_photo(msg: Message, state: FSMContext):
    await _save_profile(msg.from_user.id, state, None)
    await state.clear()
    await msg.answer("Анкета сохранена ✅")

@router.message(ProfileFSM.photo, F.photo)
async def set_photo(msg: Message, state: FSMContext):
    photo_list: list[PhotoSize] = msg.photo
    file_id = photo_list[-1].file_id if photo_list else None
    await _save_profile(msg.from_user.id, state, file_id)
    await state.clear()
    await msg.answer("Анкета сохранена ✅")

async def _save_profile(tg_id: int, state: FSMContext, file_id: str | None):
    data = await state.get_data()
    async with SessionLocal() as session:  # type: AsyncSession
        user = await get_user_by_tg(session, tg_id)
        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
        user.name = data.get("name")
        user.age = data.get("age")
        user.city = data.get("city")
        user.interests = data.get("interests")
        if file_id:
            user.photo_file_id = file_id
        await session.commit()
        await touch_last_seen(session, tg_id)
