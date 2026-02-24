import json
import os
import sqlite3
import config

_db_path = os.environ.get("PREFERENCES_DB_PATH", "preferences.db")

def _conn():
    conn = sqlite3.connect(_db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id TEXT PRIMARY KEY,
            prefs_json TEXT NOT NULL DEFAULT '{}'
        );
    ''')
    conn.commit()
    return conn

def load_preferences(user_id: str) -> dict[str, bool]:
    conn = _conn()
    try:
        cursor = conn.execute(
            "SELECT prefs_json FROM user_preferences WHERE user_id =?", 
            (str(user_id),)
            )
        row = cursor.fetchone()
        if row:
            raw_prefs = json.loads(row["prefs_json"])
            return {
                channel: is_enabled
                for channel, is_enabled in raw_prefs.items()
                if channel in config.SUPPORTED_CHANNELS
            }
        return()
    finally:
        conn.close

def save_preferences(user_id: str, prefs: dict[str, bool]) -> None:
    filtered_prefs = {
        channel: is_enabled
        for channel, is_enabled in prefs.items()
        if channel in config.SUPPORTED_CHANNELS
    }
    prefs_json = json.dumps(filtered_prefs)

    conn = _conn()
    try:
        conn.execute('''
            INSERT OR REPLACE INTO user_preferences (user_id, prefs_json)
            VALUES (?, ?)
        ''', (str(user_id), prefs_json))
        conn.commit()
    finally:
        conn.close()
