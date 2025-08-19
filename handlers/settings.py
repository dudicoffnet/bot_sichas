from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from keyboards.main import main_kb
from utils.store import get_state

router = Router()

def radius_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 км"), KeyboardButton(text="3 км")],
            [KeyboardButton(text="5 км"), KeyboardButton(text="10 км")],
            [KeyboardButton(text="⬅️ Назад в меню")]
        ],
        resize_keyboard=True
    )

@router.message(lambda m: (m.text or "").strip() in {"⚙️ Настройки", "Настройки"})
async def open_settings(m: Message):
    st = get_state(m.from_user.id)
    await m.answer(
        f"Текущий радиус: {st.radius_km} км. Выбери новый:",
        reply_markup=radius_kb()
    )

@router.message(lambda m: (m.text or "").strip() in {"1 км","3 км","5 км","10 км"})
async def set_radius(m: Message):
    st = get_state(m.from_user.id)
    st.radius_km = int(m.text.split()[0])
    await m.answer(
        f"Радиус поиска установлен: {st.radius_km} км.",
        reply_markup=main_kb()
    )
