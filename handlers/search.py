import time
from aiogram import Router
from aiogram.types import Message
from keyboards.main import geo_kb, intents_kb, visibility_kb, main_kb
from utils.store import get_state, get_profile, profiles, states

router = Router()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    from math import radians, sin, cos, sqrt, atan2
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return R*c

@router.message(lambda m: (m.text or '').strip() in {'🔍 Найти рядом','Найти рядом','Поиск рядом','Поиск поблизости'})
async def search_entry(m: Message):
    await m.answer("Отправь геопозицию, чтобы я показал людей поблизости.", reply_markup=geo_kb)

@router.message(lambda m: m.location is not None)
async def got_location(m: Message):
    st = get_state(m.from_user.id)
    st.location = (m.location.latitude, m.location.longitude)
    await m.answer("Геопозиция получена. Выбери, что хочешь сделать сейчас:", reply_markup=geo_kb)

@router.message(lambda m: (m.text or '').strip() in {
    "🍷 Выпить бокал вина","💬 Поболтать","🛍️ Пошопиться","🚶 Прогуляться","🎬 Кино",
    "☕ Кофе","🍽️ Поужинать","🎮 Поиграть","🎶 Концерт","⚽ Спорт",
    "🎨 Музей","🌳 Парк","📚 Почитать","✈️ Обсудить путешествия","❓ Другое"
})
async def choose_intent(m: Message):
    st = get_state(m.from_user.id)
    st.intent = (m.text or '').strip()
    await m.answer("На какой срок включить видимость?", reply_markup=geo_kb)

@router.message(lambda m: (m.text or '').strip() in {"30 минут","1 час","3 часа","24 часа"})
async def set_visibility(m: Message):
    st = get_state(m.from_user.id)
    now = time.time()
    delta = {"30 минут":1800, "1 час":3600, "3 часа":10800, "24 часа":86400}[m.text.strip()]
    st.visible_until = now + delta
    await m.answer("Видимость включена. Ищу совпадения поблизости…")
    await show_matches(m)

async def show_matches(m: Message):
    st = get_state(m.from_user.id)
    me_loc = st.location
    if not me_loc or not st.intent:
        await m.answer("Нужны геопозиция и выбранная цель.")
        return
    now = time.time()
    results = []
    for uid, other in states.items():
        if uid == m.from_user.id:
            continue
        if not other.location or other.intent != st.intent:
            continue
        if not other.visible_until or other.visible_until < now:
            continue
        radius = st.radius_km
        dist = haversine(me_loc[0], me_loc[1], other.location[0], other.location[1])
        if dist <= radius:
            p = profiles.get(uid)
            if p:
                results.append((dist, f"• {p.name or 'Без имени'}, {p.age or '?'} — {p.city or ''} ({dist:.1f} км)"))
            else:
                results.append((dist, f"• Пользователь {uid} ({dist:.1f} км)"))
    if not results:
        await m.answer("Пока никого не нашли. Попробуй позже.")
        return
    results.sort(key=lambda x: x[0])
    await m.answer("Нашёл рядом:\n" + "\n".join([t for _, t in results[:10]]))


from keyboards.main import main_kb
@router.message(lambda m: (m.text or '').strip() in {'⬅️ Назад в меню','Назад','В меню'})
async def back_from_search(m: Message):
    await m.answer("Меню:", reply_markup=geo_kb)
