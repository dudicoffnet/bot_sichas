
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from utils.store import get_state

router = Router()

def radius_kb():
    rows = [[KeyboardButton(text=f"{r} км")] for r in (2,5,10,25)]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@router.message(lambda m: (m.text or '').strip() in {'⚙️ Настройки','Настройки'})
async def settings_menu(m: Message):
    st = get_state(m.from_user.id)
    await m.answer(f"Текущий радиус: {st.radius_km} км. Выбери новый:", reply_markup=radius_kb())

@router.message(lambda m: (m.text or '').strip() in {'2 км','5 км','10 км','25 км'})
async def set_radius(m: Message):
    st = get_state(m.from_user.id)
    st.radius_km = int((m.text or '10 км').split()[0])
    await m.answer(f"Радиус поиска установлен: {st.radius_km} км.")
