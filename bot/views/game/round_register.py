from bot.views.game.round_menu import RoundView
from debug.DebugLogger import DebugLogger

active_rounds: dict[int, list["RoundView"]] = {} #dict[int, "RoundView"]

def register_round_view(lobby_id: int, uid: int, round_view: RoundView):
    if lobby_id not in active_rounds:
        active_rounds[lobby_id] = [round_view]
        DebugLogger.Console(f"ROUND REGISTER: Registered round with lobby_id {lobby_id}")
    else:
        active_rounds[lobby_id].append({uid: round_view})
        DebugLogger.Console()

def get_round_by_lobby_id(lobby_id: int):
    if lobby_id not in active_rounds:
        return None
    return active_rounds[lobby_id]

def debug_round_listviews():
    DebugLogger.Console(f"DEBUG ROUND VIEW PRINT: {active_rounds}")
