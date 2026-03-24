from random import randint


class GameSession:
    def __init__(self, words: list, players, player_scores: dict):
        self.words = words
        self.players = players
        self.player_scores = player_scores
        self.current_word = self.get_random_word("")
    def get_game_data(self):
        return self.players, self.current_word

    def start_round(self):
        pass
    #def update_game_data

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
                print("SESSION: get_random_word: ", word)
                return word
            else:
                word = self.words[rand_index]
                print("SESSION: get_random_word: ", word)
                self.words.pop(rand_index)
                return word


    async def start_timer(self):
        pass