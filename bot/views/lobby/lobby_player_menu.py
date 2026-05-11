import asyncio

import discord


from bot.views.base import BaseView
from bot.views.teams.teams_list_menu import TeamsListView
from db.lobbyHandle import leaveLobbyDB, findLobbyByCode
from db.userHandle import removePlayerfromDB
from debug.DebugLogger import DebugLogger


class LobbyClientView(BaseView):
    def __init__(self, lobby_name, player_count: int, players: list, code: int, interaction: discord.Interaction, host_id: int):
        self.host_id = host_id
        self.lobby_name = lobby_name
        self.player_count = player_count
        self.team_name = "Не обрано"
        self.players = players
        self.code = code
        self.menu_text = self._build_text()
        self.interaction = interaction
        super().__init__(back_view=None)

    def _build_text(self):
        players_str = "\n".join(f"{p}" for p in self.players)
        return (
            f"Хост лобі: {self.lobby_name}\n"
            f"------------------\n"
            f"🫂 Ваша команда {self.team_name}\n"
            f"------------------\n"
            f"👤 Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"------------------\n"
            f"⌚ Очікуйте початку гри..."
        )
    async def refresh_lobby(self, team_name: str):

        self.team_name = team_name
        self.menu_text = self._build_text()

    @discord.ui.button(label="Обрати команду", style=discord.ButtonStyle.primary, row=4)
    async def select_team(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = TeamsListView(interaction, self.host_id, self)
        await self.goto(interaction, view=view)

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=1)
    async def quit_lobby_client(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        from bot.states.client_lobby_state import unregister_client_lobby
        unregister_client_lobby(interaction.user.id)
        await asyncio.gather(
            removePlayerfromDB(interaction.user.id),
            leaveLobbyDB(self.code, interaction.user.id, interaction.user.name),
            self.goto(interaction, MainMenuView())
        )
        lobby = await findLobbyByCode(self.code)
        from bot.connectBot import get_bot
        bot = get_bot()
        bot.dispatch("update_lobby", lobby)

    async def exit_lobby(self):
        from bot.views.main_menu import MainMenuView
        from bot.connectBot import get_bot
        DebugLogger.Console("EXITING LOBBY CLIENT")
        view = MainMenuView()
        bot = get_bot()
        bot.dispatch("exit_client_lobby", self.interaction.user.name)
        await self.interaction.edit_original_response(
            content=view.menu_text, view=view)
