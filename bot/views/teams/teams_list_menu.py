
import discord

from bot.views.base import BaseView
from game.game_teams import register_team


class TeamsListView(BaseView):
    def __init__(self, interaction: discord.Interaction, host_id: int) -> None:
        self.host_id = host_id
        self.menu_text = "Оберіть команду, або створіть нову"
        self.interaction = interaction
        self.teams = []
        super().__init__(back_view=None)

        for i, team in self.teams:
            self.add_item(TeamButton(team=team, row=i // 3))
        self.add_item(CreateTeam(row=4, uid=self.host_id))

class TeamButton(discord.ui.Button):
    def __init__(self, team, row: int):
        super().__init__(
            label=f"Команда '{team['name']}'",
            style=discord.ButtonStyle.primary,
            custom_id=f"team_{team['name']}",
            row=row
        )

    async def callback(self, interaction: discord.Interaction):

        pass



class CreateTeam(discord.ui.Button):
    def __init__(self, row: int, uid: int):
        self.uid = uid
        super().__init__(
            label="Створити [+]",
            style=discord.ButtonStyle.success,
            row=row,
            )
    async def callback(self, interaction: discord.Interaction):
        from bot.states.lobby_state import get_views
        register_team(self.uid, interaction.user.name,[interaction.user.id])
        view = get_views(interaction.user.id)
        await interaction.response.edit_message(
            content=view.menu_text,
            view=view
        )
