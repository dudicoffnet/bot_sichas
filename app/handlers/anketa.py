from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.states.form import Form
from app.keyboards.common import gender_kb, search_target_kb, confirm_profile_kb, main_menu_kb, photo_skip_kb, location_kb
from app.services.db import save_profile, init_db
from app.config import settings

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await init_db()
    await state.clear()
    await message.answer("👋 Привет! Это бот знакомств «Сейчас».\n\nДавай создадим твою анкету. Как тебя зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("🎂 Сколько тебе лет? (числом)")
    await state.set_state(Form.age)

@router.message(Form.age)
async def form_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введи число, например 28")
    await state.update_data(age=int(message.text))
    await message.answer("🚻 Выбери свой пол:", reply_markup=gender_kb())
    await state.set_state(Form.gender)

@router.message(Form.gender)
async def form_gender(message: Message, state: FSMContext):
    if message.text not in ["Мужчина", "Женщина"]:
        return await message.answer("Выбери один из вариантов на клавиатуре")
    await state.update_data(gender=message.text)
    await message.answer("📍 Из какого ты города?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.city)

@router.message(Form.city)
async def form_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.strip())
    await message.answer("👫 Кого ты хочешь найти?", reply_markup=search_target_kb())
    await state.set_state(Form.search)

@router.message(Form.search)
async def form_search(message: Message, state: FSMContext):
    if message.text not in ["Мужчину", "Женщину", "Без разницы"]:
        return await message.answer("Выбери из предложенных вариантов")
    await state.update_data(search=message.text)
    await message.answer("✍️ Напиши пару слов о себе:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.about)

@router.message(Form.about)
async def form_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text.strip())
    await message.answer("📷 Пришли фото для профиля (одним фото) или нажми «Пропустить».", reply_markup=photo_skip_kb())
    await state.set_state(Form.photo)

@router.message(Form.photo, F.text == "Пропустить")
async def photo_skip(message: Message, state: FSMContext):
    await state.update_data(photo_file_id=None)
    await message.answer("📍 Отправь свою локацию (кнопкой) или нажми «Пропустить».", reply_markup=location_kb())
    await state.set_state(Form.location)

@router.message(Form.photo, F.photo)
async def photo_save(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=file_id)
    await message.answer("📍 Отправь свою локацию (кнопкой) или нажми «Пропустить».", reply_markup=location_kb())
    await state.set_state(Form.location)

@router.message(Form.location, F.text == "Пропустить")
async def location_skip(message: Message, state: FSMContext):
    data = await state.get_data()
    preview = (
        f"Проверь анкету:\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"🎂 Возраст: {data.get('age')}\n"
        f"🚻 Пол: {data.get('gender')}\n"
        f"📍 Город: {data.get('city')}\n"
        f"👫 Ищет: {data.get('search')}\n"
        f"✍️ О себе: {data.get('about')}\n"
        f"📷 Фото: {'есть' if data.get('photo_file_id') else 'нет'}\n"
        f"📍 Локация: не указана"
    )
    await message.answer(preview, reply_markup=confirm_profile_kb())
    await state.set_state(Form.confirm)

@router.message(Form.location, F.location)
async def location_save(message: Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    data = await state.get_data()
    preview = (
        f"Проверь анкету:\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"🎂 Возраст: {data.get('age')}\n"
        f"🚻 Пол: {data.get('gender')}\n"
        f"📍 Город: {data.get('city')}\n"
        f"👫 Ищет: {data.get('search')}\n"
        f"✍️ О себе: {data.get('about')}\n"
        f"📷 Фото: {'есть' if data.get('photo_file_id') else 'нет'}\n"
        f"📍 Локация: указана"
    )
    await message.answer(preview, reply_markup=confirm_profile_kb())
    await state.set_state(Form.confirm)

@router.callback_query(F.data == "confirm_profile")
async def confirm_profile(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profile = {
        "user_id": call.from_user.id,
        "name": data.get("name"),
        "age": data.get("age"),
        "gender": data.get("gender"),
        "city": data.get("city"),
        "search": data.get("search"),
        "about": data.get("about"),
        "photo_file_id": data.get("photo_file_id"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
    }
    await save_profile(profile)
    await state.clear()
    await call.message.answer("✅ Анкета сохранена!", reply_markup=main_menu_kb())
    await call.answer()

# Редактирование
@router.callback_query(F.data == "edit_name")
async def edit_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введи новое имя:")
    await state.set_state(Form.name)
    await call.answer()

@router.callback_query(F.data == "edit_age")
async def edit_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введи новый возраст (числом):")
    await state.set_state(Form.age)
    await call.answer()

@router.callback_query(F.data == "edit_gender")
async def edit_gender(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Выбери пол:", reply_markup=gender_kb())
    await state.set_state(Form.gender)
    await call.answer()

@router.callback_query(F.data == "edit_city")
async def edit_city(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введи город:")
    await state.set_state(Form.city)
    await call.answer()

@router.callback_query(F.data == "edit_search")
async def edit_search(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Кого хочешь найти?", reply_markup=search_target_kb())
    await state.set_state(Form.search)
    await call.answer()

@router.callback_query(F.data == "edit_about")
async def edit_about(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Напиши о себе:")
    await state.set_state(Form.about)
    await call.answer()

@router.callback_query(F.data == "edit_photo")
async def edit_photo(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Пришли новое фото или нажми «Пропустить».", reply_markup=photo_skip_kb())
    await state.set_state(Form.photo)
    await call.answer()

@router.callback_query(F.data == "edit_location")
async def edit_location(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Отправь локацию (кнопкой) или «Пропустить».", reply_markup=location_kb())
    await state.set_state(Form.location)
    await call.answer()

def register_anketa_handlers(dp):
    dp.include_router(router)
