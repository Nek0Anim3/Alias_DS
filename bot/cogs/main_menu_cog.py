import discord
from discord import slash_command
from discord.ext import commands
from bot.views.main_menu import MainMenuView
from bot.views.test_view import TestView

class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.slash_command(name="start", description="Відкриває стартове меню Еліас")
    async def start_menu(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            view=MainMenuView(),
            ephemeral=True
        )
        #MESsAGE ID ХЗ

def setup(bot):
    bot.add_cog(MenuCog(bot))