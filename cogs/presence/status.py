import discord
from discord import Member
from discord.ext import commands, tasks
from utils.config import config
from itertools import cycle


class Status(commands.Cog):
    def __init__(self, client: Member):
        self.client = client
        self.change_status.start(client)

    status = cycle(config.status)
    status_nr = cycle(config.status_nr)

    @tasks.loop(seconds=20)
    async def change_status(self, client):
        # await self.client.change_presence(activity=discord.Game(next(self.status)))
        await self.client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                name=f"{next(self.status)}", type=next(self.status_nr)
            ),
        )


def setup(client):
    client.add_cog(Status(client))
