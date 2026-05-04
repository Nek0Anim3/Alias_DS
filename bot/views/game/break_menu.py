import discord
from bot.views.base import BaseView
from debug.DebugLogger import DebugLogger


class BreakView(BaseView):
    def __init__(self, team_scores: dict, next_leader_uid: int, lobby_id: int, current_uid: int):
        self.lobby_id = lobby_id
        self.next_leader_uid = next_leader_uid
        self.menu_text = self._build_text(team_scores)
        super().__init__(back_view=None)

        #Button on next move ply
        if current_uid == next_leader_uid:
            self.add_item(ContinueButton(lobby_id=lobby_id, team_scores=team_scores))


    def _build_text(self, team_scores: dict) -> str:
        scores_str = "\n".join(
            f"{team}: {score} очків"
            for team, score in team_scores.items()
        )
        DebugLogger.Console(f"BREAK, TEAM SCORES: {team_scores}")

        return (
            f"Кінець раунду!\n\n"
            f"Рахунок:\n{scores_str}\n\n"
            f"Очікуємо..."
        )



class ContinueButton(discord.ui.Button):
    def __init__(self, lobby_id: int, team_scores: dict):
        super().__init__(
            label="Продовжити ->",
            style=discord.ButtonStyle.success,
            row=0
        )
        self.team_scores = team_scores
        self.lobby_id = lobby_id

    async def callback(self, interaction: discord.Interaction):
        from bot.connectBot import get_bot
        from game.game_registry import get_game_manager

        bot = get_bot()
        win_value = 5
        for i in self.team_scores.values():
            if i >= win_value:
                bot.dispatch("win_game", game_manager=get_game_manager(self.lobby_id))
                await interaction.response.defer()
                return

        await interaction.response.edit_message(
            content="Починаємо раунд...",
            view=None
        )
        bot = get_bot()
        game_manager = get_game_manager(self.lobby_id)

        bot.dispatch("start_round", game_manager=game_manager)