import discord


from bot.views.base import BaseView
from bot.views.lobby.lobby_player_menu import LobbyClientView

class JoinMenuView(BaseView):

    def __init__(self, interaction: discord.Interaction):
        super().__init__(back_view=None)
        self.menu_text = "Підключення до лобі.. \nВведіть код лобі"
        self.interaction = interaction


    #Метод на оновлення (перехід в даному випадку до некст менюшки)
    async def joinLobbySetView(self, player_count, players, code, lobby_name, host_id):
        from bot.states.client_lobby_state import register_client_lobby
        view = LobbyClientView(player_count=player_count, players=players, code=code, lobby_name=lobby_name, interaction=self.interaction, host_id=host_id)
        register_client_lobby(self.interaction.user.id, view)
        if self.message:
            await self.interaction.edit_original_response(content=view.menu_text, view=view)


    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.states.join_state import unregister_join_view
        from bot.states.states import clear_state
        from bot.views.main_menu import MainMenuView
        unregister_join_view(interaction.user.id)
        clear_state(interaction.user.id)
        await self.goto(interaction, MainMenuView())