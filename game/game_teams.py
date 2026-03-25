

registered_teams: dict[int, dict[str, list]] = {}

def register_team(lobby_id: int, team_name: str, players: list[int]):
    if registered_teams.get(lobby_id, None) is not None:
        if team_name in registered_teams[lobby_id]:
            return
    else:
        registered_teams[lobby_id] = {
            team_name: players
        }
    print(f"Registered team {registered_teams}.")
    return

def join_team(lobby_id: int, team_name: str, player_id: int):
    if registered_teams.get(lobby_id, None) is not None:
        if player_id not in registered_teams[lobby_id][team_name]:
            registered_teams[lobby_id][team_name].append(player_id)


