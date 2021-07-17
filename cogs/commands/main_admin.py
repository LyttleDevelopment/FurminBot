from discord.ext import commands
from utils.logger import main_log
from utils.updater import get_head, update


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client

    async def cog_check(self, ctx: commands.Context):
        if not ctx.author.id == 132487290835435521:
            await ctx.send(f"You do not have the required permissions.")
            return False

        return True

    @commands.command()
    async def head(self, ctx):
        head_output = await get_head()
        await ctx.message.delete(delay=10)
        await ctx.send(head_output, delete_after=10)

    @commands.command()
    async def update(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send(f"> <@{self.client.user.id}> is Updating...")
        await main_log(ctx.bot, f"> **<@{self.client.user.id}> MAIN:** Updating...")
        await update(ctx.bot)


def setup(client):
    client.add_cog(Admin(client))
