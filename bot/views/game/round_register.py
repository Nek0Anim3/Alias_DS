from bot.views.game.round_menu import RoundView
from debug.DebugLogger import DebugLogger

active_rounds: dict[int, dict[int, "RoundView"]] = {} #dict[int, "RoundView"]

def register_round_view(lobby_id: int, uid: int, round_view: RoundView):
    if lobby_id not in active_rounds:
        active_rounds[lobby_id] = {uid: round_view}
    else:
        active_rounds[lobby_id].update({uid: round_view})
    DebugLogger.Console(f"ROUND REGISTER: Registered round with lobby_id {lobby_id}")

def update_round_view(lobby_id: int, uid: int, round_view: RoundView):
    active_rounds[lobby_id][uid] = round_view

def get_round_by_lobby_id(lobby_id: int):
    if lobby_id not in active_rounds:
        return None
    return active_rounds[lobby_id].values()

def clear_round_views(lobby_id: int):
    if lobby_id not in active_rounds:
        return
    else:
        active_rounds[lobby_id].clear()

def debug_round_listviews():
    DebugLogger.Console(f"DEBUG ROUND VIEW PRINT: {active_rounds}")