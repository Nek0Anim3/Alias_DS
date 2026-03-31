import discord
from discord.ext import commands
from bot.states.states import States, get_state, set_state, update_data, get_data
from bot.views.packs.packs_creation_menu import CreatePackMenu
from db.packs import checkPack


class CreatePacksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        state = get_state(user_id)
        if state == States.PACK_WAITING_NAME:
            await self.handlePackName(message)
        elif state == States.PACK_WAITING_WORDS:
            await self.handlePackWords(message)

    @staticmethod
    async def handlePackName(message: discord.Message):
        name = message.content
        #Додати перевірку на присутність у БД, щоб паки не можна було назвати однаково
        user_id = message.author.id
        pack = await checkPack(name)
        if pack is True:
            print(f"PACKS: {name} already exists in DB")
            await message.reply(f"'{name}' вже зайнято, введіть іншу назву")
            return
        set_state(user_id, States.PACK_WAITING_WORDS, pack_name=name, words=[])
        view = CreatePackMenu(stage="words", words=[])
        await message.reply(content=view.menu_text, view=view)

    @staticmethod
    async def handlePackWords(message: discord.Message):
        user_id = message.author.id
        word = message.content.strip()
        data = get_data(user_id)
        words = data.get("words", [])

        if word in words:
            await message.author.send(content=f"Слово {word} вже є у наборі")
            return
        words.append(word)
        update_data(user_id, words=words)
        view = CreatePackMenu(stage="words", words=words)
        await message.reply(content=view.menu_text, view=view)

def setup(bot):
    bot.add_cog(CreatePacksCog(bot))