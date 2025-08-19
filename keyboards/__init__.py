# Безопасный экспорт: main_kb всегда, остальные — если присутствуют
from .main import main_kb
try:
    from .main import settings_kb, radius_kb, intents_kb
except Exception:
    pass
