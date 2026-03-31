#логика на обнову менюх, ужассс.
import discord
from discord.ext import commands

from db.lobbyHandle import getLobbyByID


class GameUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_start_game_global(self, message: discord.Message, lobby_id: int, ):
        lobby = await getLobbyByID(lobby_id)
        players = lobby['players']
        pass

    @commands.Cog.listener()
    async def on_ui_game_update(self, message: discord.Message, lobby_id: int):
        if message.author.bot:
            return


def setup(bot: commands.Bot):
    bot.add_cog(GameUpdateCog(bot))