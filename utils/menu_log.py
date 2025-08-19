
def _dbg_menu_log(prefix: str):
    try:
        import logging
        logging.getLogger("menu").info(prefix + " -> отправляю клавиатуру: ['🔍','📝','⚙️','💖','📍']")
    except Exception:
        pass
