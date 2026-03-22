from bot.views.lobby.lobby_player_menu import LobbyClientView

active_client_lobbys: dict[int, "LobbyClientView"] = {}

def register_client_lobby(uid: int ,view: "LobbyMenuView"):
    if uid not in active_client_lobbys:
        active_client_lobbys[uid] = view
    print("CLIENT LOBBY: Registered", active_client_lobbys)

def unregister_client_lobby(uid: int):
    if uid in active_client_lobbys:
        print("LOBBY STATE: Poped lobby with UID, ", uid)
        active_client_lobbys.pop(uid)

def get_client_lobby(uid: int):
    return active_client_lobbys.get(uid, {})