from aiogram.fsm.state import State, StatesGroup

class ProfileFSM(StatesGroup):
    name = State()
    age = State()
    city = State()
    interests = State()
    photo = State()  # optional
