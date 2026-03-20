
import discord


from bot.views.base import BaseView
from db.lobbyHandle import updatePackInLobby


class PacksSelectLobbyView(BaseView):
    def __init__(self, packs: list[dict], interaction: discord.Interaction, code: int) -> None:
        from bot.states.lobby_state import get_views
        self.code = code
        view = get_views(self.code)[interaction.user.id]
        self.menu_text = "Оберіть набір"
        self.interaction = interaction
        self.code = code
        super().__init__(back_view=None)

        for i, pack in enumerate(packs):
            self.add_item(PackButton(pack=pack, row=i // 3, code=self.code))
        self.add_item(BackButton(row=4, view=view))

class PackButton(discord.ui.Button):
    def __init__(self, pack: dict, row: int, code: int) -> None:
        super().__init__(
            label=f"Набір '{pack['name']}'",
            style=discord.ButtonStyle.primary,
            custom_id=f"pack_{pack['name']}",
            row=row
        )
        self.code = code
        self.pack = pack

    async def callback(self, interaction: discord.Interaction):
        await updatePackInLobby(interaction.user.id, self.pack['name'])
        from bot.states.lobby_state import get_views
        view = get_views(self.code)[interaction.user.id]
        await view.refreshLobby(pack_name=self.pack['name'])
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
        from bot.states.lobby_state import get_lobby_state
        view = get_lobby_state(interaction.user.id)
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )
