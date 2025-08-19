
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
import time

@dataclass
class UserProfile:
    user_id: int
    name: Optional[str] = None
    age: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[str] = None

@dataclass
class UserState:
    location: Optional[Tuple[float, float]] = None
    intent: Optional[str] = None
    visible_until: Optional[float] = None
    radius_km: int = 10

profiles: Dict[int, UserProfile] = {{}}
states: Dict[int, UserState] = {{}}
banned: Dict[int, bool] = {{}}
events: list = []

def get_state(uid:int) -> UserState:
    s = states.get(uid)
    if not s:
        s = UserState()
        states[uid] = s
    return s

def get_profile(uid:int) -> UserProfile:
    p = profiles.get(uid)
    if not p:
        p = UserProfile(user_id=uid)
        profiles[uid] = p
    return p

def log(event: str):
    events.append((time.time(), event))
