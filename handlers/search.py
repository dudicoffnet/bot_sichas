from aiogram import Router
from aiogram.types import Message
from keyboards.main import main_kb
from utils.store import get_state

router = Router()

@router.message(lambda m: (m.text or '').strip() in {'🔍 Найти рядом','Найти рядом','Поиск рядом','Поиск поблизости'})
async def search_entry(m: Message):
    await m.answer("Отправь геопозицию: скрепка 📎 → Геопозиция → Отправить текущую.", reply_markup=main_kb())

@router.message(lambda m: (m.text or "").strip() in {'📍 Отправить геолокацию','Отправить геолокацию'})
async def help_geo(m: Message):
    await m.answer("Скрепка 📎 → Геопозиция → Отправить текущую.", reply_markup=main_kb())

@router.message(lambda m: m.location is not None)
async def got_location(m: Message):
    st = get_state(m.from_user.id)
    st.location = (m.location.latitude, m.location.longitude)
    await m.answer("Геопозиция получена. Продолжаем.", reply_markup=main_kb())
