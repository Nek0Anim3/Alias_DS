import discord
from discord.ext import commands

from bot.views.main_menu import MainMenuView


class MenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @discord.slash_command(name="start", description="Відкриває стартове меню Alias")
    async def start_menu(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            view=MainMenuView(),
            ephemeral=True
        )

def setup(bot):
    bot.add_cog(MenuCog(bot))