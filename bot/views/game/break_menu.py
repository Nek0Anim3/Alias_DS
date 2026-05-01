import discord
from bot.views.base import BaseView


class BreakView(BaseView):
    def __init__(self, team_scores: dict, next_leader_uid: int, lobby_id: int, current_uid: int):
        self.lobby_id = lobby_id
        self.next_leader_uid = next_leader_uid
        self.menu_text = self._build_text(team_scores)
        super().__init__(back_view=None)

        #Button on next move ply
        if current_uid == next_leader_uid:
            self.add_item(ContinueButton(lobby_id=lobby_id))


    def _build_text(self, team_scores: dict) -> str:
        scores_str = "\n".join(
            f"{team}: {score} очків"
            for team, score in team_scores.items()
        )
        return (
            f"Кінець раунду!\n\n"
            f"Рахунок:\n{scores_str}\n\n"
            f"Очікуємо наступного ведучого..."
        )


class ContinueButton(discord.ui.Button):
    def __init__(self, lobby_id: int):
        super().__init__(
            label="Продовжити ->",
            style=discord.ButtonStyle.success,
            row=0
        )
        self.lobby_id = lobby_id

    async def callback(self, interaction: discord.Interaction):
        from bot.connectBot import get_bot
        from game.game_registry import get_game_manager

        await interaction.response.edit_message(
            content="Починаємо раунд...",
            view=None
        )
        bot = get_bot()
        game_manager = get_game_manager(self.lobby_id)

        bot.dispatch("continue_round", game_manager=game_manager)