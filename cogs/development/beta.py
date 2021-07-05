# Imports:
from discord.ext import commands


# Actions/commands:
class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx: commands.Context):
        return ctx.author.id == 132487290835435521

    # @commands.command()
    # async def test(self, ctx: commands.Context):
    #     print(ctx.guild)

    # @commands.Cog.listener()

    # @commands.command()


def setup(client):
    client.add_cog(Test(client))
