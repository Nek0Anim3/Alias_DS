import asyncio

from discord.ext import commands

from bot.states.client_lobby_state import get_client_lobby
from bot.states.lobby_state import get_hostLobby_view
from db.lobbyHandle import findLobbyByCode, getLobbyByID
from db.userHandle import removePlayerfromDB
from debug.DebugLogger import DebugLogger
from game.game_teams import get_lobby_teams, find_team_in_lobby, unregister_team


class LobbyUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_update_lobby(self, lobby):
        lobby_view = get_hostLobby_view(lobby['host'])
        playerCount = len(lobby['players'])
        players = lobby['player_names']
        DebugLogger.Console("LOBBY_UPDATE: Triggered custom event!!")
        await lobby_view.refresh_lobby(playerCount, players)

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

    @commands.Cog.listener()
    async def on_exit_client_lobby(self, lobby_id, team_name):
        DebugLogger.Console(f"LOBBY UPDATE: Client requested exit from lobby...")
        if find_team_in_lobby(lobby_id, team_name):
            unregister_team(lobby_id, team_name)
        lobby_host = get_hostLobby_view(lobby_id)
        await lobby_host.refresh_lobby(team_name="Не обрана")
        lobby = await getLobbyByID(lobby_id)

        for player in lobby['players']:
            lobby_client = get_client_lobby(player)
            try:
                await lobby_client.refresh_lobby(lobby_id)
            except AttributeError:
                DebugLogger.Console(f"EXIT CLIENT LOBBY: Not found lobby_view for ply..")
                continue


def setup(bot):
    bot.add_cog(LobbyUpdateCog(bot))