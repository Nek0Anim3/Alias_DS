
import discord

from bot.views.base import BaseView
from debug.DebugLogger import DebugLogger


class PacksListView(BaseView):
    def __init__(self, packs: list[dict], interaction: discord.Interaction):
        from bot.views.packs.packs_menu import PacksMenuView
        self.menu_text = "Твої набори:" if packs else "Немає створених наборів"
        self.interaction = interaction
        super().__init__(back_view=None)

        for i, pack in enumerate(packs):

            self.add_item(PackButton(pack=pack, row=i // 3,))
        self.add_item(BackButton(row=4, view=PacksMenuView()))

class PackButton(discord.ui.Button):
    def __init__(self, pack: dict, row: int) -> None:
        super().__init__(
            label=f"Набір '{pack['name']}'",
            style=discord.ButtonStyle.primary,
            custom_id=f"pack_{pack['name']}",
            row=row
        )
        self.pack = pack


    async def callback(self, interaction: discord.Interaction):
        from bot.views.packs.packs_one_menu import PackDescriptionMenu

        view = PackDescriptionMenu(
            pack_name=self.pack['name'],
            words=self.pack['words'],
            word_count=len(self.pack['words'])
        )
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )



class BackButton(discord.ui.Button):
    def __init__(self, row: int, view):
        super().__init__(
            label="Назад",
            style=discord.ButtonStyle.secondary,
            row=row,
            )
        self._view = view


    async def callback(self, interaction: discord.Interaction):
        from bot.states.pack_view_state import unregister_pack_view
        from bot.views.packs.packs_menu import PacksMenuView
        unregister_pack_view(interaction.user.id)
        view = PacksMenuView()
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )