from bot.views.lobby.lobby_menu import LobbyMenuView
from debug.DebugLogger import DebugLogger

active_lobbys: dict[int, "LobbyMenuView"] = {}

def register_hostLobby_view(uid: int, view: "LobbyMenuView"):
    if uid not in active_lobbys:
        active_lobbys[uid] = view
    DebugLogger.Console("LOBBY STATE: active_lobbys", active_lobbys)

def unregister_hostLobby_view(uid: int):
    if uid in active_lobbys:
        DebugLogger.Console("LOBBY STATE: Poped active lobby with UID, ", uid)
        active_lobbys.pop(uid)

def get_hostLobby_view(uid: int) -> "LobbyMenuView":
    return active_lobbys.get(uid, {})
