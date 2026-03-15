from bot.states.states import clear_state
from bot.views.base import BaseView
import discord

from bot.views.main_menu import MainMenuView


class JoinMenuView(BaseView):

    def __init__(self):
        super().__init__(back_view=None)
        self.menu_text = "Підключення до лобі.. \nВведіть код лобі"


    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        clear_state(interaction.user.id)
        await self.goto(interaction, MainMenuView())