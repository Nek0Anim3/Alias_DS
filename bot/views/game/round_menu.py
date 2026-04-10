from cProfile import label
from enum import Enum

import discord
from discord import Component

from bot.views.base import BaseView
from debug.DebugLogger import DebugLogger
from game.game_states import get_active_session


class RoundView(BaseView):
    def __init__(self, uid: int, interaction: discord.Interaction, host_id: int):
        self.host_id = host_id

        self.session = get_active_session(host_id)
        self.uid = uid
        self.players, self.current_word = self.session.get_game_data()
        self.menu_text = self._build_text(words=[self.current_word])
        self.words = [self.current_word]
        self.interaction = interaction
        from bot.connectBot import get_bot
        self.bot = get_bot()

        #Initial UI init for HOST!

        self.btn1 = ControlButton(interaction, type=ButtonTypes.GREEN)
        self.btn2 = ControlButton(interaction, type=ButtonTypes.RED)

        super().__init__(back_view=None)

        if interaction.user.id == host_id:
            self.add_item(self.btn1)
            self.add_item(self.btn2)

    #------------------------------------------------------------------------------------ quite a long constructor method...

    def _build_text(self, words):
        words_str = "\n".join(f"{w}" for w in words[:-1])
        return f"{words_str} <-"

    async def update_text(self):
        word = self.session.get_random_word(self.current_word)
        self.words.append(word)
        text = self._build_text(words=self.words)
        await self.interaction.edit_original_response(content=text, view=self)


    def rebase_view_buttons(self, role: RoleTypes):
        match role:
            case RoleTypes.LEADER:
                DebugLogger.Console(f"ROUNDS: Adding buttons to {self.uid}")
                self.add_item(self.btn1)
                self.add_item(self.btn2)
            case RoleTypes.MEMBER:
                self.remove_item(self.btn1)
                self.remove_item(self.btn2)
                DebugLogger.Console(f"ROUNDS: Removing button from {self.uid}")

    @discord.ui.button(label="Disable items", style=discord.ButtonStyle.primary, row=1)
    async def disable_button(self, button: discord.ui.Button, interaction: discord.Interaction):

        self.remove_item(self.btn1)
        self.remove_item(self.btn2)
        await self.interaction.edit_original_response(view=self, content=self.menu_text)

class ControlButton(discord.ui.Button):
    def __init__(self, interaction: discord.Interaction, type: ButtonTypes):
        if type == ButtonTypes.GREEN:
            super().__init__(
                    label="✅ Вгадав",
                    style=discord.ButtonStyle.success,
                    row=0
                )
        else:
            super().__init__(
                    label="❎ Не вгадав",
                    style=discord.ButtonStyle.danger,
                    row=0
                )
    async def callback(self, interaction: discord.Interaction):
        DebugLogger.Console("CALLBACK: Should update text")

class ButtonTypes(Enum):
    GREEN = 1
    RED = 2

class RoleTypes(Enum):
    LEADER = 1
    MEMBER = 2