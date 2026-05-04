import discord
from bot.views.base import BaseView
from game.game_manager import GameManager


class LeaderboardView(BaseView):
    def __init__(self, sorted_scores: list[tuple[str, int]], winner: str, lobby_id: int, game_manager: GameManager):
        self.sorted_scores = sorted_scores
        self.game_manager = game_manager
        self.winner = winner
        self.lobby_id = lobby_id
        self.menu_text = self._build_text()
        super().__init__(back_view=None)

    def _build_text(self) -> str:
        lines = [f"Команда **{self.winner}** перемогла!\n", "---------------"]
        for i, (team, score) in enumerate(self.sorted_scores, start=1):
            medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}." #топ дизайн СНГ, how cool is that???
            lines.append(f"{medal} {team} — {score} очок")
        return "\n".join(lines)

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.connectBot import get_bot
        bot = get_bot()
        bot.dispatch("exit_game", game_manager=self.game_manager)