# Teammate: implement get_enabled_channels(user_id) -> list of channel names from DB.
# Use a flexible schema (e.g. JSON per channel) so new channels don't need migrations.
# Swap to this in orchestrator by importing preferences.impl instead of preferences_stub.


def get_enabled_channels(user_id: str) -> list[str]:
    raise NotImplementedError("Implement DB-backed get_enabled_channels in this file.")
