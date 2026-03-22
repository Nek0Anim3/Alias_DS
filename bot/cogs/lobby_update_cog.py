import asyncio

import discord
from discord import slash_command
from discord.ext import commands


from bot.states.lobby_state import get_views
from db.lobbyHandle import findLobbyByCode
from db.userHandle import removePlayerfromDB


class LobbyUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_update_lobby(self, lobby):
        lobby_view = get_views(lobby['host'])
        playerCount = len(lobby['players'])
        players = lobby['player_names']
        print("LOBBY_UPDATE: Triggered custom event!!")
        await lobby_view.refreshLobby(playerCount, players)

    @commands.Cog.listener()
    async def on_destroy_lobby(self, code):
        from bot.states.client_lobby_state import get_client_lobby
        lobby = await findLobbyByCode(code)
        for player in lobby['players']:
            lobby_view = get_client_lobby(player)
            try:
                await asyncio.gather(lobby_view.exit_lobby(), removePlayerfromDB(player))
            except AttributeError:
                continue



def setup(bot):
    bot.add_cog(LobbyUpdateCog(bot))