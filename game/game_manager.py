import asyncio

from debug.DebugLogger import DebugLogger
from enums.Roles import RoleTypes
from game.game_session import GameSession

#оркестратор ивентов связанных с игрой + каст ивентов на обновление ui.
class GameManager:
    def __init__(self, game_session: GameSession, lobby_id: int):
        from bot.connectBot import get_bot
        self.lobby_id = lobby_id
        self.game_session = game_session
        self.player_moves = game_session.shuffle_players_list(game_session.teams)
        self.pointer_index = 0
        self.current_leader = self.player_moves[self.pointer_index]
        DebugLogger.Console(f"GAME MANAGER INIT: self.player_moves[self.pointer_index] = {self.current_leader}")#совпадает с хостом, начинает первый
        self.player_roles = {}
        self.round_index = 0
        self.bot = get_bot()
        self.set_player_roles(self.game_session.players, self.current_leader)
        DebugLogger.Console(f"------- GAME MANAGER SESSION INF --------\nLobby ID: {self.lobby_id}\nCurrent Leader: {self.current_leader}\nPlayer Moves List: {self.player_moves}\nRound Index: {self.round_index}")

    def next_pointer(self):
        if self.pointer_index == len(self.player_moves) - 1:
            self.pointer_index = 0
        else:
            self.pointer_index += 1

    def start_round(self):
        if self.round_index % 2 == 0:
            # self.current_leader = self.player_moves[self.pointer_index]
            # self.set_player_roles(self.game_session.players, self.current_leader)
            self.bot.dispatch("start_round", game_manager=self)
            DebugLogger.Console(f"------- GAME MANAGER ROUND --------\nLobby ID: {self.lobby_id}\nCurrent Leader: {self.current_leader}\nPlayer Moves List: {self.player_moves}\nRound Index: {self.round_index}")
            DebugLogger.Console(f"GAME MANAGER ROUND INF: Player Moves: {self.player_moves}\n LENGTH: {len(self.player_moves)}")
            asyncio.create_task(self.start_timer(self.game_session.time))
            self.round_index += 1

    def start_break(self):
            self.next_pointer()
            next_leader = self.player_moves[self.pointer_index]
            DebugLogger.Console(f"------- GAME MANAGER BREAK --------\nLobby ID: {self.lobby_id}\nCurrent Leader: {self.current_leader}\nPlayer Moves List: {self.player_moves}\nRound Index: {self.round_index}")
            self.bot.dispatch("start_break", game_manager=self, next_leader=next_leader)
            self.round_index += 1
            self.current_leader = self.player_moves[self.pointer_index]
            self.set_player_roles(self.game_session.players, self.current_leader)


    def set_player_roles(self, players: list, current_leader: int):
        DebugLogger.Console(f"SET PLAYER ROLES: Retrieved NEXT LEADER: {current_leader}")
        for player in players:
            if player == current_leader:
                DebugLogger.Console(f"if player == current_leader: {player} setting role to LEADER")
                self.player_roles[player] = RoleTypes.LEADER
            else:
                DebugLogger.Console(f"ELSE PLAYER not equal: {player} setting to PLAYER")
                self.player_roles[player] = RoleTypes.PLAYER
        DebugLogger.Console(f"SET PLAYER ROLES: {self.player_roles}")



    async def start_timer(self, base_time):
        while base_time > 0:
            DebugLogger.Console(f"TIMER: Left {base_time} seconds")
            self.bot.dispatch("update_timer", lobby_id=self.lobby_id, base_time=base_time)
            base_time -= 5
            await asyncio.sleep(5)

        self.start_break()
