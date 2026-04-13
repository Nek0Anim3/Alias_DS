#логика на обнову менюх, ужассс.
import discord
from discord.ext import commands

from bot.states.client_lobby_state import get_client_lobby
from bot.views.game.round_menu import RoundView
from bot.views.game.round_register import get_round_by_lobby_id
from debug.DebugLogger import DebugLogger
from game.game_session import GameSession


class GameUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_start_game_global(self, lobby):
        players = lobby['players']
        del players[0] #ain't that cool? Deletes HOST id from players list, because otherwise .get method just returns blank {} instead of LobbyClientView
        roundView = get_round_by_lobby_id(lobby['host'])
        DebugLogger.Console("GOT ROUND VIEW:", roundView)
        for player in players:

            DebugLogger.Console(f"Changing view for player: {player} to Round View -> {roundView}")
            view = get_client_lobby(player)
            # await view.goto_global(interaction=view.interaction, view=roundView[-1])
            await view.global_start_game()

    @commands.Cog.listener()
    async def on_update_text(self, message: discord.Message, lobby_id: int, session: GameSession):
        lobbies = get_round_by_lobby_id(lobby_id)
        next_word = session.get_random_word(lobbies[0].current_word)
        for lobby in lobbies:
            await lobby.update_text(next_word)
            DebugLogger.Console(f"UPDATE GAME: Changing text for lobby: {lobby}")


def setup(bot: commands.Bot):
    bot.add_cog(GameUpdateCog(bot))