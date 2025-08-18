from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    search = State()
    about = State()
    photo = State()
    location = State()
    confirm = State()
