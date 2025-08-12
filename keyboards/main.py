from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton("📝 Моя анкета"))
kb_main.add(KeyboardButton("🔔 Я свободен"))
kb_main.add(KeyboardButton("💖 Помочь проекту"))
