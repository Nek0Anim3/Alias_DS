import discord
from discord.ext import commands

from bot.states.client_lobby_state import get_client_lobby
from bot.states.interactions_state import get_interaction
from bot.states.lobby_state import get_hostLobby_view
from bot.views.game.round_menu import RoundView
from bot.views.game.round_register import get_round_by_lobby_id, register_round_view
from debug.DebugLogger import DebugLogger

from game.game_manager import GameManager
from game.game_registry import get_game_manager
from asyncio import create_task


class GameUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #separated launch method
    async def _launch_round(self, game_manager: GameManager):
        roles = game_manager.player_roles
        for uid in game_manager.game_session.players:
            interaction = get_interaction(uid)
            if interaction is None:
                DebugLogger.Console(f"LAUNCH ROUND: no interact {uid}")
                continue
            view = RoundView(
                roles[uid],
                interaction,
                game_manager.game_session.current_word,
                game_manager.lobby_id
            )
            register_round_view(game_manager.lobby_id, uid, view)
            try:
                await interaction.edit_original_response(
                    content=view.menu_text,
                    view=view
                )
            except Exception as e:
                DebugLogger.Console(f"LAUNCH ROUND EXCEPT: {uid}: {e}")
        create_task(game_manager.start_timer(game_manager.game_session.time))


    #first start, милиці у коді xd
    @commands.Cog.listener()
    async def on_start_game_global(self, game_manager: GameManager):
        roles = game_manager.player_roles
        for uid in game_manager.game_session.players:
            if uid == game_manager.lobby_id:
                player_view = get_hostLobby_view(game_manager.lobby_id)
            else:
                player_view = get_client_lobby(uid)

            view_interaction = get_interaction(uid)
            if view_interaction is None:
                DebugLogger.Console(f"on_start_game_global: нет interaction для {uid}")
                continue
            view = RoundView(
                roles[uid],
                view_interaction,
                game_manager.game_session.current_word,
                game_manager.lobby_id
            )
            register_round_view(game_manager.lobby_id, uid, view)
            await player_view.goto_global(view=view, interaction=view_interaction)
            DebugLogger.Console(f"GAME START GAME ROLE: {roles[uid]}")

        create_task(game_manager.start_timer(game_manager.game_session.time))
        game_manager.round_index += 1 #to init break
        game_manager.pointer_index = (game_manager.pointer_index + 1) % len(game_manager.player_moves) #NEXT PLAYER MOVE after break.. KOSTILI 2: ENDLESS PYTHON WAR
        game_manager.current_leader = game_manager.player_moves[game_manager.pointer_index]
    #------------
    # @commands.Cog.listener()
    # async def on_start_round(self, game_manager: GameManager, view):

    @commands.Cog.listener()
    async def on_update_text(self, state: str, lobby_id: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        game_manager = get_game_manager(lobby_id)
        word = game_manager.game_session.get_random_word(game_manager.game_session.current_word)
        for roundview in lobbies:
            await roundview.update_text(word)
        if state == "yes":
            game_manager.game_session.update_player_scores(lobby_id, True)


    @commands.Cog.listener()
    async def on_update_timer(self, lobby_id: int, base_time: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        for lobby in lobbies:
            lobby.time = base_time
            await lobby.update_text()

    @commands.Cog.listener()
    async def on_button_event(self, interaction: discord.Interaction ,lobby_id: int, status: bool):
        game_manager = get_game_manager(lobby_id)
        game_manager.game_session.update_player_scores(interaction.user.id, status)

    @commands.Cog.listener()
    async def on_start_break(self, game_manager: GameManager, next_leader: int):

        from bot.views.game.break_menu import BreakView

        team_scores = game_manager.game_session.team_scores

        for uid in game_manager.game_session.players:
            interaction = get_interaction(uid)
            if interaction is None:
                DebugLogger.Console(f"GAME UPDATE (on_start_break): No interact. {uid}")
                continue

            view = BreakView(
                team_scores=team_scores,
                next_leader_uid=next_leader,
                lobby_id=game_manager.lobby_id,
                current_uid=uid  # каждый получает свой View
            )
            try:
                await interaction.edit_original_response(
                    content=view.menu_text,
                    view=view
                )
            except Exception as e:
                DebugLogger.Console(f"on_start_break error для {uid}: {e}")

    @commands.Cog.listener()
    async def on_continue_round(self, game_manager: GameManager):
        await self._launch_round(game_manager)


    # -- LEADER BOARD (p. s. https://preview.redd.it/diana-pragmata-art-by-me-v0-3n68umifdcxg1.jpeg?width=1080&crop=smart&auto=webp&s=eac4c6b63b35c309069c251eafed097ecc24bea4)

    async def _show_leaderboard(self, game_manager: GameManager, winner: str):
        from bot.views.game.leaderboard_menu import LeaderboardView
        team_scores = game_manager.game_session.team_scores
        #sort with lambda OH BOYYY
        sorted_scores = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)

        for uid in game_manager.game_session.players:
            interaction = get_interaction(uid)
            if interaction is None:
                continue
            view = LeaderboardView(
                sorted_scores=sorted_scores,
                winner=winner,
                lobby_id=game_manager.lobby_id
            )
            try:
                await interaction.edit_original_response(
                    content=view.menu_text,
                    view=view
                )
            except Exception as e:
                DebugLogger.Console(f"Show leaderboard err: {uid}: {e}")

def setup(bot: commands.Bot):
    bot.add_cog(GameUpdateCog(bot))
