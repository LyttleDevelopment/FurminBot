import os
import random
import discord

from typing import List
from discord.ext import commands
from discord.utils import get


class Welcoming(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcoming_channel = self.client.get_channel(848670878137057290)
        picture = random.randint(1, 28)
        embed = discord.Embed(title=f"Welcome {member} to the Bestie of Friend's discord server!",
                              description=f"To begin, read the <#848675484611248179>. "
                                          f"If you want any tags go to <#848995808317407252> "
                                          f"and assign them to yourself! "
                                          f"Good luck and welcome to our nice community.",
                              color=0x007db3)
        embed.set_image(url=f"https://f.lyttle.it/{picture}.gif")
        await welcoming_channel.send(embed=embed)


def setup(client):
    client.add_cog(Welcoming(client))
