from discord.ext import commands
from utils.emojis import emojis


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client

    async def cog_check(self, ctx: commands.Context):
        # admin = get(ctx.guild.roles, name="Admin")
        # return admin in ctx.author.roles
        # return ctx.author.guild_permissions.manage_messages
        should_succeed = True
        if not ctx.author.guild_permissions.manage_messages:
            should_succeed = False
            await ctx.send(f'{emojis.error} You do not have the required permissions.')
        return should_succeed

    # Command:
    @commands.command()
    async def help(self, ctx, amount=5):
        print("no help for you, muhahahaha")


def setup(client):
    client.add_cog(Help(client))
