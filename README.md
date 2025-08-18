# Бот «Сейчас» (advanced) — фото, гео, умный матчинг, PostgreSQL (aiogram 3.x)

## Быстрый старт (локально / Railway)
1) Скопируйте `.env.example` в `.env` и заполните:
   - BOT_TOKEN=ваш_токен
   - DATABASE_URL=postgresql://user:pass@host:port/dbname   (Railway предоставляет переменную для подключения)
   - SEARCH_RADIUS_KM=10  (по умолчанию)
2) Установите зависимости: `pip install -r requirements.txt`
3) Запуск: `python start.py`

## Функции
- Пошаговая анкета (имя, возраст, пол, город, цель поиска, «о себе»)
- Загрузка **фото** профиля (или «Пропустить»)
- **Геолокация** (кнопка «📍 Отправить локацию» или «Пропустить»)
- **Умный матчинг**: пол, возраст ±3, город (если указан), **радиус** по координатам (по умолчанию 10 км)
- Хранение в **PostgreSQL**
- Меню: «🔍 Найти рядом», «👤 Мой профиль», «⚙️ Настройки», «💖 Поддержать проект»

## Структура
- start.py — входная точка
- app/config.py — настройки из .env
- app/bot.py — инициализация Bot/Dispatcher
- app/states/form.py — состояния FSM
- app/keyboards/common.py — клавиатуры
- app/services/db.py — PostgreSQL + матчинги
- app/handlers/anketa.py — анкета, фото, локация, подтверждение
- app/handlers/menu.py — профиль, поиск, пр.

## Деплой на Railway (кратко)
- Создайте PostgreSQL плагин и получите DATABASE_URL
- Добавьте переменные окружения BOT_TOKEN и DATABASE_URL
- Задеплойте репозиторий, точка входа `python start.py`
