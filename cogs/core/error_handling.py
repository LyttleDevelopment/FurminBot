# Imports:
from datetime import datetime

from discord import Forbidden
from discord.ext import commands

from utils.emojis import emojis
from utils.utils import get_class_path


class ErrorHandler(commands.Cog):
    client: commands.Bot

    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_error(self, ctx: commands.Context, error: Exception):
        cog_name: str = get_class_path(ctx.cog)
        print(f"Error occurred in cog {cog_name}: {error}")
        # TODO: handle the fact the channel may not be postable in
        try:
            await ctx.send(f"{emojis.error} An error occurred. Contact us to help you fix it!")
            print(f"ERHD: An error occurred: {error}")
        except Exception as e:
            print("ERHD: An error occurred while sending the error, of course there was.")

        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] \"{ctx.author}\" in guild \"{ctx.guild.name}\" ({ctx.guild.id}): {error}\n"

        f = open(f"logs/{datetime.today().strftime('%Y-%m-%d')}.txt", "a+")
        f.write(log_msg)
        f.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{emojis.error} Please pass in all required arguments.')
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'{emojis.error} You do not have the required permissions.')
            pass
        elif isinstance(error, Forbidden):
            # I can't DM this user
            pass
        else:
            await self.send_error(ctx, error)


def setup(client):
    client.add_cog(ErrorHandler(client))
