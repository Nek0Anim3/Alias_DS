import discord

from bot.states.pack_view_state import get_pack_view
from bot.views.base import BaseView
from db.packs import removePack
from debug.DebugLogger import DebugLogger


class PackDescriptionMenu(BaseView):
    def __init__(self, pack_name: str, words: list, word_count: int):
        self.pack_name = pack_name
        self.words = words
        self.word_count = word_count
        self.menu_text = self._build_text()

        super().__init__(back_view=None)

    def _build_text(self):
        #Hardcode limits to message 2000 characters
        words_length = 0
        words_str = ""
        for word in self.words:
            DebugLogger.Console(f"{word}")
            if words_length >= 1900:
                break
            words_str = "\n".join(f"{word}")
            words_length += len(words_str)

        return (
            f"Набір: {self.pack_name}\n"
            f"Слів: {len(self.words)}\n"
            f"{words_str}\n"
            f".... | Показано (60) з {len(self.words)}\n"
        )

    @discord.ui.button(label="Видалити", style=discord.ButtonStyle.danger, row=0)
    async def remove_pack(self, button: discord.ui.Button, interaction: discord.Interaction):
        await removePack(self.pack_name, interaction.user.id)

        from bot.states.pack_view_state import unregister_pack_view
        from bot.views.packs.packs_menu import PacksMenuView
        view = PacksMenuView()
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )
        unregister_pack_view(interaction.user.id)


    @discord.ui.button(label="Назад", style=discord.ButtonStyle.secondary, row=0)
    async def back_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.goto(interaction, get_pack_view(interaction.user.id))