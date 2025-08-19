from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List
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

profiles: Dict[int, UserProfile] = dict()
states: Dict[int, UserState] = dict()
banned: Dict[int, bool] = dict()
events: List[Tuple[float, str]] = []

def get_state(uid:int) -> UserState:
    if uid not in states:
        states[uid] = UserState()
    return states[uid]

def get_profile(uid:int) -> UserProfile:
    if uid not in profiles:
        profiles[uid] = UserProfile(user_id=uid)
    return profiles[uid]

def log(event: str):
    events.append((time.time(), event))
