from debug.DebugLogger import DebugLogger

registered_teams: dict[int, dict[str, list]] = {}

def register_team(lobby_id: int, team_name: str, players: list[int]):
    if registered_teams.get(lobby_id, None) is not None:
        if team_name in registered_teams[lobby_id]:
            return
        else:
            registered_teams[lobby_id].update({team_name:players})
            DebugLogger.Console("Added team " + team_name)
            DebugLogger.Console("All teams in lobby: ", registered_teams[lobby_id])
    else:
        registered_teams.update({lobby_id: {team_name: players}})
        DebugLogger.Console(f"Registered team {registered_teams}.")
    return

def join_team(lobby_id: int, team_name: str, player_id: int):
    if registered_teams.get(lobby_id, None) is not None:
        if player_id not in registered_teams[lobby_id][team_name]:
            registered_teams[lobby_id][team_name].append(player_id)
            DebugLogger.Console(registered_teams[lobby_id][team_name])


def unregister_team(lobby_id: int, team_name: str):
    if registered_teams.get(lobby_id, None) is not None:
        registered_teams[lobby_id].pop(team_name)
        DebugLogger.Console("Unregistered team " + team_name)

def clear_teams(lobby_id: int):
    if registered_teams.get(lobby_id, None) is not None:
        registered_teams.pop(lobby_id)
        DebugLogger.Console(f"Cleared lobby teams {lobby_id}")

def get_lobby_teams(lobby_id: int):
    if lobby_id in registered_teams:
        DebugLogger.Console(f"get_lobby_teams DEBUG: {registered_teams[lobby_id]}.")
        return registered_teams[lobby_id]
    else:
        return {}

def find_team_in_lobby(lobby_id: int, team_name: str):
    if registered_teams.get(lobby_id, None) is not None:
        if team_name in registered_teams[lobby_id]:
            DebugLogger.Console(f"FIND_TEAM DEBUG: FOUND TEAM {team_name}")
            return True
        return False
    else:
        return False
