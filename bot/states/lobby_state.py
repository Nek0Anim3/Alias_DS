from bot.views.lobby.lobby_menu import LobbyMenuView

active_lobbys: dict[int, "LobbyMenuView"] = {}

def register_view(uid: int ,view: "LobbyMenuView"):
    if uid not in active_lobbys:
        active_lobbys[uid] = view
    print("LOBBY STATE: active_lobbys", active_lobbys)

def unregister_view(uid: int):
    if uid in active_lobbys:
        print("LOBBY STATE: Poped active lobby with UID, ", uid)
        active_lobbys.pop(uid)

def get_views(uid: int):
    return active_lobbys.get(uid, {})