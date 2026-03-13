import discord
from bot.views.base import BaseView

from db.packs import addPack


class CreatePackMenu(BaseView):

    def __init__(self, stage: str, words: list = None):
        self.menu_text = self._build_text(stage, words)
        super().__init__(back_view=None)
        self.stage = stage

    def _build_text(self, stage: str, words: list):
        if stage == "name":
            return "Створення набору слів (1/2)\nВведіть ім'я набору слів:"
        else:
            words_str = "\n".join(f" {w}" for w in words) if words else "поки немає слів"
            return(
                f"Створення набору слів (2/2)\n\n"
                f"Кількість слів: {len(words)}\n"
                f"{words_str}\n\n"
                f"Пишіть слова в чат, або натисніть Готово"
            )

    @discord.ui.button(label="Готово", style=discord.ButtonStyle.green, row=0)
    async def done_pack(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.states.states import get_state, get_data
        state = get_state(interaction.user.id)

        if state == "pack_waiting_name":
            await interaction.response.send_message(
                "Спочатку введи назву набору!",
                ephemeral=True
            )
            return
        data = get_data(interaction.user.id)
        words = data.get("words", [])
        if len(words) == 0:
            await interaction.response.send_message("Мінімум додайте одне слово!", ephemeral=True)
            return

        await addPack(data.get("pack_name"), words, interaction.user.id)#Виклик БД

        from bot.views.packs_menu import PacksMenuView
        await self.goto(interaction, PacksMenuView())

    @discord.ui.button(label="Назад", style=discord.ButtonStyle.danger, row=4)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.states.states import clear_state
        from bot.views.packs_menu import PacksMenuView

        clear_state(interaction.user.id)
        view = PacksMenuView()
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )