from bot.views.game.break_menu import BreakView
from debug.DebugLogger import DebugLogger

active_rounds: dict[int, dict[int, "BreakView"]] = {} #dict[int, "BreakView"]

def register_break_view(lobby_id: int, uid: int, break_view: BreakView):
    if lobby_id not in active_rounds:
        active_rounds[lobby_id] = {uid: break_view}
    else:
        active_rounds[lobby_id].update({uid: break_view})
    DebugLogger.Console(f"Break: Registered break with lobby_id {lobby_id}")

def update_break_view(lobby_id: int, uid: int, break_view: BreakView):
    active_rounds[lobby_id][uid] = break_view

def get_break_by_lobby_id(lobby_id: int) -> dict[int, BreakView]:
    if lobby_id not in active_rounds:
        return None
    return active_rounds[lobby_id]

def clear_break_views(lobby_id: int):
    if lobby_id not in active_rounds:
        return
    else:
        active_rounds[lobby_id].clear()

def debug_round_listviews():
    DebugLogger.Console(f"DEBUG Break Views PRINT: {active_rounds}")
