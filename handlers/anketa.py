from aiogram import Router
from aiogram.types import Message
from keyboards.main import main_kb
from utils.store import get_state

router = Router()

def _set_step(user_id: int, step: str | None):
    st = get_state(user_id)
    st.filling_step = step

def _get_step(user_id: int):
    st = get_state(user_id)
    return getattr(st, "filling_step", None)

# Запуск анкеты
@router.message(lambda m: (m.text or "").strip() in {"/anketa", "✍️ Заполнить анкету", "Заполнить анкету"})
async def anketa_start(m: Message):
    _set_step(m.from_user.id, "name")
    await m.answer("Как тебя зовут? (введи имя текстом)", reply_markup=main_kb())

# Если пользователь нажимает «Моя анкета», а данных ещё нет — стартуем сбор
@router.message(lambda m: (m.text or "").strip() in {"📝 Моя анкета", "Моя анкета"})
async def maybe_show_or_fill(m: Message):
    st = get_state(m.from_user.id)
    if not getattr(st, "name", None) or not getattr(st, "age", None) or not getattr(st, "city", None):
        return await anketa_start(m)
    # иначе просто покажем, как у тебя сделано в profile.py
    # тут ничего не делаем: отработает существующий обработчик профиля

@router.message(lambda m: _get_step(m.from_user.id) == "name")
async def step_name(m: Message):
    st = get_state(m.from_user.id)
    st.name = (m.text or "").strip()
    _set_step(m.from_user.id, "age")
    await m.answer("Сколько тебе лет? (только число)")

@router.message(lambda m: _get_step(m.from_user.id) == "age")
async def step_age(m: Message):
    txt = (m.text or "").strip()
    if not txt.isdigit():
        return await m.answer("Нужна цифра, например 27.")
    st = get_state(m.from_user.id)
    st.age = int(txt)
    _set_step(m.from_user.id, "city")
    await m.answer("Из какого ты города?")

@router.message(lambda m: _get_step(m.from_user.id) == "city")
async def step_city(m: Message):
    st = get_state(m.from_user.id)
    st.city = (m.text or "").strip()
    _set_step(m.from_user.id, "photo_optional")
    await m.answer("Пришли фото (как сообщение с фото) или напиши «пропустить».")

@router.message(lambda m: _get_step(m.from_user.id) == "photo_optional" and m.photo)
async def step_photo(m: Message):
    st = get_state(m.from_user.id)
    st.photo_id = m.photo[-1].file_id
    _set_step(m.from_user.id, None)
    await _finish(m)

@router.message(lambda m: _get_step(m.from_user.id) == "photo_optional")
async def step_photo_skip(m: Message):
    if (m.text or "").strip().lower() not in {"пропустить", "skip"}:
        return await m.answer("Если не хочешь добавлять фото — напиши «пропустить».")
    _set_step(m.from_user.id, None)
    await _finish(m)

async def _finish(m: Message):
    st = get_state(m.from_user.id)
    name = getattr(st, "name", "—")
    age = getattr(st, "age", "—")
    city = getattr(st, "city", "—")
    intents = getattr(st, "intents", [])
    intents_str = " / ".join(intents) if intents else "не выбраны"
    txt = (
        "Анкета сохранена ✅\n\n"
        f"• Имя: {name}\n"
        f"• Возраст: {age}\n"
        f"• Город: {city}\n"
        f"• Цели: {intents_str}\n\n"
        "Цели и радиус можно задать в ⚙️ Настройки."
    )
    await m.answer(txt, reply_markup=main_kb())
