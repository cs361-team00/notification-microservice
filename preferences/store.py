# persistence layer: replace with SQLite (see TEAM_SETUP.md for schema and steps)
# add imports you need (e.g. json, os, sqlite3, config)

_db_path = None  # TODO: read from os.environ.get("PREFERENCES_DB_PATH", "preferences.db")


def _conn():
    """Open SQLite connection, ensure table exists, return connection."""
    # TODO: connect to _db_path, execute CREATE TABLE IF NOT EXISTS (see TEAM_SETUP.md schema), return connection
    pass


def load_preferences(user_id: str) -> dict[str, bool]:
    # TODO: query row for user_id, get prefs_json
    # TODO: if no row, return {}
    # TODO: parse JSON, filter keys to config.SUPPORTED_CHANNELS, return dict[str, bool]
    return {}  # remove once implemented: no saved prefs = use defaults


def save_preferences(user_id: str, prefs: dict[str, bool]) -> None:
    # TODO: filter prefs to only keys in config.SUPPORTED_CHANNELS
    # TODO: serialize to JSON string
    # TODO: INSERT OR REPLACE into user_preferences (user_id, prefs_json)
    pass
