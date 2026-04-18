from random import randint
import asyncio
from debug.DebugLogger import DebugLogger
from bot.connectBot import get_bot

class GameSession:
    def __init__(self, words: list, players, player_scores: dict, teams: dict, lobby_id: int):
        self.lobby_id = lobby_id
        self.words = words
        self.players = players
        self.teams = teams
        self.player_scores = player_scores
        self.current_word = self.get_random_word("")
        self.bot = get_bot()
        DebugLogger.Console(f"Game session inited: Teams debug list = {self.teams}")
#---------------------------------------------------

    def get_game_data(self):
        #zaglushka
        self.shuffle_players_list(self.teams)
        return self.current_word, self.teams



    def start_round(self):

        pass

    def update_player_scores(self, uid: int, status: bool):
        if self.player_scores[uid] == 0:
            return
        if status:
            self.player_scores[uid] += 1
        else:
            self.player_scores[uid] -= 1

    def get_random_word(self, word):
        rand_index = randint(0, len(self.words) - 1)
        if len(self.words) == 1:
            word = self.words[0]
            return word
        else:
            if self.words[rand_index] == word:
                self.words.pop(rand_index)
                rand_index += 1
                word = self.words[rand_index]
                DebugLogger.Console("SESSION: get_random_word: ", word)
                return word
            else:
                word = self.words[rand_index]
                DebugLogger.Console("SESSION: get_random_word: ", word)
                self.words.pop(rand_index)
                return word


    async def start_timer(self, base_time):
        while base_time > 0:
            DebugLogger.Console(f"TIMER: Left {base_time} seconds")
            self.bot.dispatch("update_timer", lobby_id=self.lobby_id, base_time=base_time)
            base_time -= 5
            await asyncio.sleep(5)
        self.bot.dispatch("update_timer", lobby_id=self.lobby_id, base_time=base_time)
        DebugLogger.Console(f"TIMER: END TIME")

#-----
    def shuffle_players_list(self, players: dict):
        test_list = [['Jake', 'Diana'], ['Bob', 'Mike'], ['Celestia', 'Andrew', 'Timurka'], ['Gekidzo', 'Bogdan', 'Kirill', 'Nicolay']]

        #player_list = list(players.values())

        transposed_list = list(map(list, zip(*test_list)))
        flat_list = [item for sublist in transposed_list for item in sublist]

        #FIX ADD LEADING 0 ZAGLUSHKA PNG

        #[[Jake, Alice, Cole], [Bob, Mike, Paimon], [Celestia, Andrew, Timurka], [Gekidzo, Bogdan, Kirill]
        #DebugLogger.Console(f"---SHUFFLE PLAYERS---\n player_list = bebebe \n Typeof player_list = {type(player_list)},\n Transposed_list = {transposed_list},\n flat = {flat_list}")
        DebugLogger.Console(f"FLAT LIST TEST: {flat_list}")



