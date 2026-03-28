
import discord

from bot.views.base import BaseView
from game.game_teams import register_team, get_lobby_teams, join_team


class TeamsListView(BaseView):
    def __init__(self, interaction: discord.Interaction, host_id: int, back_view):
        self.host_id = host_id
        self.back_view = back_view
        self.menu_text = "Оберіть команду, або створіть нову"
        self.interaction = interaction
        self.teams = get_lobby_teams(self.host_id)
        super().__init__(back_view=None)
        for team in self.teams:
            print("DEBUG: teams:", team)
            self.add_item(TeamButton(team=team, row=len(self.teams) // 3, lobby_id=self.host_id, team_list_view=self))
        self.add_item(CreateTeam(row=4, uid=self.host_id, teamlistview=self))
        self.add_item(BackButton(teamlistview=self))

class TeamButton(discord.ui.Button):
    def __init__(self, team, row: int, lobby_id: int, team_list_view: TeamsListView):
        self.team = team
        self.teamListView = team_list_view
        self.lobby_id = lobby_id
        super().__init__(
            label=f"Команда '{team}'",
            style=discord.ButtonStyle.primary,
            custom_id=f"team_{team}",
            row=row
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.name != self.team:
            join_team(lobby_id=self.lobby_id, player_id=interaction.user.id, team_name=self.team)
            print(f"{interaction.user.id} JOINED TEAM {self.team}")
            view = self.teamListView.back_view
            await view.refresh_lobby(team_name=self.team)
            await interaction.response.edit_message(content=view.menu_text, view=view)
        else:
            print(f"TEAMS: Exception! Cannot join player {interaction.user.name} to self team")



class CreateTeam(discord.ui.Button):
    def __init__(self, row: int, uid: int, teamlistview: TeamsListView):
        self.uid = uid
        self.teamlistview = teamlistview
        super().__init__(
            label="Створити [+]",
            style=discord.ButtonStyle.success,
            row=row,
            )
    async def callback(self, interaction: discord.Interaction):
        register_team(self.uid, interaction.user.name,[interaction.user.id])
        back_view = self.teamlistview.back_view
        await back_view.refresh_lobby(team_name=interaction.user.name)
        await interaction.response.edit_message(
            content=back_view.menu_text,
            view=back_view
        )

class BackButton(discord.ui.Button):
    def __init__(self, teamlistview: TeamsListView):
        self.teamlistview = teamlistview
        super().__init__(
            label="Назад",
            style=discord.ButtonStyle.secondary,
            row=4,
            )
    async def callback(self, interaction: discord.Interaction):
        back_view = self.teamlistview.back_view
        await interaction.response.edit_message(
            content=back_view.menu_text,
            view=back_view
        )