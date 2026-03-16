import discord
from discord import slash_command
from discord.ext import commands

from bot.states.lobby_state import get_views
from db.lobbyHandle import findLobbyByCode


class LobbyUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_update_lobby(self, code):
        lobby_view = get_views(code)
        lobby = await findLobbyByCode(code)
        playerCount = len(lobby['players'])
        players = lobby['player_names']
        print("LOBBY_UPDATE: Triggered custom event!!")

        for uid, view in lobby_view.items():
            await view.refreshLobby(playerCount, players)



def setup(bot):
    bot.add_cog(LobbyUpdateCog(bot))