from cProfile import label
from enum import Enum

import discord
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

        super().__init__(back_view=None)

        if interaction.user.id == host_id:
            self.add_item(ControlButton(interaction, type=ButtonTypes.GREEN))
            self.add_item(ControlButton(interaction, type=ButtonTypes.RED))

    #------------------------------------------------------------------------------------ quite a long constructor method...

    def _build_text(self, words):
        words_str = "\n".join(f"{w}" for w in words[:-1])
        return f"{words_str} <-"

    async def update_text(self):
        word = self.session.get_random_word(self.current_word)
        self.words.append(word)
        text = self._build_text(words=self.words)
        await self.interaction.edit_original_response(content=text, view=self)

    # @discord.ui.button(label="✅ Вгадав", style=discord.ButtonStyle.success, row=0)
    # async def like_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     self.bot.dispatch("ui_game_update")
    #
    # @discord.ui.button(label="❎ Не вгадав", style=discord.ButtonStyle.danger, row=0)
    # async def dislike_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     self.bot.dispatch("ui_game_update")

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
                    style=discord.ButtonStyle.success,
                    row=0
                )
    async def callback(self, interaction: discord.Interaction):
        DebugLogger.Console("CALLBACK: Should update text")

class ButtonTypes(Enum):
    GREEN = 1
    RED = 2
