# stub: everyone gets all channels until preferences/impl is done
from config import SUPPORTED_CHANNELS


def get_enabled_channels(user_id: str) -> list[str]:
    return list(SUPPORTED_CHANNELS)
