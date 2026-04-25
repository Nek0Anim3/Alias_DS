from debug.DebugLogger import DebugLogger
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
        self.player_roles = game_session.set_player_roles(game_session.players, self.current_leader)
        self.round_index = 0
        self.bot = get_bot()
        DebugLogger.Console(f"------- GAME MANAGER SESSION INF --------\nLobby ID: {self.lobby_id}\nCurrent Leader: {self.current_leader}\nPlayer Moves List: {self.player_moves}\nRound Index: {self.round_index}")

    def start_round(self):
        if self.round_index % 2 == 0:
            try:
                self.pointer_index += 1
            except IndexError:
                self.pointer_index = 0
            self.current_leader = self.player_moves[self.pointer_index]
            self.game_session.set_player_roles(self.game_session.players, self.current_leader)
            self.game_session.start_round()
            self.bot.dispatch("start_round")
        else:

            self.bot.dispatch("start_break")

