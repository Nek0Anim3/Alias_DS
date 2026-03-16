from bot.views.base import BaseView

_states: dict[int, dict] = {}

def set_state(user_id: int, state: str, **data):
    _states[user_id] = {"state": state, "data": data}
    print("STATES: Set state", _states[user_id]["state"])
    print("STATES: Dict, ", _states)

def get_state(user_id: int) -> str | None:
    return _states.get(user_id, {}).get("state")

def get_data(user_id: int) -> dict:
    return _states.get(user_id, {}).get("data", {})

def update_data(user_id: int, **kwargs):
    if user_id in _states:
        _states[user_id]["data"].update(kwargs)
        print("STATES: Updated data ", _states[user_id]["data"])

def clear_state(user_id: int):
    print("STATES: Cleared state ", user_id)
    _states.pop(user_id, None)


class States:
    PACK_WAITING_NAME = "pack_waiting_name"
    PACK_WAITING_WORDS = "pack_waiting_words"
    CODE_LOBBY_WAIT = "code_lobby_wait"
    IN_GAME = "in_game"
    IN_GAME_BREAK = "in_game_break"