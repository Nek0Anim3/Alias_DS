import discord

from bot.states.states import set_state, States
from bot.views.base import BaseView
from bot.views.packs_creation_menu import CreatePackMenu
from db.packs import fetchOwnPacks


class PacksMenuView(BaseView):
    menu_text = "Тут ви можете створити новий набір слів \nТакож можна продивитись існуючі набори"

    def __init__(self):
        from bot.views.main_menu import MainMenuView
        super().__init__(back_view=MainMenuView())

    @discord.ui.button(label="[+] Створити Набір", style=discord.ButtonStyle.green, row=0)
    async def create_pack_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.goto(interaction, CreatePackMenu("name", []))
        set_state(interaction.user.id, States.PACK_WAITING_NAME)

    @discord.ui.button(label="Мої набори", style=discord.ButtonStyle.primary, row=0)
    async def my_packs(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.packs_mypacks_menu import PacksListView
        packs = await fetchOwnPacks(interaction.user.id)
        await self.goto(interaction, PacksListView(packs))

    # @discord.ui.button(label="Список наборів", style=discord.ButtonStyle.secondary, row=1)
    # async def list_packs(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     await self.goto(interaction, PacksMenuView())