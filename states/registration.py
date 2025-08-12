from aiogram.dispatcher.filters.state import State, StatesGroup

class Reg(StatesGroup):
    name = State()
    age = State()
    gender = State()
    location = State()
    activities = State()
