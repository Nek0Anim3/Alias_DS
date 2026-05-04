import discord
from discord.ext import commands
from bot.states.client_lobby_state import get_client_lobby
from bot.states.interactions_state import get_interaction
from bot.states.lobby_state import get_hostLobby_view
from bot.views.game.break_register import register_break_view, get_break_by_lobby_id
from bot.views.game.round_menu import RoundView
from bot.views.game.round_register import get_round_by_lobby_id, register_round_view, update_round_view
from debug.DebugLogger import DebugLogger
from game.game_manager import GameManager
from game.game_registry import get_game_manager
from asyncio import create_task


class GameUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_start_round(self, game_manager: GameManager):
        roles = game_manager.player_roles
        DebugLogger.Console(f"(START ROUND) PLAYER ROLES LIST: {game_manager.player_roles}")
        first_word = game_manager.game_session.get_random_word(game_manager.game_session.current_word)
        for uid in game_manager.game_session.players:
            interaction = get_interaction(uid)
            if interaction is None:
                DebugLogger.Console(f"LAUNCH ROUND: no interact {uid}")
                continue
            view = RoundView(
                roles[uid],
                interaction,
                first_word,
                game_manager.lobby_id
            )
            DebugLogger.Console(f"UPDATING ROUND VIEW TO {uid}, view: {view}. LobbyID: {game_manager.lobby_id}")
            update_round_view(game_manager.lobby_id, uid, view)
            break_views = get_break_by_lobby_id(game_manager.lobby_id)
            try:
                    await interaction.edit_original_response(
                        content=view.menu_text,
                        view=view
                    )
            except Exception as e:
                DebugLogger.Console(f"LAUNCH ROUND EXCEPT: {uid}: {e}")
            break_views[uid] = None
            game_manager.start_round()


    @commands.Cog.listener()
    async def on_start_game_global(self, game_manager: GameManager):
        roles = game_manager.player_roles

        first_word = game_manager.game_session.get_random_word(game_manager.game_session.current_word)
        for uid in game_manager.game_session.players:
            if uid == game_manager.lobby_id:
                player_view = get_hostLobby_view(game_manager.lobby_id)
            else:
                player_view = get_client_lobby(uid)

            view_interaction = get_interaction(uid)
            if view_interaction is None:
                DebugLogger.Console(f"on_start_game_global: no interact {uid}")
                continue
            view = RoundView(
                roles[uid],
                view_interaction,
                first_word,
                game_manager.lobby_id
            )
            register_round_view(game_manager.lobby_id, uid, view)
            await player_view.goto_global(view=view, interaction=view_interaction)
            DebugLogger.Console(f"GAME START GAME ROLE: {roles[uid]}")

        game_manager.round_index += 1
        create_task(game_manager.start_timer(game_manager.game_session.time))

        DebugLogger.Console(f"-------- START GAME GLOBAL INF --------\nRound INDEX: {game_manager.round_index}\nPointer: {game_manager.pointer_index}\nCurrent Leader: {game_manager.current_leader}")


    @commands.Cog.listener()
    async def on_update_text(self, state: str, lobby_id: int, uid: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        game_manager = get_game_manager(lobby_id)
        word = game_manager.game_session.get_random_word(game_manager.game_session.current_word)
        for roundview in lobbies:
            await roundview.update_text(word)
        if state == "yes":
            game_manager.game_session.update_player_scores(uid, True)
        else:
            game_manager.game_session.update_player_scores(uid, False)


    @commands.Cog.listener()
    async def on_update_timer(self, lobby_id: int, base_time: int):
        lobbies = get_round_by_lobby_id(lobby_id)
        for lobby in lobbies:
            lobby.time = base_time
            await lobby.update_text()

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
                current_uid=uid
            )
            register_break_view(game_manager.lobby_id, uid, view)
            try:
                await interaction.edit_original_response(
                    content=view.menu_text,
                    view=view
                )
            except Exception as e:
                DebugLogger.Console(f"GAME UPDATE (on_start_break): Exception {uid}: {e}")
        DebugLogger.Console(f"--------GAME BREAK: CHANGES---------\nRound idx: {game_manager.round_index}, Pointer: {game_manager.pointer_index}\nLeader: {game_manager.current_leader}\n Roles: {game_manager.player_roles}")

    @commands.Cog.listener()
    async def on_win_game(self, game_manager: GameManager):
        # await self._launch_round(game_manager)
        await self._show_leaderboard(game_manager)

    # -- LEADER BOARD (p. s. https://preview.redd.it/diana-pragmata-art-by-me-v0-3n68umifdcxg1.jpeg?width=1080&crop=smart&auto=webp&s=eac4c6b63b35c309069c251eafed097ecc24bea4)
    # -- One of my fav soundtracks Hunger and Hope - Between August and December
    async def _show_leaderboard(self, game_manager: GameManager):
        from bot.views.game.leaderboard_menu import LeaderboardView
        team_scores = game_manager.game_session.team_scores
        #sort with lambda OH BOYYY
        sorted_scores = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
        winner = sorted_scores[0][0]
        DebugLogger.Console(f"WINNER: {winner}")
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

    @commands.Cog.listener()
    async def on_exit_game(self, game_manager: GameManager):
        pass
def setup(bot: commands.Bot):
    bot.add_cog(GameUpdateCog(bot))
