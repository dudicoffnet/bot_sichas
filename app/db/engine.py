from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from app.config import get_settings
from .models import Base, User, ActivityLog, Ban, SearchPref
from datetime import datetime, timezone

_settings = get_settings()
engine = create_async_engine(_settings.db_url, future=True, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_user_by_tg(session: AsyncSession, tg_id: int) -> User | None:
    res = await session.execute(select(User).where(User.tg_id == tg_id))
    return res.scalar_one_or_none()

async def touch_last_seen(session: AsyncSession, tg_id: int):
    user = await get_user_by_tg(session, tg_id)
    if user:
        user.last_seen = datetime.now(timezone.utc)
        await session.commit()

def is_online(user: User) -> bool:
    # Онлайном считаем тех, кто активничал за последние 5 минут
    if not user.last_seen:
        return False
    delta = datetime.now(timezone.utc) - user.last_seen
    return delta.total_seconds() <= 300

async def get_or_create_prefs(session: AsyncSession, tg_id: int) -> SearchPref:
    res = await session.execute(select(SearchPref).where(SearchPref.tg_id == tg_id))
    prefs = res.scalar_one_or_none()
    if prefs is None:
        prefs = SearchPref(tg_id=tg_id, age_min=None, age_max=None, city_filter=None)
        session.add(prefs)
        await session.commit()
        await session.refresh(prefs)
    return prefs
