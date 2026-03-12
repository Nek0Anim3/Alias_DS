import discord

from bot.views.base import BaseView

class PacksMenuView(BaseView):
    menu_text = "Правила Alias"

    def __init__(self):
        from bot.views.main_menu import MainMenuView
        super().__init__(back_view=MainMenuView)

    @discord.ui.button(label="ПРИКОЛ", style=discord.ButtonStyle.primary, row=0)
    async def open_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.goto(interaction, PacksMenuView())