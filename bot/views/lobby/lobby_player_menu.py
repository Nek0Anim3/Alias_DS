import asyncio

from bot.views.base import BaseView
import discord


from db.lobbyHandle import leaveLobbyDB
from db.userHandle import removePlayerfromDB


class LobbyClientView(BaseView):
    def __init__(self, lobby_name, player_count: int, players: list, code: int):
        self.lobby_name = lobby_name
        self.player_count = player_count
        self.players = players
        self.code = code
        self.menu_text = self._build_text()
        super().__init__(back_view=None)

    def _build_text(self):
        players_str = "\n".join(f"{p}" for p in self.players)
        return (
            f"Хост лобі {self.lobby_name}\n"
            f"Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"Очікуйте початку гри..."
        )

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=1)
    async def quit_lobby_client(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        await asyncio.gather(
            removePlayerfromDB(interaction.user.id),
            leaveLobbyDB(self.code, interaction.user.id, interaction.user.name),
            self.goto(interaction, MainMenuView())
        )
        from bot.connectBot import get_bot
        bot = get_bot()
        bot.dispatch("update_lobby", self.code)

