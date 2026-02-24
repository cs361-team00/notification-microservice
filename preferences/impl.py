# uses preferences/store for persistence; teammate adds SQLite in store.py
import config
from preferences import store


def _default_prefs() -> dict[str, bool]:
    return {ch: True for ch in config.SUPPORTED_CHANNELS}


def get_enabled_channels(user_id: str) -> list[str]:
    prefs = store.load_preferences(user_id) or _default_prefs()
    return [ch for ch in config.SUPPORTED_CHANNELS if prefs.get(ch, True)]


def get_preferences(user_id: str) -> dict[str, bool]:
    return store.load_preferences(user_id) or _default_prefs()


def update_preferences(user_id: str, prefs: dict[str, bool]) -> dict[str, bool]:
    allowed = {k: bool(v) for k, v in prefs.items() if k in config.SUPPORTED_CHANNELS}
    current = store.load_preferences(user_id) or _default_prefs()
    current = {**current, **allowed}
    store.save_preferences(user_id, current)
    return current
