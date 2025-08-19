from aiogram import Router
from aiogram.types import Message
from keyboards.main import main_kb, geo_kb
from utils.store import get_state

router = Router()

@router.message(lambda m: (m.text or '').strip() in {'🔍 Найти рядом','Найти рядом','Поиск рядом','Поиск поблизости'})
async def search_entry(m: Message):
    await m.answer("Отправь геопозицию, чтобы я показал людей поблизости.", reply_markup=main_kb())

@router.message(lambda m: (m.text or '').strip() in {'📍 Отправить геолокацию','Отправить геолокацию','Геолокация'})
async def ask_geo(m: Message):
    await m.answer(
        "Чтобы отправить геопозицию: скрепка 📎 → Геопозиция → Отправить текущую.",
        reply_markup=main_kb()
    )

    await m.answer("Нажми кнопку ниже, чтобы отправить свою геопозицию.", reply_markup=main_kb())

@router.message(lambda m: m.location is not None)
async def got_location(m: Message):
    st = get_state(m.from_user.id)
    st.location = (m.location.latitude, m.location.longitude)
    await m.answer("Геопозиция получена. Выбери действие:", reply_markup=main_kb())
