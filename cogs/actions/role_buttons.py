import os
import re
import discord

from typing import List
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

        if payload.emoji.id == 809136459868798976:
            role = get(guild.roles, id=842873737774235659)
            await member.remove_roles(role)
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
        admin_channel = self.client.get_channel(802288905599975444)

        if payload.channel_id == 802288905599975444:
            message = await channel.fetch_message(payload.message_id)
            user_id = re.findall(r"\|\|ID:(.*)\|\|", message.content)
            member = get(guild.members, id=int(user_id[0]))
            role = get(guild.roles, id=842873737774235659)
            await member.add_roles(role)
            await admin_channel.send(f"<@{payload.user_id}> gave the NSFW role to <@{user_id[0]}>")
            return

        if user.bot or channel.id != 848995808317407252:
            return

        if payload.emoji.id == 809136459868798976:
            await admin_channel.send(f"<@{payload.user_id}> requested the NSFW role? going to give that?"
                                     f"\nIf yes, react with any emoji to this message. ||ID:{payload.user_id}||")
            return

        roles = load_json("role_buttons")

        role_id = int(roles[f"{payload.emoji.id}"])
        role = get(guild.roles, id=role_id)
        await member.add_roles(role)


def setup(client):
    client.add_cog(RoleButtons(client))
