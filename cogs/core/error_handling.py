from datetime import datetime
from discord import Forbidden
from discord.ext import commands
from utils.logger import error_log
from utils.utils import get_class_path


class ErrorHandler(commands.Cog):
    client: commands.Bot

    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_error(self, ctx: commands.Context, error: Exception):
        cog_name: str = get_class_path(ctx.cog)
        print(
            f"> **<@{self.client.user.id}> ERHR:** Error occurred in cog {cog_name}: {error}"
        )
        await error_log(
            self.client,
            f"> **<@{self.client.user.id}> ERHR:** Error occurred in cog {cog_name}: {error}",
        )
        # TODO: handle the fact the channel may not be postable in
        try:
            await error_log(self.client, f"ERHR: An error occurred: {error}")
            print(f"> **<@{self.client.user.id}> ERHR:** An error occurred: {error}")
        except Exception as e:
            await error_log(
                self.client,
                f"> **<@{self.client.user.id}> ERHR:** An error occurred while sending the error, of course there was.",
            )
            print(
                "ERHR: An error occurred while sending the error, of course there was."
            )

        log_msg = (
            f"[{datetime.now().strftime('%H:%M:%S')}] \"{ctx.author}\" in guild "
            f'"{ctx.guild.name}" ({ctx.guild.id}): {error}\n'
        )

        f = open(f"logs/{datetime.today().strftime('%Y-%m-%d')}.txt", "a+")
        f.write(log_msg)
        f.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"> **Please pass in all required arguments.**")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"> **You're on cooldown, try again in {error.retry_after:.2f} seconds.**"
            )
        if isinstance(error, Forbidden):
            await error_log(
                self.client,
                f"> **<@{self.client.user.id}> ERHR:** An error occurred: {error}",
            )
            # I can't DM this user
            pass
        else:
            await error_log(
                self.client,
                f"> **<@{self.client.user.id}> ERHR:** An error occurred: {error}",
            )
            await self.send_error(ctx, error)


def setup(client):
    client.add_cog(ErrorHandler(client))
