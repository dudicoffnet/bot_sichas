from app.db.models import ActivityLog
from app.db.engine import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def log_action(actor_tg_id: int, action: str, target_tg_id: int | None = None, details: str | None = None):
    async with SessionLocal() as session:  # type: AsyncSession
        session.add(ActivityLog(actor_tg_id=actor_tg_id, action=action, target_tg_id=target_tg_id, details=details))
        await session.commit()
