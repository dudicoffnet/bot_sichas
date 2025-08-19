from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class Anketa(StatesGroup):
    name = State()
    age = State()
    city = State()
    photo = State()
    goal = State()
    radius = State()

@router.message(lambda m: m.text == "📝 Заполнить анкету")
async def start_anketa(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(Anketa.name)

@router.message(Anketa.name)
async def anketa_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(Anketa.age)

@router.message(Anketa.age)
async def anketa_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Укажите ваш город:")
    await state.set_state(Anketa.city)

@router.message(Anketa.city)
async def anketa_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Загрузите вашу фотографию:")
    await state.set_state(Anketa.photo)

@router.message(Anketa.photo)
async def anketa_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото.")
        return
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("Какая цель вашего знакомства?")
    await state.set_state(Anketa.goal)

@router.message(Anketa.goal)
async def anketa_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("Укажите радиус поиска (в км):")
    await state.set_state(Anketa.radius)

@router.message(Anketa.radius)
async def anketa_radius(message: types.Message, state: FSMContext):
    await state.update_data(radius=message.text)
    data = await state.get_data()
    await message.answer(
        f"Анкета заполнена!\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Город: {data['city']}\n"
        f"Цель: {data['goal']}\n"
        f"Радиус: {data['radius']} км"
    )
    await state.clear()
