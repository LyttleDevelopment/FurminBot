import os
from typing import List

import discord
from discord.ext import commands
from discord.utils import get
from utils.json_manager import load_json, save_json


class RoleButtons(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = client

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        user = self.bot.get_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = get(guild.members, id=payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)

        if user.bot or channel.id != 848995808317407252:
            return

        roles = load_json("role_buttons")

        role_id = int(roles[f"{payload.emoji.id}"])
        role = get(guild.roles, id=role_id)
        await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = self.bot.get_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = get(guild.members, id=payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)

        if user.bot or channel.id != 848995808317407252:
            return

        roles = load_json("role_buttons")

        role_id = int(roles[f"{payload.emoji.id}"])
        role = get(guild.roles, id=role_id)
        await member.add_roles(role)


def setup(client):
    client.add_cog(RoleButtons(client))
