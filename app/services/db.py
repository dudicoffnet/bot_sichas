import math
import asyncpg
from typing import Optional, Dict, Any
from app.config import settings

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS profiles (
    user_id BIGINT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    city TEXT,
    search TEXT,
    about TEXT,
    photo_file_id TEXT,
    lat REAL,
    lon REAL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
"""

UPSERT_SQL = """
INSERT INTO profiles(user_id, name, age, gender, city, search, about, photo_file_id, lat, lon)
VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
ON CONFLICT(user_id) DO UPDATE SET
  name=EXCLUDED.name,
  age=EXCLUDED.age,
  gender=EXCLUDED.gender,
  city=EXCLUDED.city,
  search=EXCLUDED.search,
  about=EXCLUDED.about,
  photo_file_id=EXCLUDED.photo_file_id,
  lat=EXCLUDED.lat,
  lon=EXCLUDED.lon,
  updated_at=NOW();
"""

SELECT_SQL = "SELECT user_id, name, age, gender, city, search, about, photo_file_id, lat, lon FROM profiles WHERE user_id=$1"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    from math import radians, sin, cos, atan2, sqrt
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

async def get_pool():
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL не задан в окружении")
    return await asyncpg.create_pool(dsn=settings.DATABASE_URL, min_size=1, max_size=5)

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as con:
        await con.execute(CREATE_SQL)
    await pool.close()

async def save_profile(profile: Dict[str, Any]) -> None:
    pool = await get_pool()
    async with pool.acquire() as con:
        await con.execute(
            UPSERT_SQL,
            profile["user_id"],
            profile.get("name"),
            profile.get("age"),
            profile.get("gender"),
            profile.get("city"),
            profile.get("search"),
            profile.get("about"),
            profile.get("photo_file_id"),
            profile.get("lat"),
            profile.get("lon"),
        )
    await pool.close()

async def get_profile(user_id: int) -> Optional[Dict[str, Any]]:
    pool = await get_pool()
    async with pool.acquire() as con:
        row = await con.fetchrow(SELECT_SQL, user_id)
    await pool.close()
    if not row:
        return None
    return dict(row)

async def find_match_for(user_id: int, me: Dict[str, Any], radius_km: float):
    pool = await get_pool()
    query = """
        SELECT user_id, name, age, gender, city, search, about, photo_file_id, lat, lon
        FROM profiles
        WHERE user_id <> $1
          AND ($2::TEXT IS NULL OR gender = $2)
          AND ($3::TEXT IS NULL OR city = $3)
          AND ($4::INT IS NULL OR age BETWEEN $4 - 3 AND $4 + 3)
        ORDER BY updated_at DESC
        LIMIT 100
    """
    target_gender = None
    if me.get("search") in ("Мужчину", "Женщину"):
        target_gender = "Мужчина" if me["search"] == "Мужчину" else "Женщина"

    city = me.get("city") or None
    age = me.get("age") or None

    async with pool.acquire() as con:
        rows = await con.fetch(query, user_id, target_gender, city, age)
    await pool.close()

    me_lat, me_lon = me.get("lat"), me.get("lon")
    if me_lat is not None and me_lon is not None:
        filtered = []
        for r in rows:
            lat, lon = r["lat"], r["lon"]
            if lat is None or lon is None:
                continue
            d = haversine(me_lat, me_lon, lat, lon)
            if d <= radius_km:
                filtered.append((d, dict(r)))
        if filtered:
            filtered.sort(key=lambda x: x[0])
            return filtered[0][1]
    return dict(rows[0]) if rows else None
