from bot.states.pack_view_state import get_pack_view
from bot.views.base import BaseView
import discord
class PackDescriptionMenu(BaseView):
    def __init__(self, pack_name: str, words: list, word_count: int):
        self.pack_name = pack_name
        self.words = words
        self.word_count = word_count
        self.menu_text = self._build_text()

        super().__init__(back_view=None)

    def _build_text(self):
        words_str = "\n".join(f"{p}" for p in self.words)
        return (
            f"Набір: {self.pack_name}\n"
            f"Слів: {len(self.words)}\n"
            f"{words_str}\n"
        )

    @discord.ui.button(label="Назад", style=discord.ButtonStyle.secondary, row=0)
    async def back_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.goto(interaction, get_pack_view(interaction.user.id))