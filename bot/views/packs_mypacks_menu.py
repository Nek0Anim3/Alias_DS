import discord


from bot.views.base import BaseView



class PacksListView(BaseView):
    def __init__(self, packs: list[dict]):
        from bot.views.packs_menu import PacksMenuView
        self.menu_text = "Твої набори:" if packs else "Немає створених наборів"
        super().__init__(back_view=None)

        for i, pack in enumerate(packs):
            self.add_item(PackButton(pack=pack, row=i // 3))
        self.add_item(BackButton(row=4, view=PacksMenuView()))

class PackButton(discord.ui.Button):
    def __init__(self, pack: dict, row: int):
        super().__init__(
            label=f"Набір '{pack['name']}'",
            style=discord.ButtonStyle.primary,
            custom_id=f"pack_{pack['name']}",  # уникальный id
            row=row
        )
        self.pack = pack

    async def callback(self, interaction: discord.Interaction):
        words = self.pack['words']
        words_str = "\n".join(f" {w}" for w in words)
        await interaction.response.edit_message( #FIX AttributeError 'BackButton' object has no attribute 'to_components'. Did you mean: 'from_component'? PLS
            content=f"Набір {self.pack['name']}\n"
                    f"Слів: {len(self.pack['words'])}\n"
                    f"{words_str}",
            view = BackButton(row=4, view=None)
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
        from bot.states.pack_view_state import get_pack_view
        if not self._view:
            self._view = get_pack_view(interaction.user.id)
        await interaction.response.edit_message(
            content=self._view.menu_text,
            view=self._view
        )