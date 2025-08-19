# SINGLE ENTRYPOINT for aiogram v3 — fixed Bot init for 3.7+ (parse_mode via DefaultBotProperties)
import asyncio, logging, os
from os import path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties

logging.basicConfig(level=logging.INFO)

def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔍 Найти рядом")],
                  [KeyboardButton(text="📝 Моя анкета")],
                  [KeyboardButton(text="⚙️ Настройки")],
                  [KeyboardButton(text="💖 Помочь проекту")]],
        resize_keyboard=True)

settings_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📍 Радиус поиска")],
              [KeyboardButton(text="🎯 Цели встречи")],
              [KeyboardButton(text="⬅️ Назад в меню")]],
    resize_keyboard=True)

radius_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="1 км"), KeyboardButton(text="3 км")],
              [KeyboardButton(text="5 км"), KeyboardButton(text="10 км")],
              [KeyboardButton(text="⬅️ Назад в меню")]],
    resize_keyboard=True)

INTENT_SET = ["🍷 Выпить бокал вина","💬 Поболтать","☕ Кофе","🛍️ Пошопиться вместе","🚶 Прогулка","🎬 Кино",
              "🏛️ Музей","💼 Коворкинг","🏋️ Спортзал","🏃 Пробежка","🎲 Настолки","📸 Фотопрогулка",
              "🗣️ Языковой обмен","📚 Учёба вместе","🧳 Путешествия/планы","🐕 Выгул собаки",
              "🎉 Вечеринка","🍽️ Поесть вместе"]
rows = [[KeyboardButton(text=a), KeyboardButton(text=b)] for a,b in zip(INTENT_SET[0::2], INTENT_SET[1::2])]
rows.append([KeyboardButton(text="⬅️ Назад в меню")])
intents_kb = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

class Anketa(StatesGroup):
    name = State(); age = State(); city = State(); intents = State(); radius = State()

PROFILES = {}
router = Router()

@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message):
    splash = "assets/splash.png"
    if path.exists(splash):
        try:
            await message.answer_photo(FSInputFile(splash), caption="👋 Привет! Это бот знакомств «Сейчас».")
        except Exception:
            await message.answer("👋 Привет! Это бот знакомств «Сейчас».")
    else:
        await message.answer("👋 Привет! Это бот знакомств «Сейчас».")
    await message.answer("Меню:", reply_markup=main_kb())

@router.message(F.text == "⬅️ Назад в меню")
async def back_to_menu(message: Message):
    await message.answer("Меню:", reply_markup=main_kb())

@router.message(F.text == "📝 Моя анкета")
async def anketa_start(message: Message, state: FSMContext):
    await state.set_state(Anketa.name)
    await message.answer("Как тебя зовут?")

@router.message(Anketa.name)
async def anketa_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(Anketa.age)
    await message.answer("Сколько тебе лет? (14–100)")

@router.message(Anketa.age)
async def anketa_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or not (14 <= int(message.text) <= 100):
        return await message.answer("Введи число от 14 до 100.")
    await state.update_data(age=int(message.text))
    await state.set_state(Anketa.city)
    await message.answer("Из какого ты города?")

@router.message(Anketa.city)
async def anketa_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.strip())
    await state.set_state(Anketa.intents)
    await message.answer("Выбери 1–3 цели встречи:", reply_markup=intents_kb)

@router.message(Anketa.intents, F.text.in_(INTENT_SET))
async def anketa_intents(message: Message, state: FSMContext):
    data = await state.get_data()
    intents = data.get("intents", [])
    if message.text not in intents:
        intents.append(message.text)
    if len(intents) > 3:
        return await message.answer("Уже выбрано 3 цели. Перейди к радиусу или вернись в меню.")
    await state.update_data(intents=intents)
    if len(intents) >= 1:
        await state.set_state(Anketa.radius)
        await message.answer("Теперь выбери радиус поиска:", reply_markup=radius_kb)

@router.message(Anketa.radius, F.text.in_({"1 км","3 км","5 км","10 км"}))
async def anketa_radius(message: Message, state: FSMContext):
    km = int(message.text.split()[0])
    await state.update_data(radius=km)
    data = await state.get_data()
    PROFILES[message.from_user.id] = {"name": data["name"], "age": data["age"], "city": data["city"],
                                      "intents": data.get("intents", []), "radius": km}
    txt = (f"Анкета сохранена:\nИмя: {data['name']}\nВозраст: {data['age']}\nГород: {data['city']}\n"
           f"Цели: {', '.join(data.get('intents', []))}\nРадиус: {km} км")
    await message.answer(txt, reply_markup=main_kb())
    await state.clear()

@router.message(F.text == "⚙️ Настройки")
async def settings_open(message: Message):
    r = PROFILES.get(message.from_user.id, {}).get("radius", 5)
    await message.answer(f"Настройки. Текущий радиус: {r} км. Что меняем?", reply_markup=settings_kb)

@router.message(F.text == "📍 Радиус поиска")
async def settings_radius(message: Message):
    await message.answer("Выбери радиус:", reply_markup=radius_kb)

@router.message(F.text.in_({"1 км","3 км","5 км","10 км"}))
async def settings_radius_set(message: Message):
    uid = message.from_user.id
    prof = PROFILES.setdefault(uid, {})
    prof["radius"] = int(message.text.split()[0])
    await message.answer(f"Радиус установлен: {prof['radius']} км.", reply_markup=settings_kb)

@router.message(F.text == "🎯 Цели встречи")
async def settings_intents(message: Message):
    await message.answer("Выбери 1–3 цели:", reply_markup=intents_kb)

@router.message(F.text.in_(set(INTENT_SET)))
async def settings_intents_set(message: Message):
    uid = message.from_user.id
    prof = PROFILES.setdefault(uid, {})
    arr = set(prof.get("intents", []))
    if len(arr) >= 3 and message.text not in arr:
        return await message.answer("Уже выбрано 3 цели. Убери лишнее через меню и начни заново.")
    arr.add(message.text)
    prof["intents"] = list(arr)
    await message.answer(f"Цель сохранена: {message.text} ✓", reply_markup=intents_kb)

@router.message(F.text == "💖 Помочь проекту")
async def donate(message: Message):
    text = ("Спасибо за поддержку!\nЕсли откроется картинка — это QR. Если нет — напиши, пришлю вручную.")
    for candidate in ["assets/qr.png", "assets/donate_qr.png", "assets/QR.png"]:
        if os.path.exists(candidate):
            try:
                return await message.answer_photo(FSInputFile(candidate), caption=text)
            except Exception:
                break
    await message.answer(text)

@router.message(F.text == "🔍 Найти рядом")
async def nearby(message: Message):
    r = PROFILES.get(message.from_user.id, {}).get("radius", 5)
    await message.answer(f"Поиск рядом на радиусе {r} км (демо).", reply_markup=main_kb())

def _get_token() -> str:
    for key in ("BOT_TOKEN","TOKEN","TELEGRAM_TOKEN"):
        val = os.getenv(key)
        if val and val.strip():
            return val.strip()
    if os.path.exists("token.txt"):
        with open("token.txt","r",encoding="utf-8") as f:
            return f.read().strip()
    raise RuntimeError("Не найден токен. Установи BOT_TOKEN/TOKEN/TELEGRAM_TOKEN или положи token.txt.")

async def main():
    bot = Bot(token=_get_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except Exception:
        pass
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
