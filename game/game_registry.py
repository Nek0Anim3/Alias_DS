from debug.DebugLogger import DebugLogger
from game.game_session import GameSession
from game.game_manager import GameManager

active_sessions: dict[int, "GameSession"] = {}

def register_active_session(lobby_id: int, session: "GameSession"):
    if lobby_id not in active_sessions:
        active_sessions[lobby_id] = session
    DebugLogger.Console(f"GAME REGISTRY Registered session {lobby_id}.")

def remove_active_session(lobby_id: int):
    if lobby_id in active_sessions:
        active_sessions.pop(lobby_id)
    DebugLogger.Console(f"GAME REGISTRY Removed session {lobby_id}.")

def get_active_session(lobby_id: int):
    if lobby_id in active_sessions:
        DebugLogger.Console(f"GAME REGISTRY Sent session {lobby_id}.")
        return active_sessions[lobby_id]
    else:
        return None


active_gamemanagers: dict[int, "GameManager"] = {}

def register_game_manager(lobby_id: int, game_manager: "GameManager"):
    if lobby_id not in active_gamemanagers:
        active_gamemanagers[lobby_id] = game_manager
        DebugLogger.Console(f"GAME REGISTRY Registered Game Manager: {lobby_id}.")

def get_game_manager(lobby_id: int) -> "GameManager":
    if lobby_id in active_gamemanagers:
        return active_gamemanagers[lobby_id]
    else:
        return None

def remove_game_manager(lobby_id: int):
    if lobby_id in active_gamemanagers:
        del active_gamemanagers[lobby_id]
        DebugLogger.Console(f"GAME REGISTRY Removed Game Manager: {lobby_id}.")