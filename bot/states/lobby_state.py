from bot.views.lobby.lobby_menu import LobbyMenuView

active_lobbys: dict[int, dict[int, "LobbyMenuView"]] = {}
lobby_save: dict[int, "LobbyMenuView"] = {}

def register_view(code: int, uid: int ,view: "LobbyMenuView"):
    if code not in active_lobbys:
        active_lobbys[code] = {}
    active_lobbys[code][uid] = view
    print("LOBBY STATE: active_lobbys", active_lobbys)

def unregister_view(code: int):
    if code in active_lobbys:
        print("LOBBY STATE: Poped active lobby with code, ", code)
        active_lobbys.pop(code)

def get_views(code: int):
    return active_lobbys.get(code, {})

def save_lobby_state(uid: int, view: "LobbyMenuView"):
    if uid not in lobby_save:
        lobby_save[uid] = view
        print("LOBBY STATE: Saved lobby with uid, ", uid)

def pop_lobby_state(uid: int):
    if uid in lobby_save:
        lobby_save.pop(uid)
    print("LOBBY STATE: Popped lobby with uid, ", uid)

def get_lobby_state(uid: int):
    if uid in lobby_save:
        return lobby_save[uid]
    else:
        return None