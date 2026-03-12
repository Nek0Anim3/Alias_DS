from bot.views.lobby_menu import LobbyMenuView

active_lobbys: dict[int, dict[int, "LobbyMenuView"]] = {}

def register_view(code: int, user_id: int, view: "LobbyMenuView"):
    if code not in active_lobbys:
        active_lobbys[code] = {}
    active_lobbys[code][user_id] = view
    print("LOBBY STATE: active_lobbys", active_lobbys)

def unregister_view(code: int, user_id: int):
    if code in active_lobbys:
        print("LOBBY STATE: Poped active lobby with code, ", code)
        active_lobbys.pop(code)

def get_views(code: int):
    return active_lobbys.get(code, {})