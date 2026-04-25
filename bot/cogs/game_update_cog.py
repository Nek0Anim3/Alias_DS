from discord.ext import commands

from bot.states.client_lobby_state import get_client_lobby
from bot.states.interactions_state import get_interaction
from bot.states.lobby_state import get_hostLobby_view
from bot.views.game.round_menu import RoundView
from bot.views.game.round_register import get_round_by_lobby_id, register_round_view
from debug.DebugLogger import DebugLogger
from enums.Roles import RoleTypes
from game.game_manager import GameManager
from game.game_registry import get_game_manager


class GameUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_start_game_global(self, game_manager: GameManager):
        roles = game_manager.player_roles
        for uid in game_manager.game_session.players:
            if uid == game_manager.lobby_id:
                player_view = get_hostLobby_view(game_manager.lobby_id)
            else:
                player_view = get_client_lobby(uid)
            view_interaction = get_interaction(uid)
            view = RoundView(roles[uid], view_interaction, game_manager.game_session.current_word, game_manager.lobby_id)
            register_round_view(game_manager.lobby_id, uid, view)
            await player_view.goto_global(view=view, interaction=view_interaction)
            DebugLogger.Console(f"GAME START GAME ROLE: {roles[uid]}")
        await game_manager.game_session.start_timer(game_manager.game_session.time)

    @commands.Cog.listener()
    async def on_start_round(self, game_manager: GameManager, view):
        roles = game_manager.player_roles
        for uid in roles:
            if roles[uid] == RoleTypes.LEADER:
                pass



    @commands.Cog.listener()
    async def on_update_text(self, state: str, lobby_id: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        game_manager = get_game_manager(lobby_id)
        word = game_manager.game_session.get_random_word(game_manager.game_session.current_word)
        for roundview in lobbies:
            await roundview.update_text(word)


    @commands.Cog.listener()
    async def on_update_timer(self, lobby_id: int, base_time: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        for lobby in lobbies:
            lobby.time = base_time
            await lobby.update_text()


def setup(bot: commands.Bot):
    bot.add_cog(GameUpdateCog(bot))
