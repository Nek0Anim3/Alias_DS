import asyncio

import discord


from bot.views.base import BaseView
from db.lobbyHandle import deleteLobbyDB
from db.userHandle import removePlayerfromDB


class LobbyMenuView(BaseView):
    def __init__(self, uname: str, code: int, player_count: int, players: list, interaction: discord.Interaction):
        self.uname = uname
        self.code = code
        self.player_count = player_count
        self.players = players
        self.interaction = interaction
        self.menu_text = self._build_text()
        super().__init__(back_view=None)

    def _build_text(self):
        players_str = "\n".join(f"{p}" for p in self.players)
        return (
            f"Лобі {self.uname}\n"
            f"Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"Код: {self.code}\n"
        )


    async def refreshLobby(self, player_count: int, players: list): #не забути про те, що тут метод повинен оновлювати ще список гравців
        #ще можна копіпаст цього методу для інших менюшок де це реально буде необхідно в реалтаймі
        self.player_count = player_count
        self.players = players
        self.menu_text = self._build_text()
        if self.message:
            await self.interaction.edit_original_response(content=self.menu_text, view=self)


    @discord.ui.button(label="Почати Гру", style=discord.ButtonStyle.primary, row=0)
    async def start_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        from bot.states.lobby_state import unregister_view
        unregister_view(self.code)
        await asyncio.gather(
            deleteLobbyDB(interaction.user.id),
            removePlayerfromDB(interaction.user.id),
            self.goto(interaction, MainMenuView())
        )
